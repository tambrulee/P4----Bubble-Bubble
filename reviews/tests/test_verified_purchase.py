from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from catalog.models import Product
from checkout.models import Order, OrderItem
from reviews.models import Review

User = get_user_model()


class VerifiedPurchaseTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="u1", password="pass12345")

        self.product = Product.objects.create(
            title="Test Soap",
            slug="test-soap",
            description="",
            scent="Lavender",
            weight_g=100,
            price="5.00",
            stock_qty=10,
            active=True,
            tags="",  # if tags is not blankable, keep this
        )

        self.order = Order.objects.create(
            user=self.user,
            full_name="Test User",
            email="u1@example.com",
            address_line1="1 Street",
            city="Sheffield",
            postcode="S1 1AA",
            status=Order.PAID,
            fulfilment_status=Order.DELIVERED,
            total="5.00",
        )

        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            qty=1,
            unit_price="5.00",
        )

    def test_review_from_order_sets_verified_purchase_true(self):
        self.client.login(username="u1", password="pass12345")
        url = reverse(
            "reviews:from_order", args=[self.order.id, self.product.id])

        resp = self.client.post(
            url, data={"rating": 5, "comment": "Great!"})
        self.assertEqual(resp.status_code, 302)

        r = Review.objects.get(user=self.user, product=self.product)
        self.assertTrue(r.verified_purchase)
