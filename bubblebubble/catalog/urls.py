from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'catalog'

urlpatterns = [
    path("", views.home, name="home"),
    path("shop/", views.product_list, name="product_list"),
    path("winter-isles/", views.winter_isles, name="winter_isles"),
    path("refillables/", views.refillables, name="refillables"),
    path('p/<slug:slug>/', views.product_detail, name='product_detail'),
    path("about/", views.about, name="about"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
