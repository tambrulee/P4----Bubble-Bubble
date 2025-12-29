from django.urls import path
from . import views

urlpatterns = [
    path("owner/", views.dashboard, name="owner_dashboard"),

    path(
        "owner/products/", views.products, name="owner_products"),
    path(
        "owner/products/new/",
        views.product_create, name="owner_product_create"),
    path(
        "owner/products/<int:pk>/edit/",
        views.product_edit, name="owner_product_edit"),
    path(
        "owner/products/<int:pk>/toggle/",
        views.product_toggle_active, name="owner_product_toggle"),
    path(
        "owner/products/<int:pk>/images/",
        views.product_images, name="owner_product_images"),
    path(
        "owner/images/<int:image_id>/delete/",
        views.product_image_delete, name="owner_product_image_delete"),

    path("owner/orders/", views.orders, name="owner_orders"),
    path("owner/orders/<int:order_id>/",
        views.order_detail, name="owner_order_detail"),
        path(
        "orders/<int:order_id>/fulfilment/<str:fulfilment>/",
        views.owner_order_set_fulfilment,
        name="owner_order_set_fulfilment",
    ),
]
