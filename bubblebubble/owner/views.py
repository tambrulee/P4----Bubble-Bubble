from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from catalog.models import Product, ProductImage
from checkout.models import Order
from .forms import ProductForm, ProductImageForm
from django.conf import settings
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.views.decorators.http import require_http_methods


@staff_member_required
@require_http_methods(["GET", "POST"])
def owner_login(request):
    # Already logged in
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("owner_dashboard")
        # Logged in but not staff -> boot them out
        logout(request)
        messages.error(request, "Staff access only.")
        return redirect("owner_login")

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)

        if not user.is_staff:
            logout(request)
            messages.error(request, "Staff access only.")
            return redirect("owner_login")

        # Respect ?next=... if present, but keep it inside /owner/
        next_url = request.GET.get("next")
        if next_url and next_url.startswith("/owner/"):
            return redirect(next_url)

        messages.success(request, "Welcome back.")
        return redirect("owner_dashboard")

    return render(request, "owner/login.html", {"form": form})


@staff_member_required
def dashboard(request):
    low_qs = Product.objects.filter(
        active=True,
        stock_qty__lte=settings.LOW_STOCK_THRESHOLD
    ).order_by("stock_qty", "title")

    return render(request, "owner/dashboard.html", {
        "product_count": Product.objects.count(),
        "inactive_count": Product.objects.filter(
            active=False).count(),
        "pending_orders": Order.objects.filter(
            status=Order.PENDING).count(),
        "low_stock_count": low_qs.count(),
        "low_stock": low_qs[:10],
        "LOW_STOCK_THRESHOLD": settings.LOW_STOCK_THRESHOLD,
    })


# ---------- Products ----------
@staff_member_required
def products(request):
    qs = Product.objects.annotate(
        image_count=Count("images")).order_by("title")
    return render(request, "owner/products.html", {
        "products": qs,
        "LOW_STOCK_THRESHOLD": settings.LOW_STOCK_THRESHOLD,
    })


@staff_member_required
def product_create(request):
    form = ProductForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("owner_products")
    return render(
        request, "owner/product_form.html", {
            "form": form, "mode": "Create"})


@staff_member_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("owner_products")
    return render(
        request, "owner/product_form.html", {
            "form": form, "mode": "Edit", "product": product})


@staff_member_required
def product_toggle_active(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.active = not product.active
    product.save(update_fields=["active"])
    return redirect("owner_products")


# ---------- Product images ----------
@staff_member_required
def product_images(request, pk):
    product = get_object_or_404(Product, pk=pk)
    images = product.images.all().order_by("-id")

    form = ProductImageForm(
        request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        img = form.save(commit=False)
        img.product = product
        img.save()
        return redirect("owner_product_images", pk=product.pk)

    return render(request, "owner/product_images.html", {
        "product": product,
        "images": images,
        "form": form,
    })


@staff_member_required
def product_image_delete(request, image_id):
    img = get_object_or_404(ProductImage, pk=image_id)
    product_id = img.product_id
    img.delete()
    return redirect("owner_product_images", pk=product_id)


# ---------- Orders ----------
@staff_member_required
def orders(request):
    tab = request.GET.get("tab", "new")

    base = Order.objects.all().order_by("-created_at")

    if tab == "all":
        qs = base
    elif tab == "new":
        # Paid orders that still need dispatching
        qs = base.filter(
            status=Order.PAID, fulfilment_status=Order.NEW)
    elif tab == "dispatched":
        qs = base.filter(
            status=Order.PAID, fulfilment_status=Order.DISPATCHED)
    elif tab == "delivered":
        qs = base.filter(
            status=Order.PAID, fulfilment_status=Order.DELIVERED)
    elif tab == "abandoned":
        # “Started checkout” orders that never became paid
        qs = base.filter(
            status=Order.PENDING)
    else:
        qs = base

    counts = {
        "all": base.count(),
        "new": base.filter(
            status=Order.PAID, fulfilment_status=Order.NEW).count(),
        "dispatched": base.filter(
            status=Order.PAID, fulfilment_status=Order.DISPATCHED).count(),
        "delivered": base.filter(
            status=Order.PAID, fulfilment_status=Order.DELIVERED).count(),
        "abandoned": base.filter(
            status=Order.PENDING).count(),
    }

    return render(request, "owner/orders.html", {
        "orders": qs,
        "tab": tab,
        "counts": counts,
    })


@staff_member_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, "owner/order_detail.html", {"order": order})


# ---------- Analytics ----------
@staff_member_required
def owner_analytics(request):
    now = timezone.now()
    d7 = now - timedelta(days=7)
    d30 = now - timedelta(days=30)

    paid = Order.objects.filter(status="PAID")

    ctx = {
        "rev_7": paid.filter(
            created_at__gte=d7).aggregate(v=Sum("total"))["v"] or 0,
        "rev_30": paid.filter(
            created_at__gte=d30).aggregate(v=Sum("total"))["v"] or 0,
        "orders_7": paid.filter(
            created_at__gte=d7).count(),
        "orders_30": paid.filter(
            created_at__gte=d30).count(),
        "aov_30": paid.filter(
            created_at__gte=d30).aggregate(v=Avg("total"))["v"] or 0,
        "pending": Order.objects.filter(status="PENDING").count(),
    }
    return render(request, "owner/analytics.html", ctx)


@staff_member_required
@require_POST
def owner_order_set_fulfilment(request, order_id, fulfilment):
    order = get_object_or_404(Order, pk=order_id)

    allowed = {Order.DISPATCHED, Order.DELIVERED, Order.CANCELLED}
    if fulfilment not in allowed:
        return redirect("owner_orders")

    order.fulfilment_status = fulfilment

    # timestamps
    now = timezone.now()
    if fulfilment == Order.DISPATCHED:
        order.dispatched_at = now
    elif fulfilment == Order.DELIVERED:
        order.delivered_at = now
    elif fulfilment == Order.CANCELLED:
        order.cancelled_at = now

    order.save(update_fields=[
        "fulfilment_status",
        "dispatched_at",
        "delivered_at",
        "cancelled_at",
    ])
    return redirect("owner_orders")
