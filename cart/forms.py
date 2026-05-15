from django import forms


class AddToCartForm(forms.Form):
    qty = forms.IntegerField(min_value=1, max_value=10)

    def __init__(self, *args, max_stock=10, **kwargs):
        """Initialize form and set max_value for qty based on stock."""
        super().__init__(*args, **kwargs)
        self.max_stock = max_stock
        self.fields["qty"].max_value = min(10, max_stock)

    def clean_qty(self):
        """Validate that requested quantity does not exceed stock."""
        q = self.cleaned_data["qty"]
        if q > self.max_stock:
            raise forms.ValidationError("Not enough stock available.")
        return q
