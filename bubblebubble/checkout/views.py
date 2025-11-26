import stripe
from decimal import Decimal
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponseBadRequest
from cart.utils import get_or_create_cart
from .models import Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout_summary(request):
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        return redirect("cart:view")
    context = {
        "cart": cart,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, "checkout/summary.html", context)


@login_required
def start_checkout(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    cart = get_or_create_cart(request)
    if not cart.items.exists():
        return HttpResponseBadRequest("Cart is empty")

    # Build order
    total = Decimal("0.00")
    order = Order.objects.create(user=request.user, total=Decimal("0.00"))

    line_items = []
    for item in cart.items.select_related("product"):
        p = item.product
        unit_price = p.price
        qty = item.qty
        total += unit_price * qty

        OrderItem.objects.create(
            order=order,
            product=p,
            qty=qty,
            unit_price=unit_price,
        )

        line_items.append({
            "price_data": {
                "currency": settings.STRIPE_CURRENCY,
                "product_data": {
                    "name": p.title,
                },
                "unit_amount": int(unit_price * 100),  # decimal -> pennies
            },
            "quantity": qty,
        })

    order.total = total
    order.save()

    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=line_items,
        success_url=request.build_absolute_uri(
            reverse("checkout:success")
        ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse("checkout:summary")),
        customer_email=request.user.email or None,
        metadata={
            "order_id": str(order.id),
            "user_id": str(request.user.id),
        },
    )

    order.stripe_session_id = session.id
    order.save()

    return JsonResponse({"sessionId": session.id})


@login_required
def checkout_success(request):
    session_id = request.GET.get("session_id")
    if not session_id:
        return redirect("catalog:product_list")

    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except Exception:
        return redirect("catalog:product_list")

    order = Order.objects.filter(
        stripe_session_id=session.id,
        user=request.user
    ).first()

    if order and order.status != Order.PAID:
        order.status = Order.PAID
        order.save()
        # clear cart
        cart = get_or_create_cart(request)
        cart.items.all().delete()

    return render(request, "checkout/success.html", {"order": order})


@login_required
def checkout_cancel(request):
    return render(request, "checkout/cancel.html")
