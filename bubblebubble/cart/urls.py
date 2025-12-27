from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.view_cart, name="view"),
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("update/<int:item_id>/", views.update_item, name="update"),
    path("remove/<int:item_id>/", views.remove_item, name="remove"),
    path("mini/", views.mini_cart, name="mini"),
]
