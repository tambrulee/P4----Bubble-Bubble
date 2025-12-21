from django.db import models
from django.conf import settings
from catalog.models import Product


class Order(models.Model):
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"
    NEW = "NEW"
    DISPATCHED = "DISPATCHED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (PAID, "Paid"),
        (FAILED, "Failed"),
    ]

    FULFILMENT_CHOICES = [
        (NEW, "New"),
        (DISPATCHED, "Dispatched"),
        (DELIVERED, "Delivered"),
        (CANCELLED, "Cancelled"),
    ]

    # user now optional – allows guest orders
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )

    # guest / contact details
    full_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    postcode = models.CharField(max_length=20, blank=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDING,
    )
    total = models.DecimalField(max_digits=8, decimal_places=2)
    stripe_session_id = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    stock_deducted = models.BooleanField(default=False)

    fulfilment_status = models.CharField(
        max_length=12,
        choices=FULFILMENT_CHOICES,
        default=NEW,
    )

    dispatched_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        who = self.user or self.email or "guest"
        return f"Order #{self.id} for {who}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    def subtotal(self):
        return self.qty * self.unit_price

    def __str__(self):
        return f"{self.product} x {self.qty}"

