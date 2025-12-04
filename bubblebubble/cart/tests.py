from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from catalog.models import Product
from cart.models import Cart, CartItem


User = get_user_model()


class CartViewQuantityTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="cartuser", password="testpass123"
        )
        self.client.login(username="cartuser", password="testpass123")

        # Create a product
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

        # Create a cart and a cart item with qty=3
        self.cart = Cart.objects.create(user=self.user, session_key="testsession")
        self.item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            qty=3,
        )

    def test_cart_page_displays_item_quantity(self):
        """Cart page should show the item's quantity in the qty input."""
        url = reverse("cart:view")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        # Check the cart in context has the item with the correct qty
        cart = response.context["cart"]
        item = cart.items.first()
        self.assertEqual(item.qty, 3)

        # Check the HTML contains value="3" for the quantity input
        self.assertInHTML(
            '<input type="number" name="qty" value="3"',
            response.content.decode("utf-8")
        )
