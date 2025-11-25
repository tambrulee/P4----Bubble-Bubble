from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # redirect to login after successful signup
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "accounts/signup.html", {"form": form})
