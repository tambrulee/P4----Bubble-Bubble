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
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.db.models import Prefetch
from django.db.models import Q
from reviews.models import Review
from .forms import OwnerReplyForm
from django.core.paginator import Paginator



# ---------- Owner login ----------


@require_http_methods(["GET", "POST"])
def owner_login(request):
    """Handle owner/staff login with redirection and access control."""
    # Already logged in
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("owner:owner_dashboard")

        # Logged in but not staff → hard reset
        request.session.flush()
        messages.error(request, "Staff access only.")
        return redirect("owner:owner_login")

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()

        # BLOCK NON-STAFF — DO NOT LOG THEM IN
        if not user.is_staff:
            messages.error(request, "This account does not have admin access.")
            return redirect("owner:owner_login")

        auth_login(request, user)

        next_url = request.POST.get("next") or request.GET.get("next")
        if next_url and next_url.startswith("/owner/"):
            return redirect(next_url)

        messages.success(request, "Welcome back.")
        return redirect("owner:owner_dashboard")

    return render(
        request,
        "owner/login.html",
        {
            "form": form,
            "next": request.GET.get("next", ""),
        },
    )


# ---------- Dashboard ----------


@staff_member_required
def dashboard(request):
    """Display the owner dashboard with key metrics."""
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


# ---------- Orders ----------


@staff_member_required
def orders(request):
    """Display the list of orders with filtering by fulfilment status."""
    tab = request.GET.get("tab", "new")

    base = Order.objects.all().order_by("-created_at")

    if tab == "all":
        qs = base.filter(
            status=Order.PAID,
            fulfilment_status__in=[
                    Order.DELIVERED,
                    Order.DISPATCHED,
                    Order.NEW,],)
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
    else:
        qs = base

    counts = {
        "all": base.filter(
            status=Order.PAID,
            fulfilment_status__in=[
                Order.DELIVERED, Order.DISPATCHED, Order.NEW,]).count(),
        "new": base.filter(
            status=Order.PAID, fulfilment_status=Order.NEW).count(),
        "dispatched": base.filter(
            status=Order.PAID, fulfilment_status=Order.DISPATCHED).count(),
        "delivered": base.filter(
            status=Order.PAID, fulfilment_status=Order.DELIVERED).count(),
    }

    paginator = Paginator(qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "owner/orders.html", {
    "orders": page_obj,
    "page_obj": page_obj,
    "paginator": paginator,
    "tab": tab,
    "counts": counts,
})



@staff_member_required
def order_detail(request, order_id):
    """Display the detail page for a specific order."""
    order = get_object_or_404(Order, pk=order_id)
    return render(request, "owner/order_detail.html", {"order": order})


# ---------- Analytics ----------
@staff_member_required
def owner_analytics(request):
    """Display sales analytics for the owner dashboard."""
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


# ---------- Owner product list with filters ----------
@staff_member_required
@require_POST
def owner_order_set_fulfilment(request, order_id, fulfilment):
    """Set the fulfilment status of an order."""
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
    return redirect("owner:owner_orders")


@login_required
@staff_member_required
def products(request):
    """Display the owner product list with filtering and sorting."""
    # --- GET params (must match template name="...") ---
    active_status = request.GET.get("status", "").strip().lower()
    active_tag = request.GET.get("tag", "").strip().lower()
    active_stock = request.GET.get("stock", "").strip().lower()
    active_sort = request.GET.get("sort", "title").strip().lower()

    low_threshold = getattr(settings, "LOW_STOCK_THRESHOLD", 5)

    qs = Product.objects.all()

    # --- Filters ---
    if active_status == "active":
        qs = qs.filter(active=True)
    elif active_status == "hidden":
        qs = qs.filter(active=False)

    if active_tag:
        qs = qs.filter(tags__icontains=active_tag)

    if active_stock == "out":
        qs = qs.filter(stock_qty=0)
    elif active_stock == "low":
        qs = qs.filter(stock_qty__gt=0, stock_qty__lte=low_threshold)
    elif active_stock == "in":
        qs = qs.filter(stock_qty__gt=low_threshold)

    # --- Sorting ---
    sort_map = {
        "title": ["title"],
        "newest": ["-created_at", "title"],
        "price_asc": ["price", "title"],
        "price_desc": ["-price", "title"],
        "stock_asc": ["stock_qty", "title"],
        "stock_desc": ["-stock_qty", "title"],
    }
    if active_sort not in sort_map:
        active_sort = "title"
    qs = qs.order_by(*sort_map[active_sort])

    # --- Counts for template ---
    qs = qs.annotate(image_count=Count("images", distinct=True))

    # Prefetch images for each product
    qs = qs.prefetch_related(
        Prefetch("images", queryset=ProductImage.objects.order_by("-id"))
    )

    # --- Build tag dropdown from DB ---
    raw_tags = Product.objects.exclude(tags="").values_list("tags", flat=True)
    tag_options = sorted({
        t.strip().lower()
        for row in raw_tags
        for t in row.split(",")
        if t.strip()
    })

    # --- Pagination ---
    paginator = Paginator(qs, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)


    return render(request, "owner/products.html", {
    "products": page_obj,
    "page_obj": page_obj,
    "paginator": paginator,

    "LOW_STOCK_THRESHOLD": low_threshold,
    "active_status": active_status,
    "active_tag": active_tag,
    "active_stock": active_stock,
    "active_sort": active_sort,
    "tag_options": tag_options,
    "debug_qs": request.GET.urlencode(),
})



# ---------- Product create / edit / toggle active ----------


@staff_member_required
def product_create(request):
    """Create a new product."""
    form = ProductForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("owner_products")
    return render(
        request, "owner/product_form.html", {
            "form": form, "mode": "Create"})


@staff_member_required
def product_edit(request, pk):
    """Edit an existing product."""
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("owner:owner_products")
    return render(
        request, "owner/product_form.html", {
            "form": form, "mode": "Edit", "product": product})


@staff_member_required
def product_toggle_active(request, pk):
    """Toggle a product's active status."""
    product = get_object_or_404(Product, pk=pk)
    product.active = not product.active
    product.save(update_fields=["active"])
    return redirect("owner:owner_products")


# ---------- Product images ----------
@staff_member_required
def product_images(request, pk):
    """Manage images for a specific product."""
    product = get_object_or_404(Product, pk=pk)
    images = product.images.all().order_by("-id")

    form = ProductImageForm(
        request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        img = form.save(commit=False)
        img.product = product
        img.save()
        return redirect("owner:owner_product_images", pk=product.pk)

    return render(request, "owner/product_images.html", {
        "product": product,
        "images": images,
        "form": form,
    })


@staff_member_required
def product_image_delete(request, image_id):
    """Delete a product image."""
    img = get_object_or_404(ProductImage, pk=image_id)
    product_id = img.product_id
    img.delete()
    return redirect("owner:owner_product_images", pk=product_id)


# --------- Duplicate product ----------


@login_required
def product_duplicate(request, pk):
    """Duplicate a product."""
    original = get_object_or_404(Product, pk=pk)

    # Create a new product (slug handled automatically in save())
    duplicate = Product.objects.create(
        title=f"{original.title} (Copy)",
        description=original.description,
        scent=original.scent,
        weight_g=original.weight_g,
        price=original.price,
        stock_qty=0,          # reset stock
        active=False,         # safer default
        tags=original.tags,
    )

    return redirect("owner:owner_product_edit", pk=duplicate.pk)


# --------- Bulk actions ----------


@staff_member_required
@require_POST
def products_bulk_action(request):
    """Perform bulk actions on selected products."""
    action = request.POST.get("action")
    ids = request.POST.getlist("product_ids")

    if not ids:
        messages.error(request, "Select at least one product first.")
        return redirect("owner:owner_products")

    qs = Product.objects.filter(pk__in=ids)

    if action == "activate":
        updated = qs.update(active=True)
        messages.success(request, f"Activated {updated} product(s).")
        return redirect("owner:owner_products")

    if action == "hide":
        updated = qs.update(active=False)
        messages.success(request, f"Hidden {updated} product(s).")
        return redirect("owner:owner_products")

    if action == "delete":
        count = qs.count()
        qs.delete()
        messages.success(request, f"Deleted {count} product(s).")
        return redirect("owner:owner_products")

    messages.error(request, "Unknown action.")
    return redirect("owner:owner_products")

# ---------- Reviews management ----------


LOW_RATING_THRESHOLD = 2  # 1–2 stars highlighted


@staff_member_required
def owner_reviews(request):
    """Display and filter product reviews for the owner."""
    qs = Review.objects.select_related("product", "user").order_by("-created_at")

    status = request.GET.get("status", "all")
    if status == "pending":
        qs = qs.filter(is_approved=False)
    elif status == "low":
        qs = qs.filter(rating__lte=LOW_RATING_THRESHOLD)
    elif status == "unreplied":
        qs = qs.filter(Q(owner_reply="") | Q(owner_reply__isnull=True))

    paginator = Paginator(qs, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "owner/reviews.html", {
    "reviews": page_obj,
    "page_obj": page_obj,
    "paginator": paginator,
    "status": status,
    "low_threshold": LOW_RATING_THRESHOLD,
})



@staff_member_required
def owner_review_detail(request, pk):
    """View and reply to a specific product review."""
    review = get_object_or_404(Review.objects.select_related("product", "user"), pk=pk)

    if request.method == "POST":
        form = OwnerReplyForm(request.POST, instance=review)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner_replied_at = timezone.now()
            obj.save(update_fields=["owner_reply", "owner_replied_at", "updated_at"])
            messages.success(request, "Reply saved.")
            return redirect("owner:owner_review_detail", pk=review.pk)
    else:
        form = OwnerReplyForm(instance=review)

    return render(request, "owner/review_detail.html", {
        "review": review,
        "form": form,
        "is_low_rated": review.rating <= LOW_RATING_THRESHOLD,
        "low_threshold": LOW_RATING_THRESHOLD,
    })


@staff_member_required
def owner_review_approve(request, pk):
    """Approve a product review."""
    review = get_object_or_404(Review, pk=pk)
    review.is_approved = True
    review.save(update_fields=["is_approved", "updated_at"])
    messages.success(request, "Review approved (visible on product page).")
    return redirect(request.META.get("HTTP_REFERER", "owner:owner_reviews"))


@staff_member_required
def owner_review_hide(request, pk):
    """Hide a product review."""
    review = get_object_or_404(Review, pk=pk)
    review.is_approved = False
    review.save(update_fields=["is_approved", "updated_at"])
    messages.warning(request, "Review hidden (not visible on product page).")
    return redirect(request.META.get("HTTP_REFERER", "owner:owner_reviews"))
