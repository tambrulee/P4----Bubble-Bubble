from .models import Cart

def get_or_create_cart(request):
    """Retrieve or create a cart for the current user or session."""
    if not request.session.session_key:
        request.session.create()

    request.session.set_expiry(60 * 60 * 24 * 14)
    session_key = request.session.session_key

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user,
            defaults={"session_key": session_key},
        )
        # if cart already existed, make sure session_key isn't blank/None
        if not cart.session_key:
            cart.session_key = session_key
            cart.save(update_fields=["session_key"])
        return cart

    cart, _ = Cart.objects.get_or_create(user=None, session_key=session_key)
    return cart
