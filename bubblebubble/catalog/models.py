from django.db import models
from django.utils.text import slugify

class Product(models.Model):
    CANDLE = "CANDLE"
    SOAP = "SOAP"
    TYPES = [
        (CANDLE, "Candle"),
        (SOAP, "Soap"),
    ]

    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    product_type = models.CharField(max_length=12, choices=TYPES)
    description = models.TextField(blank=True)
    scent = models.CharField(max_length=50, help_text="e.g. Lavender, Citrus")
    burn_time_min = models.PositiveIntegerField(null=True, blank=True)  # candles only
    weight_g = models.PositiveIntegerField(help_text="Net weight in grams")
    price = models.DecimalField(max_digits=6, decimal_places=2)  # e.g. 12.99
    stock_qty = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    image_url = models.URLField(blank=True)  # keep it simple: link to an image
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug = base
            i = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
