from django import forms


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100, label="Full name")
    email = forms.EmailField(label="Email address")
    address_line1 = forms.CharField(max_length=255, required=False, label="Address line 1")
    address_line2 = forms.CharField(max_length=255, required=False, label="Address line 2")
    city = forms.CharField(max_length=100, required=False)
    postcode = forms.CharField(max_length=20, required=False, label="Postcode")
