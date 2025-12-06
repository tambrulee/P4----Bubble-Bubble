from .models import Cart


def get_or_create_cart(request):
    # ensure session key exists
    if not request.session.session_key:
        request.session.create()

    # keep cart around for e.g. 14 days for guests
    request.session.set_expiry(60 * 60 * 24 * 14)

    session_key = request.session.session_key

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(
            user=request.user,
            defaults={"session_key": session_key},
        )
    else:
        cart, _ = Cart.objects.get_or_create(
            user=None,
            session_key=session_key,
        )

    return cart
