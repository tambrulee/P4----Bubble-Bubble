from import_export import resources
from .models import Product


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        import_id_fields = ('slug',)  # or 'id'
        fields = (
            'title',
            'slug',
            'product_type',
            'description',
            'scent',
            'burn_time_min',
            'weight_g',
            'price',
            'stock_qty',
            'active',
        )
