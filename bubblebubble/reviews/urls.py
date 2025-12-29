from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("add/<slug:slug>/", views.add_review, name="add"),
    path(
        "order/<int:order_id>/product/<int:product_id>/",
        views.review_from_order, name="from_order"),
]
