from django import forms


class AddToCartForm(forms.Form):
    qty = forms.IntegerField(min_value=1, max_value=10)

    def __init__(self, *args, max_stock=10, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_stock = max_stock
        self.fields["qty"].max_value = min(10, max_stock)

    def clean_qty(self):
        q = self.cleaned_data["qty"]
        if q > self.max_stock:
            raise forms.ValidationError("Not enough stock available.")
        return q
