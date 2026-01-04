from django.db import models
from django.utils.text import slugify


class Product(models.Model):

    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    description = models.TextField(blank=True)
    scent = models.CharField(max_length=50, help_text="e.g. Lavender, Citrus")
    weight_g = models.PositiveIntegerField(help_text="Net weight in grams")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock_qty = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # NEW
    tags = models.CharField(
        max_length=250,
        blank=True,
        help_text="Comma-separated tags, e.g. winter, woody, refillable"
    )

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


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField(max_length=140, blank=True)

    def __str__(self):
        return f"Image for {self.product.title}"
