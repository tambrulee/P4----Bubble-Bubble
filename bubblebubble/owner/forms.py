from django import forms
from catalog.models import Product, ProductImage
from reviews.models import Review



class ProductForm(forms.ModelForm):

    class Meta:

        model = Product
        fields = [
            "title",
            "description",
            "scent",
            "weight_g",
            "price",
            "stock_qty",
            "active",
            "tags",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
            }),
            "scent": forms.TextInput(attrs={"class": "form-control"}),
            "weight_g": forms.NumberInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
            }),
            "stock_qty": forms.NumberInput(attrs={"class": "form-control"}),
            "tags": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. winter, woody, refillable",
            }),
        }

    def clean_tags(self):
        tags = self.cleaned_data.get("tags", "")
        cleaned = ", ".join(
            t.strip().lower()
            for t in tags.split(",")
            if t.strip()
        )
        return cleaned


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ["image", "alt_text"]


class OwnerReplyForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["owner_reply"]
        widgets = {
            "owner_reply": forms.Textarea(attrs={"rows": 4, "placeholder": "Write a public reply…"})
        }