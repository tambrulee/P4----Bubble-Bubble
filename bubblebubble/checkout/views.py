import stripe
from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponseBadRequest

from cart.utils import get_or_create_cart
from .models import Order, OrderItem
from .forms import CheckoutForm

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY



def checkout_summary(request):
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        return redirect("cart:view")

    # Pre-fill email if user is logged in
    initial = {}
    if request.user.is_authenticated and getattr(request.user, "email", None):
        initial["email"] = request.user.email

    form = CheckoutForm(initial=initial)

    context = {
        "cart": cart,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "form": form,
    }
    return render(request, "checkout/summary.html", context)


def start_checkout(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    cart = get_or_create_cart(request)
    if not cart.items.exists():
        return HttpResponseBadRequest("Cart is empty")

    form = CheckoutForm(request.POST)
    if not form.is_valid():
        # Re-render the summary page with errors
        context = {
            "cart": cart,
            "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
            "form": form,
        }
        return render(request, "checkout/summary.html", context, status=400)

    data = form.cleaned_data
    full_name = data["full_name"]
    email = data["email"]
    address_line1 = data.get("address_line1")
    address_line2 = data.get("address_line2")
    city = data.get("city")
    postcode = data.get("postcode")

    total = Decimal("0.00")

    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        total=Decimal("0.00"),
        full_name=full_name,
        email=email,
        address_line1=address_line1 or "",
        address_line2=address_line2 or "",
        city=city or "",
        postcode=postcode or "",
    )

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

        line_items.append(
            {
                "price_data": {
                    "currency": settings.STRIPE_CURRENCY,
                    "product_data": {"name": p.title},
                    "unit_amount": int(unit_price * 100),
                },
                "quantity": qty,
            }
        )

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
        customer_email=email or (
            getattr(request.user, "email", None)
            if request.user.is_authenticated
            else None
        ),
        metadata={
            "order_id": str(order.id),
            "user_id": str(request.user.id)
            if request.user.is_authenticated
            else "",
        },
    )

    order.stripe_session_id = session.id
    order.save()

    # Send the customer to Stripe Checkout
    return redirect(session.url)



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
    ).first()

    if order and order.status != Order.PAID:
        order.status = Order.PAID
        order.save()

        # clear cart (guest or logged-in: based on session)
        cart = get_or_create_cart(request)
        cart.items.all().delete()

        # send confirmation email
        send_order_confirmation_email(order)

    return render(request, "checkout/success.html", {"order": order})



def checkout_cancel(request):
    return render(request, "checkout/cancel.html")

# --- New function added to send order confirmation email ---
def send_order_confirmation_email(order):
    """
    Send a confirmation email to the customer for the given order.
    Safe to call only once per order.
    """
    if not order.email:
        return  # nothing to send to

    subject = f"Your BubbleBubble order #{order.id}"

    context = {"order": order}
    message = render_to_string("checkout/emails/order_confirmation.txt", context)
    try:
        html_message = render_to_string(
            "checkout/emails/order_confirmation.html", context
        )
    except Exception:
        html_message = None

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
        html_message=html_message,
    )

