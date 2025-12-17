from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
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
                "placeholder": "Full name",
                "autocomplete": "name",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Email address",
                "autocomplete": "email",
            }),
            "address_line1": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Address line 1",
                "autocomplete": "address-line1",
            }),
            "address_line2": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Address line 2 (optional)",
                "autocomplete": "address-line2",
            }),
            "city": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "City",
                "autocomplete": "address-level2",
            }),
            "postcode": forms.TextInput(attrs={
                "class": "form-control text-uppercase",
                "placeholder": "Postcode",
                "autocomplete": "postal-code",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # make these required at checkout (even though model has blank=True)
        required = ["full_name", "email", "address_line1", "city", "postcode"]
        for f in required:
            self.fields[f].required = True

        # nice label text for floating labels (optional)
        self.fields["full_name"].label = "Full name"
        self.fields["email"].label = "Email address"
        self.fields["address_line1"].label = "Address line 1"
        self.fields["address_line2"].label = "Address line 2 (optional)"
        self.fields["city"].label = "City"
        self.fields["postcode"].label = "Postcode"
