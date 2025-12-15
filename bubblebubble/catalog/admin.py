from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Product, ProductImage
from .resources import ProductResource


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.action(description="Deactivate selected products")
def deactivate_products(modeladmin, request, queryset):
    queryset.update(active=False)


@admin.action(description="Activate selected products")
def activate_products(modeladmin, request, queryset):
    queryset.update(active=True)


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ("title", "product_type", "scent", "price", "stock_qty", "active")
    list_filter = ("product_type", "scent", "active")
    search_fields = ("title", "scent", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProductImageInline]                 # ✅ attach inline
    actions = [activate_products, deactivate_products]  # ✅ bulk actions


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "alt_text")
