"""Minimal smoke tests for main site pages and basic flows."""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import NoReverseMatch, reverse

"""Avoid importing Django ORM models at module import time.

Importing models at top-level can trigger class creation before Django's
app registry is configured when the unittest loader imports test modules.
Move imports into setUp so they occur after Django is initialized by the
test runner.
"""


User = get_user_model()


class SmokeTests(TestCase):
    """Minimal smoke tests for key pages and flows."""

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="smokebuyer",
            email="smoke@example.com",
            password="smokepass",
        )

        # Create a vendor user required by Store.vendor foreign key
        self.vendor = User.objects.create_user(
            username="smokevendor",
            email="vendor@example.com",
            password="vendorpass",
        )

        # Import models here to ensure Django apps registry is ready and to
        # avoid duplicate model registration under different module names.
        from shop import models as _models  # type: ignore

        # Bind model classes to the test instance
        self.Store = _models.Store
        self.Product = _models.Product
        self.Cart = _models.Cart
        self.Profile = _models.Profile

        # Ensure vendor profile role is 'vendor' if profile exists; create if missing
        try:
            self.vendor.profile.role = "vendor"
            self.vendor.profile.save()
        except Exception:
            # If signal hasn't created a profile yet, create one
            self.Profile.objects.get_or_create(
                user=self.vendor, defaults={"role": "vendor"}
            )

        # Create a store and a product
        self.store = self.Store.objects.create(
            name="Smoke Store",
            vendor=self.vendor,
            description="Smoke store for tests",
        )

        self.product = self.Product.objects.create(
            name="Smoke Product",
            store=self.store,
            description=("A small product used by smoke tests"),
            price=Decimal("9.99"),
            quantity=10,
            is_active=True,
        )

        # Ensure the cart exists for user
        self.cart, _ = self.Cart.objects.get_or_create(user=self.user)
        self.client = Client()

    # Models already imported and bound to self above

    def test_home_page_loads(self):
        resp = self.client.get("/")
        self.assertIn(resp.status_code, (200, 302))

    def test_product_detail_and_add_to_cart(self):
        # Product detail (use reverse to match URLconf)
        url = reverse("shop:product_detail", kwargs={"pk": self.product.id})
        resp = self.client.get(url)
        self.assertIn(resp.status_code, (200, 302))

        # Log in and add to cart
        logged = self.client.login(username="smokebuyer", password="smokepass")
        self.assertTrue(logged)

        add_url = f"/cart/add/{self.product.id}/"

        # Try reverse for named URL; fallback to hardcoded path used by the app
        try:
            add_resp = self.client.post(
                reverse("shop:add_to_cart", kwargs={"product_id": self.product.id})
            )
        except NoReverseMatch:
            add_resp = self.client.post(add_url)

        # Some setups redirect with 302 or 303 after POST; accept either
        self.assertIn(add_resp.status_code, (200, 302, 303))

        # Verify cart updated by checking the cart detail page (session-based cart)
        try:
            cart_url = reverse("shop:cart_detail")
        except NoReverseMatch:
            cart_url = "/cart/"

        cart_resp = self.client.get(cart_url)
        self.assertIn(cart_resp.status_code, (200, 302))
        # Product name should appear in cart page HTML
        self.assertIn(self.product.name.encode(), cart_resp.content)

    def test_checkout_page_requires_post_or_login(self):
        # Checkout page should be reachable (may redirect to login)
        resp = self.client.get("/checkout/")
        self.assertIn(resp.status_code, (200, 302))

        # After login, checkout should load
        self.client.login(username="smokebuyer", password="smokepass")
        resp2 = self.client.get("/checkout/")
        self.assertIn(resp2.status_code, (200, 302))
