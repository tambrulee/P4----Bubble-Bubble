from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .models import Product

def home(request):
    best_sellers = (
        Product.objects
        .filter(
            active=True,
            tags__icontains="bestseller"
        )
        .order_by("-created_at")[:4]
    )

    promos = [
        {"title": "Winter Isles bundle", "text": "Seasonal scents — limited run.", "tag": "winter"},
        {"title": "Refill & save", "text": "Low-waste favourites with refill options.", "tag": "refillable"},
    ]

    testimonials = [
        {"quote": "Smells incredible and feels so gentle — my new daily ritual.", "name": "Customer"},
        {"quote": "Fast delivery, beautiful packaging, and the scent lasts ages.", "name": "Customer"},
        {"quote": "Finally found a vegan soap that doesn’t dry my skin out.", "name": "Customer"},
    ]

    return render(request, "catalog/home.html", {
        "best_sellers": best_sellers,
        "promos": promos,
        "testimonials": testimonials,
        "free_shipping_threshold": 35,
        "LOW_STOCK_THRESHOLD": settings.LOW_STOCK_THRESHOLD,
    })

def product_list(request):
    tag = request.GET.get("tag")

    products = Product.objects.filter(active=True)

    if tag:
        products = products.filter(tags__icontains=tag)

    products = products.order_by("-created_at")

    return render(request, "catalog/shop_all.html", {
        "products": products,
        "active_tag": tag,
        "LOW_STOCK_THRESHOLD": settings.LOW_STOCK_THRESHOLD,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, active=True)
    return render(request, "catalog/product_detail.html", {
        "product": product,
        "LOW_STOCK_THRESHOLD": settings.LOW_STOCK_THRESHOLD,
    })

def about(request):
    return render(request, "catalog/about.html")

def winter_isles(request):
    products = Product.objects.filter(active=True, tags__icontains="winter").order_by("-created_at")
    return render(request, "catalog/category_page.html", {
        "products": products,
        "LOW_STOCK_THRESHOLD": settings.LOW_STOCK_THRESHOLD,
        "page_title": "Winter Isles",
        "page_description": "Limited edition seasonal blends inspired by the UK landscape — sea air, hedgerow berries, juniper and frost.",
        "hero_image": "img/hero/slide2.png",  # change to your real hero
        "tag": "winter",
    })

def refillables(request):
    products = Product.objects.filter(active=True, tags__icontains="refillable").order_by("-created_at")
    return render(request, "catalog/category_page.html", {
        "products": products,
        "LOW_STOCK_THRESHOLD": settings.LOW_STOCK_THRESHOLD,
        "page_title": "Refillable Soaps",
        "page_description": "Low-waste favourites designed for everyday rituals — refill options so you don’t have to keep buying new bottles.",
        "hero_image": "img/hero/slide3.png",  # change to your real hero
        "tag": "refillable",
    })