from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from catalog.models import Product
from checkout.models import OrderItem, Order
from .forms import ReviewForm
from .models import Review

@login_required
def add_review(request, slug):
    product = get_object_or_404(Product, slug=slug, active=True)

    # Check if user has a PAID order containing this product
    has_purchased = OrderItem.objects.filter(
        order__user=request.user,
        order__status=Order.PAID,
        product=product,
    ).exists()

    if not has_purchased:
        messages.error(request, "You can only review products you have purchased.")
        return redirect("catalog:product_detail", slug=slug)

    try:
        existing = Review.objects.get(user=request.user, product=product)
    except Review.DoesNotExist:
        existing = None

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=existing)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(request, "Your review has been saved.")
            return redirect("catalog:product_detail", slug=slug)
    else:
        form = ReviewForm(instance=existing)

    return render(request, "reviews/add_review.html", {"product": product, "form": form})

@login_required
def review_from_order(request, order_id, product_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.fulfilment_status != Order.DELIVERED:
        messages.error(request, "You can only review items after delivery.")
        return redirect("accounts:my_order_detail", order.id)

    product = get_object_or_404(Product, id=product_id, active=True)

    if not OrderItem.objects.filter(order=order, product=product).exists():
        messages.error(request, "That product isn’t part of this order.")
        return redirect("accounts:my_order_detail", order.id)

    existing = Review.objects.filter(user=request.user, product=product).first()

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=existing)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.verified_purchase = True
            # only if you added this field:
            if hasattr(review, "order_id"):
                review.order = order
            review.save()
            messages.success(request, "Your review has been saved.")
            return redirect("accounts:my_order_detail", order.id)
    else:
        form = ReviewForm(instance=existing)

    return render(request, "reviews/add_review.html", {
        "product": product,
        "order": order,
        "form": form,
    })