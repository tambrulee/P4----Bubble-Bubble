from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import EmailUserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from checkout.models import Order

def signup(request):
    next_url = request.GET.get("next") or "catalog:product_list"

    if request.method == "POST":
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(next_url)
    else:
        form = EmailUserCreationForm()

    return render(request, "accounts/signup.html", {"form": form})


@login_required
def my_orders(request):
    orders = (
        Order.objects
        .filter(user=request.user, status=Order.PAID)
        .order_by("-created_at")
    )
    return render(request, "accounts/my_orders.html", {"orders": orders})


@login_required
def my_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "accounts/my_order_detail.html", {"order": order})
