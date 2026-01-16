# checkout/forms.py
from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    saved_address = forms.ModelChoiceField(
        queryset=None,  # set in __init__
        required=False,
        empty_label="Use a saved address…",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    save_address = forms.BooleanField(
        required=False,
        label="Save this address for next time",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = Order
        fields = [
            "full_name",
            "email",
            "address_line1",
            "address_line2",
            "city",
            "postcode",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": " ",
                "autocomplete": "name",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": " ",
                "autocomplete": "email",
            }),
            "address_line1": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": " ",
                "autocomplete": "address-line1",
            }),
            "address_line2": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": " ",
                "autocomplete": "address-line2",
            }),
            "city": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": " ",
                "autocomplete": "address-level2",
            }),
            "postcode": forms.TextInput(attrs={
                "class": "form-control text-uppercase",
                "placeholder": " ",
                "autocomplete": "postal-code",
            }),
        }

    def __init__(self, *args, **kwargs):
        """Initialize form, set required fields and handle user-specific logic."""
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # required fields
        required = ["full_name", "email", "address_line1", "city", "postcode"]
        for f in required:
            self.fields[f].required = True

        # labels
        self.fields["full_name"].label = "Full name"
        self.fields["email"].label = "Email address"
        self.fields["address_line1"].label = "Address line 1"
        self.fields["address_line2"].label = "Address line 2 (optional)"
        self.fields["city"].label = "City"
        self.fields["postcode"].label = "Postcode"

        # Logged-in users: show dropdown + checkbox
        if user and user.is_authenticated:
            from accounts.models import ShippingAddress
            self.fields["saved_address"].queryset = (
                ShippingAddress.objects.filter(
                    user=user).order_by("-is_default", "-created_at")
            )
        else:
            # Guests: hide them
            self.fields.pop("saved_address", None)
            self.fields.pop("save_address", None)

        if user and user.is_authenticated:
            from accounts.models import ShippingAddress
            qs = ShippingAddress.objects.filter(user=user).order_by("-is_default", "-created_at")
            self.fields["saved_address"].queryset = qs

            # Add data-* attributes to each option for JS autofill
            choices = [("", "Use a saved address…")]
            for addr in qs:
                choices.append((
                    addr.pk,
                    str(addr),
                ))
            self.fields["saved_address"].choices = choices
