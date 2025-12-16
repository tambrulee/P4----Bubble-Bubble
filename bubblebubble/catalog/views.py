from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    products = Product.objects.filter(active=True, stock_qty__gt=0)
    return render(request, "catalog/product_list.html", {
        "products": products,
        "LOW_STOCK_THRESHOLD": settings.LOW_STOCK_THRESHOLD,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, active=True)
    return render(request, "catalog/product_detail.html", {
        "product": product,
        "LOW_STOCK_THRESHOLD": settings.LOW_STOCK_THRESHOLD,
    })
