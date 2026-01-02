from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path("", views.home, name="home"),
    path("shop/", views.product_list, name="product_list"),
    path("winter-isles/", views.winter_isles, name="winter_isles"),
    path("refillables/", views.refillables, name="refillables"),
    path('p/<slug:slug>/', views.product_detail, name='product_detail'),
    path("about/", views.about, name="about"),

    # Legal and contact pages

    path("delivery/", views.delivery, name="delivery"),
    path("returns/", views.returns, name="returns"),
    path("faq/", views.faq, name="faq"),
    path("terms/", views.terms, name="terms"),
    path("privacy/", views.privacy, name="privacy"),
    path("cookies/", views.cookies, name="cookies"),
    path("contact/", views.contact, name="contact"),
]
