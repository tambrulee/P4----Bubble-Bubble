from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import EmailUserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from checkout.models import Order
from django.db import transaction
from .forms import ShippingAddressForm
from .models import ShippingAddress
from django.contrib import messages


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


@login_required
def address_list(request):
    addresses = ShippingAddress.objects.filter(user=request.user).order_by("-is_default", "-created_at")
    return render(request, "accounts/address_list.html", {"addresses": addresses})


@login_required
@transaction.atomic
def address_set_default(request, pk):
    addr = get_object_or_404(ShippingAddress, pk=pk, user=request.user)
    ShippingAddress.objects.filter(user=request.user, is_default=True).update(is_default=False)
    addr.is_default = True
    addr.save(update_fields=["is_default"])
    return redirect("accounts:address_list")


@login_required
def address_create(request):
    if request.method == "POST":
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            addr = form.save(commit=False)
            addr.user = request.user

            if addr.is_default:
                ShippingAddress.objects.filter(user=request.user, is_default=True).update(is_default=False)

            addr.save()
            messages.success(request, "Address saved.")
            return redirect("accounts:address_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ShippingAddressForm()

    return render(request, "accounts/address_form.html", {"form": form, "title": "Add address"})


@login_required
def address_update(request, pk):
    addr = get_object_or_404(ShippingAddress, pk=pk, user=request.user)

    if request.method == "POST":
        form = ShippingAddressForm(request.POST, instance=addr)
        if form.is_valid():
            addr = form.save(commit=False)

            if addr.is_default:
                ShippingAddress.objects.filter(user=request.user, is_default=True).exclude(pk=addr.pk).update(is_default=False)

            addr.save()
            messages.success(request, "Address updated.")
            return redirect("accounts:address_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ShippingAddressForm(instance=addr)

    return render(request, "accounts/address_form.html", {"form": form, "title": "Edit address"})

    addr = get_object_or_404(ShippingAddress, pk=pk, user=request.user)

    if request.method == "POST":
        form = ShippingAddressForm(request.POST, instance=addr)
        if form.is_valid():
            addr = form.save(commit=False)

            if addr.is_default:
                ShippingAddress.objects.filter(user=request.user, is_default=True).exclude(pk=addr.pk).update(is_default=False)

            addr.save()
            return redirect("accounts:address_list")
    else:
        form = ShippingAddressForm(instance=addr)

    return render(request, "accounts/address_form.html", {"form": form, "title": "Edit address"})


@login_required
def address_delete(request, pk):
    addr = get_object_or_404(ShippingAddress, pk=pk, user=request.user)

    if request.method == "POST":
        addr.delete()
        return redirect("accounts:address_list")

    return render(request, "accounts/address_confirm_delete.html", {"address": addr})
