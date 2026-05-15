from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
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
        """Auto-generate slug from title if not provided."""
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
        """Return a string representation of the product."""
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField(max_length=140, blank=True)

    def __str__(self):
        """Return a string representation of the product image."""
        return f"Image for {self.product.title}"

    def save(self, *args, **kwargs):
        """
        Save the ProductImage, converting uploads to compressed WebP and
        resizing to a sensible max size for faster delivery (Lighthouse/LCP).
        """
        # If no image attached, save normally
        if not self.image:
            return super().save(*args, **kwargs)

        # If this is an existing instance and the image hasn't changed, save normally
        if self.pk:
            try:
                old = ProductImage.objects.get(pk=self.pk)
                if old.image and old.image.name == self.image.name:
                    return super().save(*args, **kwargs)
            except ProductImage.DoesNotExist:
                pass

        # Open uploaded image
        self.image.seek(0)
        img = Image.open(self.image)

        # Convert to RGB to avoid issues with PNGs (alpha) etc.
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Resize down (adjust these numbers to your UI needs)
        # Product cards were ~656px wide in Lighthouse; this sets an upper bound.
        max_w, max_h = 1200, 1200
        img.thumbnail((max_w, max_h), Image.LANCZOS)

        # Encode as WebP
        buffer = BytesIO()
        img.save(buffer, format="WEBP", quality=78, method=6)
        buffer.seek(0)

        # Ensure filename ends with .webp
        base_name = self.image.name.rsplit(".", 1)[0]
        webp_name = f"{base_name}.webp"

        # Replace the uploaded file with the optimised one
        self.image.save(webp_name, ContentFile(buffer.read()), save=False)

        super().save(*args, **kwargs)
