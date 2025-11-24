from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import CartItem
from .forms import AddToCartForm
from .utils import get_or_create_cart
from catalog.models import Product


def view_cart(request):
    cart = get_or_create_cart(request)
    return render(request, "cart/view.html", {"cart": cart})


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, active=True)
    cart = get_or_create_cart(request)

    form = AddToCartForm(request.POST, max_stock=product.stock_qty)
    if form.is_valid():
        qty = form.cleaned_data["qty"]
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        item.qty = min(item.qty + qty, product.stock_qty)
        item.save()
    return redirect("cart:view")


@require_POST
def update_item(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    try:
        qty = int(request.POST.get("qty", 1))
    except ValueError:
        qty = 1
    qty = max(1, min(qty, item.product.stock_qty))
    item.qty = qty
    item.save()
    return redirect("cart:view")


@require_POST
def remove_item(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    item.delete()
    return redirect("cart:view")
