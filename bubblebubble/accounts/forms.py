from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import ShippingAddress

User = get_user_model()


class EmailUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email address")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",)

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        # Since we store email in username too, we must ensure uniqueness
        if User.objects.filter(
            username__iexact=email).exists() or User.objects.filter(
                email__iexact=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists. "
                "Try logging in instead."
            )
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data["email"]  # already cleaned + lowercased
        user.username = email               # keep username unique
        user.email = email
        if commit:
            user.save()
        return user


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            "label",
            "full_name",
            "address_line1",
            "address_line2",
            "city",
            "postcode",
            "is_default",
        ]
        widgets = {
            "label": forms.TextInput(attrs={"class": "form-control"}),
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "address_line1": forms.TextInput(attrs={"class": "form-control"}),
            "address_line2": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "postcode": forms.TextInput(attrs={"class": "form-control text-uppercase"}),
            "is_default": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }