import stripe
from decimal import Decimal

from django.conf import settings
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_POST

from cart.utils import get_or_create_cart
from accounts.models import ShippingAddress

from .models import Order, OrderItem
from .forms import CheckoutForm
from .services import deduct_stock_for_order

from django.core.mail import send_mail
from django.template.loader import render_to_string


stripe.api_key = settings.STRIPE_SECRET_KEY

CHECKOUT_SESSION_KEY = "checkout_data"


# ----------------------------
# Step 1: Delivery details page
# ----------------------------
@require_http_methods(["GET", "POST"])
def checkout_details(request):
    """
    Collect delivery details and validate them.
    On success, store cleaned data in session and redirect to summary page.
    """
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        return redirect("cart:view")

    initial = {}

    if request.user.is_authenticated:
        if getattr(request.user, "email", None):
            initial["email"] = request.user.email

        default_addr = (
            ShippingAddress.objects.filter(user=request.user, is_default=True).first()
            or ShippingAddress.objects.filter(user=request.user).order_by("-created_at").first()
        )
        if default_addr:
            initial.setdefault("full_name", default_addr.full_name)
            initial.setdefault("address_line1", default_addr.address_line1)
            initial.setdefault("address_line2", default_addr.address_line2)
            initial.setdefault("city", default_addr.city)
            initial.setdefault("postcode", default_addr.postcode)

    if request.method == "POST":
        form = CheckoutForm(request.POST, user=request.user)
        if form.is_valid():
            request.session[CHECKOUT_SESSION_KEY] = form.cleaned_data
            request.session.modified = True
            return redirect("checkout:summary")
    else:
        form = CheckoutForm(initial=initial, user=request.user)

    return render(request, "checkout/summary.html", {
        "cart": cart,
        "form": form,
    })


# ----------------------------
# Step 2: Summary page (no Stripe yet)
# ----------------------------
def checkout_summary(request):
    """
    Display checkout summary using validated session data.
    If no session data exists, redirect back to details page.
    """
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        return redirect("cart:view")

    data = request.session.get(CHECKOUT_SESSION_KEY)
    if not data:
        return redirect("checkout:details")

    # Build a form instance for display (no POST here)
    form = CheckoutForm(initial=data, user=request.user)

    return render(request, "checkout/summary.html", {
        "cart": cart,
        "form": form,
        "checkout_data": data,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
    })


# ----------------------------
# Create Stripe session (only when clicking Pay)
# ----------------------------
@require_POST
def create_stripe_session(request):
    """
    Create the Order + Stripe Checkout Session.
    Requires validated checkout data stored in session.
    """
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        return HttpResponseBadRequest("Cart is empty")

    form = CheckoutForm(request.POST, user=request.user)
    if not form.is_valid():
        return render(request, "checkout/checkout.html", {
            "cart": cart,
            "form": form,
        }, status=400)

    data = form.cleaned_data

    if not form.is_valid():
        # If somehow invalid, send them back to details with errors
        return render(request, "checkout/summary.html", {
            "cart": cart,
            "form": form,
        }, status=400)

    data = form.cleaned_data

    full_name = data["full_name"]
    email = data["email"]
    address_line1 = data.get("address_line1") or ""
    address_line2 = data.get("address_line2") or ""
    city = data.get("city") or ""
    postcode = data.get("postcode") or ""

    saved = data.get("saved_address") if request.user.is_authenticated else None
    if saved:
        full_name = saved.full_name or full_name
        address_line1 = saved.address_line1
        address_line2 = saved.address_line2 or ""
        city = saved.city
        postcode = saved.postcode

    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        status=Order.PENDING if hasattr(Order, "PENDING") else "PENDING",
        total=Decimal("0.00"),
        full_name=full_name,
        email=email,
        address_line1=address_line1,
        address_line2=address_line2,
        city=city,
        postcode=postcode,
    )

    total = Decimal("0.00")
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
                "product_data": {"name": p.title},
                "unit_amount": int(unit_price * 100),
            },
            "quantity": qty,
        })

    order.total = total
    order.save(update_fields=["total"])

    # Save address if requested and they DIDN'T pick an existing one
    if request.user.is_authenticated and data.get("save_address") and not saved:
        addr, _ = ShippingAddress.objects.get_or_create(
            user=request.user,
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            postcode=postcode,
            defaults={"label": "Home", "full_name": full_name},
        )
        if not ShippingAddress.objects.filter(user=request.user, is_default=True).exists():
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
            getattr(request.user, "email", None) if request.user.is_authenticated else None
        ),
        metadata={
            "order_id": str(order.id),
            "user_id": str(request.user.id) if request.user.is_authenticated else "",
        },
    )

    order.stripe_session_id = session.id
    order.save(update_fields=["stripe_session_id"])

    return redirect(session.url)


# ----------------------------
# Success + Cancel
# ----------------------------
def checkout_success(request):
    """Handle successful checkout and display order summary."""
    session_id = request.GET.get("session_id")
    if not session_id:
        return redirect("catalog:product_list")

    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except Exception:
        return redirect("catalog:product_list")

    order = Order.objects.filter(stripe_session_id=session.id).first()
    if not order:
        return redirect("catalog:product_list")

    order_items = (
        OrderItem.objects
        .filter(order=order)
        .select_related("product")
    )

    if order.status != Order.PAID:
        order.status = Order.PAID

        update_fields = ["status"]
        if hasattr(order, "fulfilment_status") and hasattr(Order, "NEW"):
            order.fulfilment_status = Order.NEW
            update_fields.append("fulfilment_status")

        order.save(update_fields=update_fields)

        deduct_stock_for_order(order.id)

        cart = get_or_create_cart(request)
        cart.items.all().delete()

        # clear session checkout data so refresh doesn't recreate flows
        request.session.pop(CHECKOUT_SESSION_KEY, None)

        send_order_confirmation_email(order)

    return render(request, "checkout/success.html", {
        "order": order,
        "order_items": order_items
    })


def checkout_cancel(request):
    """Display the checkout cancellation page."""
    return render(request, "checkout/cancel.html")


def send_order_confirmation_email(order):
    """Send a confirmation email to the customer for the given order."""
    if not order.email:
        return

    subject = f"Your BubbleBubble Order #{order.id}"
    context = {"order": order}

    message = render_to_string("checkout/emails/order_confirmation.txt", context)
    try:
        html_message = render_to_string("checkout/emails/order_confirmation.html", context)
    except Exception:
        html_message = None

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
        html_message=html_message,
    )
