from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import reverse
from django.core import mail

from catalog.models import Product
from cart.models import Cart, CartItem
from checkout.models import Order, OrderItem


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="noreply@bubblebubble.test",
)
class CheckoutSuccessEmailTests(TestCase):
    def setUp(self):
        # simple product
        self.product = Product.objects.create(
            title="Lavender Candle",
            product_type=Product.CANDLE,
            description="Test candle",
            scent="Lavender",
            weight_g=200,
            price=Decimal("12.50"),
            stock_qty=10,
            active=True,
        )

        # create a cart tied to the client session
        session = self.client.session
        session.save()
        self.session_key = session.session_key

        self.cart = Cart.objects.create(session_key=self.session_key)
        CartItem.objects.create(cart=self.cart, product=self.product, qty=2)

        # matching order for the Stripe session
        self.order = Order.objects.create(
            user=None,
            status=Order.PENDING,
            total=Decimal("25.00"),
            stripe_session_id="cs_test_123",
            full_name="Test Customer",
            email="customer@example.com",
        )

        # 🔹 Add an OrderItem so it appears in the confirmation email
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            qty=2,
            unit_price=Decimal("12.50"),
        )


    @patch("checkout.views.stripe.checkout.Session.retrieve")
    def test_checkout_success_marks_order_paid_clears_cart_and_sends_email(
        self, mock_retrieve
    ):
        """
        Given a valid Stripe session and pending order,
        when the success view is called,
        then the order is marked paid, cart is cleared,
        and a confirmation email is sent to the customer.
        """
        mock_retrieve.return_value = SimpleNamespace(id="cs_test_123")

        url = reverse("checkout:success") + "?session_id=cs_test_123"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        # Order marked as PAID
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, Order.PAID)

        # Cart cleared
        self.assertEqual(self.cart.items.count(), 0)

        # One email sent
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.to, ["customer@example.com"])
        self.assertIn("Order", email.subject)
        self.assertIn("Lavender Candle", email.body)
        self.assertIn("£25.00", email.body)

    @patch("checkout.views.stripe.checkout.Session.retrieve")
    def test_checkout_success_does_not_send_email_if_order_already_paid(
        self, mock_retrieve
    ):
        """
        If the order is already marked as PAID,
        we shouldn't send a second email.
        """
        self.order.status = Order.PAID
        self.order.save()

        mock_retrieve.return_value = SimpleNamespace(id="cs_test_123")

        url = reverse("checkout:success") + "?session_id=cs_test_123"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        # No new emails
        self.assertEqual(len(mail.outbox), 0)
