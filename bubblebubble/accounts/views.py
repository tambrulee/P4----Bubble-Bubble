from django.shortcuts import render, redirect
from django.contrib.auth import login

from .forms import EmailUserCreationForm


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
