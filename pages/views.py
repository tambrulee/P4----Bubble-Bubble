from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings

from .forms import ContactForm


def delivery(request):
    return render(request, "pages/delivery.html")


def returns(request):
    return render(request, "pages/returns.html")


def faq(request):
    return render(request, "pages/faq.html")


def terms(request):
    return render(request, "pages/terms.html")


def privacy(request):
    return render(request, "pages/privacy.html")


def cookies(request):
    return render(request, "pages/cookies.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            to_email = getattr(settings, "CONTACT_TO_EMAIL", None) or settings.DEFAULT_FROM_EMAIL

            body = (
                f"New contact form submission from Moon & Moss\n\n"
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Subject: {subject}\n\n"
                f"Message:\n{message}\n"
            )

            EmailMessage(
                subject=f"[Moon & Moss Contact] {subject}",
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[to_email],
                reply_to=[email],
            ).send(fail_silently=False)

            messages.success(request, "Thanks — your message has been sent.")
            return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "pages/contact.html", {"form": form})
