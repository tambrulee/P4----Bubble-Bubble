from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count

from catalog.models import Product, ProductImage
from checkout.models import Order

from .forms import ProductForm, ProductImageForm

from django.conf import settings


@staff_member_required
def dashboard(request):
    low_qs = Product.objects.filter(
        active=True,
        stock_qty__lte=settings.LOW_STOCK_THRESHOLD
    ).order_by("stock_qty", "title")

    return render(request, "owner/dashboard.html", {
        "product_count": Product.objects.count(),
        "inactive_count": Product.objects.filter(active=False).count(),
        "pending_orders": Order.objects.filter(status=Order.PENDING).count(),
        "low_stock_count": low_qs.count(),
        "low_stock": low_qs[:10],
        "LOW_STOCK_THRESHOLD": settings.LOW_STOCK_THRESHOLD,
    })


# ---------- Products ----------
@staff_member_required
def products(request):
    qs = Product.objects.annotate(image_count=Count("images")).order_by("title")
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
    return render(request, "owner/product_form.html", {"form": form, "mode": "Create"})


@staff_member_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("owner_products")
    return render(request, "owner/product_form.html", {"form": form, "mode": "Edit", "product": product})


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

    form = ProductImageForm(request.POST or None, request.FILES or None)
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
    qs = Order.objects.all().order_by("-created_at")
    return render(request, "owner/orders.html", {"orders": qs})


@staff_member_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, "owner/order_detail.html", {"order": order})

