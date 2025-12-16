from django import forms
from catalog.models import Product, ProductImage


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "title",
            "product_type",
            "description",
            "scent",
            "weight_g",
            "price",
            "stock_qty",
            "active",
        ]


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ["image", "alt_text"]
