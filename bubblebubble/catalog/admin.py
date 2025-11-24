from django.contrib import admin
from .models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "product_type", "scent", "price", "stock_qty", "active")
    list_filter = ("product_type", "scent", "active")
    search_fields = ("title", "scent", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProductImageInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "alt_text")


