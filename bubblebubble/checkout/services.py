from django.db import transaction
from django.db.models import F
from django.core.exceptions import ValidationError

from catalog.models import Product
from .models import Order


@transaction.atomic
def deduct_stock_for_order(order_id: int) -> None:
    """
    Deduct stock exactly once for a PAID order.
    Uses DB locks to prevent overselling and double-deduct.
    """
    order = Order.objects.select_for_update().get(pk=order_id)

    if order.stock_deducted:
        return

    # Lock all products in the order
    items = list(order.items.select_related("product").all())
    product_ids = [i.product_id for i in items]
    products = {
        p.id: p
        for p in Product.objects.select_for_update().filter(id__in=product_ids)
    }

    # Validate stock
    for item in items:
        p = products[item.product_id]
        if item.qty > p.stock_qty:
            raise ValidationError(
                f"Not enough stock for {
                    p.title}. Requested {
                        item.qty}, available {
                            p.stock_qty}"
            )

    # Deduct using F expressions
    for item in items:
        Product.objects.filter(pk=item.product_id).update(
            stock_qty=F("stock_qty") - item.qty
        )

    order.stock_deducted = True
    order.save(update_fields=["stock_deducted"])
