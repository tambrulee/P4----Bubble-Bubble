from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]

    def clean_rating(self):
        """Ensure rating is between 1 and 5."""
        r = self.cleaned_data["rating"]
        if not 1 <= r <= 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return r
