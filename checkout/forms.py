import re

from django import forms
from django.core.validators import RegexValidator

from .models import Order

UK_POSTCODE_RE = (
    r"^([Gg][Ii][Rr]\s?0[Aa]{2})|"
    r"((([A-Za-z][0-9]{1,2})|"
    r"(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|"
    r"(([A-Za-z][0-9][A-Za-z])|"
    r"([A-Za-z][A-Ha-hJ-Yj-y][0-9][A-Za-z]?))))\s?"
    r"[0-9][A-Za-z]{2})$"
)

postcode_validator = RegexValidator(
    regex=UK_POSTCODE_RE,
    message="Enter a valid UK postcode.",
)


class CheckoutForm(forms.ModelForm):
    """
    Checkout form backed by Order, with optional saved-address support
    for logged-in users and full server-side validation (JS optional).
    """

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
        """
        Attach user for saved-address validation, configure required fields,
        add HTML required attributes, and build the saved-address dropdown.
        """
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # If this is a bound form (POST), add Bootstrap invalid classes to fields with errors
        if self.is_bound:
            for name in self.fields:
                if name == "saved_address":
                    continue
                if self.errors.get(name):
                    css = self.fields[name].widget.attrs.get("class", "")
                    if "is-invalid" not in css:
                        self.fields[name].widget.attrs["class"] = (css + " is-invalid").strip()

        # --- Add HTML required attrs for browser/Bootstrap validation ---
        for name, field in self.fields.items():
            if field.required:
                field.widget.attrs["required"] = "required"

        # Ensure saved_address never participates in HTML validation
        if "saved_address" in self.fields:
            self.fields["saved_address"].required = False
            self.fields["saved_address"].widget.attrs.pop("required", None)
            self.fields["saved_address"].widget.attrs["data-no-validate"] = "true"

        # --- Make certain fields required server-side ---
        required = ["full_name", "email", "address_line1", "city", "postcode"]
        for name in required:
            self.fields[name].required = True
            self.fields[name].widget.attrs["required"] = "required"

        # --- Postcode validator ---
        self.fields["postcode"].validators.append(postcode_validator)

        # --- Guest users: hide saved-address fields ---
        if not (self.user and self.user.is_authenticated):
            self.fields.pop("saved_address", None)
            self.fields.pop("save_address", None)
            return

        # --- Logged-in users: set saved address queryset & choices ---
        from accounts.models import ShippingAddress

        qs = ShippingAddress.objects.filter(user=self.user).order_by(
            "-is_default", "-created_at"
        )
        self.fields["saved_address"].queryset = qs
        self.fields["saved_address"].choices = [("", "Use a saved address…")] + [
            (addr.pk, str(addr)) for addr in qs
        ]

    def clean(self):
        cleaned = super().clean()

        saved = cleaned.get("saved_address")
        if not saved:
            return cleaned

        # If anything about saved is off, just ignore it (no errors)
        if not (self.user and self.user.is_authenticated):
            cleaned["saved_address"] = None
            return cleaned

        if getattr(saved, "user_id", None) != self.user.id:
            cleaned["saved_address"] = None
            return cleaned

        # If valid, overwrite from saved address
        cleaned["full_name"] = saved.full_name or cleaned.get("full_name", "")
        cleaned["address_line1"] = saved.address_line1
        cleaned["address_line2"] = saved.address_line2 or ""
        cleaned["city"] = saved.city
        cleaned["postcode"] = saved.postcode

        return cleaned

    def clean_postcode(self):
        """
        Normalize postcode formatting:
        - strip, uppercase
        - remove extra spaces
        - reinsert single space before last 3 chars
        """
        pc = (self.cleaned_data.get("postcode") or "").strip().upper()
        pc = re.sub(r"\s+", "", pc)

        if not pc:
            return pc

        if len(pc) > 3:
            pc = pc[:-3] + " " + pc[-3:]

        return pc
