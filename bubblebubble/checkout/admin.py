from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "qty", "unit_price")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id", "created_at", "full_name", "email", "total", "status")
    list_filter = ("status", "created_at")
    search_fields = (
        "id", "full_name", "email", "postcode", "stripe_session_id")
    ordering = ("-created_at",)
    inlines = [OrderItemInline]

    # usually you don't want staff editing financial truth by accident:
    readonly_fields = ("total", "stripe_session_id", "created_at")
