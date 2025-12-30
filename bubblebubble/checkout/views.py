import stripe
from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseBadRequest
from cart.utils import get_or_create_cart
from .models import Order, OrderItem
from .forms import CheckoutForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .services import deduct_stock_for_order
from accounts.models import ShippingAddress

stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout_summary(request):
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        return redirect("cart:view")

    initial = {}

    if request.user.is_authenticated:
        # email
        if getattr(request.user, "email", None):
            initial["email"] = request.user.email

        # prefill from default saved address (optional but feels great)
        default_addr = (
            ShippingAddress.objects.filter(
                user=request.user, is_default=True).first()
            or ShippingAddress.objects.filter(
                user=request.user).order_by("-created_at").first()
        )
        if default_addr:
            initial.setdefault("full_name", default_addr.full_name)
            initial.setdefault("address_line1", default_addr.address_line1)
            initial.setdefault("address_line2", default_addr.address_line2)
            initial.setdefault("city", default_addr.city)
            initial.setdefault("postcode", default_addr.postcode)

    form = CheckoutForm(initial=initial, user=request.user)

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

    form = CheckoutForm(request.POST, user=request.user)
    if not form.is_valid():
        context = {
            "cart": cart,
            "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
            "form": form,
        }
        return render(request, "checkout/summary.html", context, status=400)

    data = form.cleaned_data

    # base values from form
    full_name = data["full_name"]
    email = data["email"]
    address_line1 = data.get("address_line1") or ""
    address_line2 = data.get("address_line2") or ""
    city = data.get("city") or ""
    postcode = data.get("postcode") or ""

    # if user picked a saved address, overwrite shipping fields with it
    saved = data.get(
        "saved_address") if request.user.is_authenticated else None
    if saved:
        full_name = saved.full_name or full_name
        address_line1 = saved.address_line1
        address_line2 = saved.address_line2 or ""
        city = saved.city
        postcode = saved.postcode

    total = Decimal("0.00")

    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        total=Decimal("0.00"),
        full_name=full_name,
        email=email,
        address_line1=address_line1,
        address_line2=address_line2,
        city=city,
        postcode=postcode,
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
    order.save(update_fields=["total"])

    # Save address if requested and they DIDN'T pick an existing one
    if request.user.is_authenticated and data.get(
            "save_address") and not saved:
        addr, created = ShippingAddress.objects.get_or_create(
            user=request.user,
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            postcode=postcode,
            defaults={"label": "Home", "full_name": full_name},
        )
        # if no default exists, set this as default
        if not ShippingAddress.objects.filter(
                user=request.user, is_default=True).exists():
            addr.is_default = True
            addr.save(update_fields=["is_default"])

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
    order.save(update_fields=["stripe_session_id"])

    return redirect(session.url)


def checkout_success(request):
    session_id = request.GET.get("session_id")
    if not session_id:
        return redirect("catalog:product_list")

    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except Exception:
        return redirect("catalog:product_list")

    order = Order.objects.filter(stripe_session_id=session.id).first()

    if order and order.status != Order.PAID:
        order.status = Order.PAID
        # NEW fulfilment tag
        if hasattr(order, "fulfilment_status") and not order.fulfilment_status:
            order.fulfilment_status = Order.NEW

        # even if it's already set, this keeps it consistent:
        if hasattr(Order, "NEW"):
            order.fulfilment_status = Order.NEW

        order.save(update_fields=["status", "fulfilment_status"])

        deduct_stock_for_order(order.id)

        cart = get_or_create_cart(request)
        cart.items.all().delete()

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

    subject = f"Your BubbleBubble Order #{order.id}"

    context = {"order": order}
    message = render_to_string(
        "checkout/emails/order_confirmation.txt", context)
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
