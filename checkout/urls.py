from django.urls import path
from . import views

app_name = "checkout"

urlpatterns = [
    path("", views.checkout_summary, name="summary"),
    path("start/", views.start_checkout, name="start_checkout"),
    path("success/", views.checkout_success, name="success"),
    path("cancel/", views.checkout_cancel, name="cancel"),
]
