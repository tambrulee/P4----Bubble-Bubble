from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from catalog.models import Product
from cart.models import Cart

User = get_user_model()


class AddToCartTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="cartuser", password="testpass123"
        )
        self.client.login(username="cartuser", password="testpass123")

        self.product = Product.objects.create(
            title="Test Soap",
            product_type=Product.SOAP,
            description="Test soap desc",
            scent="Lavender",
            weight_g=200,
            price=6.99,
            stock_qty=10,
            active=True,
        )

    def test_first_add_sets_qty_to_requested_amount(self):
        """First add_to_cart should set qty exactly to
        requested value (not default+requested)."""
        url = reverse("cart:add", args=[self.product.id])
        response = self.client.post(url, {"qty": 1}, follow=True)

        self.assertEqual(response.status_code, 200)
        cart = Cart.objects.first()
        item = cart.items.get(product=self.product)
        self.assertEqual(item.qty, 1)

    def test_second_add_increments_quantity(self):
        """Adding the same product again should increment qty."""
        url = reverse("cart:add", args=[self.product.id])

        # first add
        self.client.post(url, {"qty": 1})
        # second add
        self.client.post(url, {"qty": 1})

        cart = Cart.objects.first()
        item = cart.items.get(product=self.product)
        self.assertEqual(item.qty, 2)
