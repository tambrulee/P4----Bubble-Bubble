from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .models import Product
from django.db.models import Count



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
        {"title":
         "Winter Isles bundle", "text": "Seasonal scents — limited run.",
         "tag": "winter"},
        {"title":
         "Refill & save", "text": "Low-waste favourites with refill options.",
         "tag": "refillable"},
    ]

    testimonials = [
        {"quote":
         "Smells incredible and feels so gentle — my new daily ritual.",
         "name": "Customer"},
        {"quote":
         "Fast delivery, beautiful packaging, and the scent lasts ages.",
         "name": "Customer"},
        {"quote":
         "Finally found a vegan soap that doesn’t dry my skin out.",
         "name": "Customer"},
    ]

    return render(request, "catalog/home.html", {
        "best_sellers": best_sellers,
        "promos": promos,
        "testimonials": testimonials,
        "free_shipping_threshold": 35,
        "LOW_STOCK_THRESHOLD": settings.LOW_STOCK_THRESHOLD,
    })


SCENT_FAMILIES = [
    ("earthy", "Earthy"),
    ("herbal", "Herbal"),
    ("fruity", "Fruity"),
    ("cocoa", "Cocoa"),
    ("coffee", "Coffee"),
    ("honey", "Honey"),
    ("oat", "Oat"),
    ("floral", "Floral"),
]

RANGES = [
    ("winter", "Winter Isles"),
    ("refillable", "Refillables"),
]


def product_list(request):
    range_tag = request.GET.get("range", "").strip().lower()
    scent_family = request.GET.get("scent_family", "").strip().lower()
    price_min = request.GET.get("price_min", "").strip()
    price_max = request.GET.get("price_max", "").strip()
    sort = request.GET.get("sort", "newest").strip().lower()

    qs = Product.objects.filter(active=True)

    # Range filter (tags)
    if range_tag:
        qs = qs.filter(tags__icontains=range_tag)

    # Scent family filter (tags)
    if scent_family:
        qs = qs.filter(tags__icontains=scent_family)

    # Price range
    try:
        if price_min != "":
            qs = qs.filter(price__gte=price_min)
    except ValueError:
        pass

    try:
        if price_max != "":
            qs = qs.filter(price__lte=price_max)
    except ValueError:
        pass

    # Sorting
    if sort == "price_asc":
        qs = qs.order_by("price", "-created_at")
    elif sort == "price_desc":
        qs = qs.order_by("-price", "-created_at")
    elif sort == "popularity":
        # Only use this if you have a related reviews name "reviews".
        # Otherwise fallback to newest.
        try:
            qs = qs.annotate(
                review_count=Count("reviews")).order_by(
                    "-review_count", "-created_at")
        except Exception:
            qs = qs.order_by("-created_at")
    else:
        sort = "newest"
        qs = qs.order_by("-created_at")

    return render(request, "catalog/shop_all.html", {
        "products": qs,
        "LOW_STOCK_THRESHOLD": settings.LOW_STOCK_THRESHOLD,

        "active_range": range_tag,
        "active_scent_family": scent_family,
        "active_price_min": price_min,
        "active_price_max": price_max,
        "active_sort": sort,

        "RANGES": RANGES,
        "SCENT_FAMILIES": SCENT_FAMILIES,
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
    products = Product.objects.filter(
        active=True, tags__icontains="winter").order_by("-created_at")
    return render(request, "catalog/category_page.html", {
        "products": products,
        "LOW_STOCK_THRESHOLD": settings.LOW_STOCK_THRESHOLD,
        "page_title": "Winter Isles",
        "page_description":
        "Limited edition seasonal blends inspired by the "
        "UK landscape — sea air, hedgerow berries, juniper and frost.",
        "hero_image": "img/hero/slide2.png",  # change to your real hero
        "tag": "winter",
    })


def refillables(request):
    products = Product.objects.filter(
        active=True, tags__icontains="refillable").order_by("-created_at")
    return render(request, "catalog/category_page.html", {
        "products": products,
        "LOW_STOCK_THRESHOLD": settings.LOW_STOCK_THRESHOLD,
        "page_title": "Refillable Soaps",
        "page_description":
        "Low-waste favourites designed for everyday rituals — "
        "refill options so you don’t have to keep buying new bottles.",
        "hero_image": "img/hero/slide3.png",  # change to your real hero
        "tag": "refillable",
    })
