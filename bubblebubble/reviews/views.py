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

    # Restrict to completed/paid orders (use whatever you consider “completed”)
    if order.status != Order.PAID:
        messages.error(request, "You can only review items from completed orders.")
        return redirect("accounts:order_detail", order_id=order.id)  # adjust URL name if different

    product = get_object_or_404(Product, id=product_id, active=True)

    # Ensure product is in that order
    if not OrderItem.objects.filter(order=order, product=product).exists():
        messages.error(request, "That product isn’t part of this order.")
        return redirect("accounts:order_detail", order_id=order.id)

    review, _ = Review.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={"verified_purchase": True, "order": order},
    )

    # If an existing review existed (created via old route), upgrade it
    review.verified_purchase = True
    if review.order_id is None:
        review.order = order

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            r = form.save(commit=False)
            r.user = request.user
            r.product = product
            r.verified_purchase = True
            r.order = order
            r.save()
            messages.success(request, "Your review has been saved.")
            return redirect("accounts:order_detail", order_id=order.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, "reviews/add_review.html", {
        "product": product,
        "order": order,
        "form": form,
    })
