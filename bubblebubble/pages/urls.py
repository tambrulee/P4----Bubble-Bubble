from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("contact/", views.contact, name="contact"),
    path("delivery/", views.delivery, name="delivery"),
    path("returns/", views.returns, name="returns"),
    path("faq/", views.faq, name="faq"),
    path("terms/", views.terms, name="terms"),
    path("privacy/", views.privacy, name="privacy"),
    path("cookies/", views.cookies, name="cookies"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)