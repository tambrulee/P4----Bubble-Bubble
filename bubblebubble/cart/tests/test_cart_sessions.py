# cart/tests/test_cart_sessions.py
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in

from cart.models import Cart, CartItem
from cart.utils import get_or_create_cart
from catalog.models import Product


User = get_user_model()


class CartSessionTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="alice", email="alice@example.com", password="secret"
        )
        self.product = Product.objects.create(
            title="Test Product",
            product_type=Product.CANDLE,   # or Product.SOAP, doesn’t matter
            description="Test description",
            scent="Lavender",
            weight_g=200,
            price="10.00",                 # string is fine for DecimalField
            stock_qty=10,
            active=True,
        )

    def _get_request(self, user=None):
        """
        Helper to build a request with a working session.
        """
        request = self.factory.get("/")
        # attach a session the way middleware would
        from django.contrib.sessions.middleware import SessionMiddleware

        middleware = SessionMiddleware(lambda x: x)
        middleware.process_request(request)
        request.session.save()

        if user:
            request.user = user
        else:
            from django.contrib.auth.models import AnonymousUser
            request.user = AnonymousUser()

        return request

    def test_get_or_create_cart_creates_guest_cart(self):
        request = self._get_request()
        cart = get_or_create_cart(request)

        self.assertIsNotNone(cart.pk)
        self.assertIsNone(cart.user)
        self.assertTrue(cart.session_key)

    def test_get_or_create_cart_returns_same_cart_for_same_guest_session(self):
        request = self._get_request()
        cart1 = get_or_create_cart(request)
        cart2 = get_or_create_cart(request)

        self.assertEqual(cart1.pk, cart2.pk)

    def test_get_or_create_cart_uses_user_cart_when_authenticated(self):
        request = self._get_request(user=self.user)
        cart = get_or_create_cart(request)

        self.assertEqual(cart.user, self.user)
        self.assertTrue(cart.session_key)

    def test_merge_guest_cart_into_user_cart_on_login(self):
        # Step 1: guest builds a cart
        guest_request = self._get_request()
        guest_cart = get_or_create_cart(guest_request)
        CartItem.objects.create(cart=guest_cart, product=self.product, qty=2)

        session_key = guest_request.session.session_key

        # Step 2: user logs in with same session; Django emits user_logged_in
        login_request = guest_request
        login_request.user = self.user

        # send the signal manually in tests (Django would do this in real login)
        user_logged_in.send(
            sender=self.user.__class__,
            request=login_request,
            user=self.user,
        )

        # After login, there should be a user cart with the items
        user_cart = Cart.objects.get(user=self.user)
        self.assertEqual(user_cart.items.count(), 1)
        item = user_cart.items.first()
        self.assertEqual(item.product, self.product)
        self.assertEqual(item.qty, 2)

        # Guest cart should be gone
        self.assertFalse(
            Cart.objects.filter(session_key=session_key, user__isnull=True).exists()
        )
