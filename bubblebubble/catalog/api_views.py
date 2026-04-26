from django.http import JsonResponse
from .models import Product


def products_api(request):
    products = Product.objects.filter(active=True).order_by("-created_at").prefetch_related("images")

    data = [
        {
            "id": product.id,
            "name": product.title,
            "description": product.description,
            "scent": product.scent,
            "weight_g": product.weight_g,
            "price": float(product.price),
            "stock_qty": product.stock_qty,
            "slug": product.slug,
            "tags": [tag.strip() for tag in product.tags.split(",") if tag.strip()],
            "images": [
                {
                    "url": image.image.url,
                    "alt_text": image.alt_text,
                }
                for image in product.images.all()
            ],
        }
        for product in products
    ]

    return JsonResponse(data, safe=False)