from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import CartItem
from .utils import get_or_create_cart
from catalog.models import Product
from django.http import JsonResponse
from django.contrib import messages
from django.template.loader import render_to_string


def view_cart(request):
    cart = get_or_create_cart(request)
    return render(request, "cart/view.html", {"cart": cart})


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, active=True)
    cart = get_or_create_cart(request)

    try:
        qty = int(request.POST.get("qty", 1))
    except (TypeError, ValueError):
        qty = 1

    qty = max(1, qty)
    qty = min(qty, product.stock_qty)

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        item.qty = qty
    else:
        item.qty = min(item.qty + qty, product.stock_qty)
    item.save()

    cart_count = sum(i.qty for i in cart.items.all())
    added_msg = f"Added {qty} × {product.title} to your cart."

    is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"
    if is_ajax:
        mini_html = render_to_string("cart/_mini_cart.html", {"cart": cart}, request=request)
        total = cart.total() if callable(getattr(cart, "total", None)) else getattr(cart, "total", 0)

        return JsonResponse({
            "ok": True,
            "message": added_msg,
            "cart_count": cart_count,
            "mini_html": mini_html,
            "cart_total": str(total),
        })

    messages.success(request, added_msg)
    return redirect(request.META.get("HTTP_REFERER", "cart:view"))


@require_POST
def update_item(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)

    try:
        qty = int(request.POST.get("qty", 1))
    except (TypeError, ValueError):
        qty = 1

    qty = max(1, qty)
    qty = min(qty, item.product.stock_qty)

    item.qty = qty
    item.save()
    return redirect("cart:view")


@require_POST
def remove_item(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    item.delete()
    return redirect("cart:view")



def add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    qty = int(request.POST.get("qty", 1))

    cart = get_or_create_cart(request)

    cart_count = sum(i.qty for i in cart.items.all())

    added_msg = f"Added {qty} × {product.title} to your cart."

    is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"

    if is_ajax:
        return JsonResponse({
            "ok": True,
            "message": added_msg,
            "cart_count": cart_count,
            "product_id": product.id,
            "qty_added": qty,
        })

    messages.success(request, added_msg)
    # keep your current behaviour for non-JS users
    return redirect("cart:view")


def mini_cart(request):
    cart = get_or_create_cart(request)
    html = render_to_string("cart/_mini_cart.html", {"cart": cart}, request=request)

    cart_count = sum(i.qty for i in cart.items.all())
    total = cart.total() if callable(getattr(cart, "total", None)) else getattr(cart, "total", 0)

    return JsonResponse({
        "ok": True,
        "html": html,
        "cart_count": cart_count,
        "cart_total": str(total),
    })


@require_POST
def update_item(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)

    try:
        qty = int(request.POST.get("qty", 1))
    except (TypeError, ValueError):
        qty = 1

    qty = max(1, qty)
    qty = min(qty, item.product.stock_qty)

    item.qty = qty
    item.save()

    cart_count = sum(i.qty for i in cart.items.all())

    is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"
    if is_ajax:
        mini_html = render_to_string("cart/_mini_cart.html", {"cart": cart}, request=request)
        return JsonResponse({
            "ok": True,
            "cart_count": cart_count,
            "mini_html": mini_html,
            "message": "Cart updated.",
        })

    return redirect("cart:view")