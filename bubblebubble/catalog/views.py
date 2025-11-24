from django.shortcuts import render, get_object_or_404
from django.http import Http404

# TODO: replace this with real Product model once you've added it
FAKE_PRODUCTS = [
    {
        "slug": "lavender-calm",
        "title": "Lavender Calm",
        "scent": "Lavender",
        "weight_g": 200,
        "price": 12.99,
        "type": "Candle",
        "description": "Hand-poured lavender soy candle in a glass jar.",
        "image": "https://placehold.co/400x300?text=Lavender+Calm",
    },
    {
        "slug": "citrus-spark",
        "title": "Citrus Spark",
        "scent": "Citrus",
        "weight_g": 180,
        "price": 11.99,
        "type": "Soap",
        "description": "Refreshing citrus soap bar with shea butter.",
        "image": "https://placehold.co/400x300?text=Citrus+Spark",
    },
]

def product_list(request):
    # later: Product.objects.filter(active=True)
    return render(request, "catalog/product_list.html", {"products": FAKE_PRODUCTS})

def product_detail(request, slug):
    # later: get_object_or_404(Product, slug=slug, active=True)
    for p in FAKE_PRODUCTS:
        if p["slug"] == slug:
            return render(request, "catalog/product_detail.html", {"product": p})
    raise Http404("Product not found")
