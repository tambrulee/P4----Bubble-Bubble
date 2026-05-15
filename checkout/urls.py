from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "checkout"

urlpatterns = [
    # Step 1: delivery details form (GET/POST)
    path("", views.checkout_details, name="details"),

    # Step 2: summary page
    path("summary/", views.checkout_summary, name="summary"),

    # Step 3: Stripe session creation (POST)
    path("start/", views.create_stripe_session, name="start_checkout"),

    path("success/", views.checkout_success, name="success"),
    path("cancel/", views.checkout_cancel, name="cancel"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
