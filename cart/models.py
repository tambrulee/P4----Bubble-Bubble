from django.db import models
from django.conf import settings
from catalog.models import Product


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.CASCADE
    )
    session_key = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of the cart."""
        return f"Cart {self.pk} for {self.user or self.session_key}"

    @property
    def total(self):
        """Calculate the total cost of all items in the cart."""
        return sum(
            item.subtotal for item in self.items.select_related("product"))


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product")

    @property
    def subtotal(self):
        """Calculate the subtotal for this cart item."""
        return self.qty * self.product.price
