from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    #path("admin/", admin.site.urls),
    path("shop_manager/", admin.site.urls),

    # Serve media locally even when DEBUG=False
    path("media/<path:path>", serve, {"document_root": settings.MEDIA_ROOT}),

    # App URLs
    path("", include("catalog.urls")),
    path("cart/", include("cart.urls")),
    path("checkout/", include("checkout.urls")),
    path("reviews/", include("reviews.urls")),
    path("", include("owner.urls")),

    # Auth (login/logout/password reset)
    path("accounts/", include("accounts.urls")),
    
]

# Serve media locally even when DEBUG=False
urlpatterns += [
    path("media/<path:path>", serve, {"document_root": settings.MEDIA_ROOT}),
]
