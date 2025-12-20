from .utils import get_or_create_cart

def cart_count(request):
    cart = get_or_create_cart(request)
    try:
        count = sum(i.qty for i in cart.items.all())
    except Exception:
        count = 0
    return {"cart_count": count}
