# cart/signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .models import Cart, CartItem


@receiver(user_logged_in)
def merge_carts_on_login(sender, request, user, **kwargs):
    """
    When a user logs in, merge any existing guest cart (for this session)
    into the user's cart, then delete the guest cart.

    - Guest cart is identified by session_key + user is null.
    - User cart is identified by user.
    """
    session_key = getattr(request.session, "session_key", None)
    if not session_key:
        return

    try:
        guest_cart = Cart.objects.get(session_key=session_key, user__isnull=True)
    except Cart.DoesNotExist:
        # no guest cart for this session → nothing to do
        return

    # Get or create the user's cart
    user_cart, _ = Cart.objects.get_or_create(
        user=user,
        defaults={"session_key": session_key},
    )

    # Merge items
    for guest_item in guest_cart.items.select_related("product"):
        user_item, created = CartItem.objects.get_or_create(
            cart=user_cart,
            product=guest_item.product,
            defaults={"qty": guest_item.qty},
        )
        if not created:
            # we could also respect stock limits here if needed
            user_item.qty += guest_item.qty
            # If you want to honour stock_qty, uncomment:
            # max_qty = guest_item.product.stock_qty
            # user_item.qty = min(user_item.qty, max_qty)
            user_item.save()

    # Remove the guest cart now that it's merged
    guest_cart.delete()
