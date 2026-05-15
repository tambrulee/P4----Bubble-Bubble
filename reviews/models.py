from django.db import models
from django.conf import settings
from django.utils import timezone
from catalog.models import Product
from checkout.models import Order


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    verified_purchase = models.BooleanField(default=False)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)

    is_approved = models.BooleanField(default=False)
    owner_reply = models.TextField(blank=True)
    owner_replied_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options for Review model."""
        unique_together = ("user", "product")
        ordering = ["-created_at"]

    def __str__(self):
        """Return a string representation of the review."""
        return f"Review of {self.product} by {self.user}"

    def set_owner_reply_timestamp(self):
        """Set the timestamp when the owner replies to the review."""
        self.owner_replied_at = timezone.now()
