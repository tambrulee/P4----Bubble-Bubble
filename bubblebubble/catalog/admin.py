from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "product_type", "scent", "price", "stock_qty", "active")
    list_filter = ("product_type", "scent", "active")
    search_fields = ("title", "scent", "description")
    prepopulated_fields = {"slug": ("title",)}
