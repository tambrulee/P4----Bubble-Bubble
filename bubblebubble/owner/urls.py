from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView

app_name = "owner"

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="owner/login.html",
            redirect_authenticated_user=True,
            next_page=reverse_lazy("owner:owner_dashboard"),  # ✅ default redirect
        ),
        name="owner_login",
    ),

    path("login/", views.owner_login, name="owner_login"),

    path("", views.dashboard, name="owner_dashboard"),

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
    path(
        "owner/orders/<int:order_id>/",
        views.order_detail, name="owner_order_detail"),
    path(
        "orders/<int:order_id>/fulfilment/<str:fulfilment>/",
        views.owner_order_set_fulfilment,
        name="owner_order_set_fulfilment",
    ),
     path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="owner/password_reset_form.html",
            email_template_name="owner/password_reset_email.html",
            subject_template_name="owner/password_reset_subject.txt",
            success_url=reverse_lazy("owner:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="owner/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="owner/password_reset_confirm.html",
            success_url=reverse_lazy(
                "owner:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="owner/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
]
