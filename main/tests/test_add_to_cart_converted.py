"""Converted add-to-cart test (light refactor for style).

This test uses Django TestCase and the test client to exercise the
add-to-cart flow. Pylint may report false positives for Django's
model managers (``objects``); disable that specific check here.
"""

# Pylint doesn't always understand Django model attributes like
# ``objects``. Disable the no-member check for this test module.
# pylint: disable=E1101

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from shop.models import Product, Store

User = get_user_model()


class AddToCartConvertedTests(TestCase):
    """Converted from developer script: test_add_to_cart.py"""

    def setUp(self):
        # Create buyer and vendor
        self.buyer = User.objects.create_user(
            username="demo_buyer",
            email="demo_buyer@example.com",
            password="demo123",
        )
        self.vendor = User.objects.create_user(
            username="demo_vendor",
            email="vendor@example.com",
            password="vendor123",
        )
        # Create store and product
        self.store = Store.objects.create(
            name="Demo Store",
            vendor=self.vendor,
            description="Vendor store",
        )

        self.product = Product.objects.create(
            name="Demo Product",
            store=self.store,
            description="Test product",
            price=Decimal("4.50"),
            quantity=5,
            is_active=True,
        )
        self.client = Client()

    def test_add_to_cart_functionality(self):
        """Ensure a user can add a product to their cart and view it."""
        # login
        resp = self.client.post(
            "/login/",
            {"username": "demo_buyer", "password": "demo123"},
        )
        # allow redirect or ok
        self.assertIn(resp.status_code, (200, 302))

        # add to cart (post)
        add_resp = self.client.post(f"/cart/add/{self.product.id}/")
        self.assertIn(add_resp.status_code, (200, 302, 303))

        # check cart page
        cart_resp = self.client.get("/cart/")
        self.assertIn(cart_resp.status_code, (200, 302))
        self.assertIn(self.product.name.encode(), cart_resp.content)
