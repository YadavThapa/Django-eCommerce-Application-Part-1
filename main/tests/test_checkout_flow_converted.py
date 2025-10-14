"""Basic checkout flow test converted from a developer script.

Simple end-to-end checkout flow using the Django test client.
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from shop.models import Product, Store

# pylint: disable=E1101

User = get_user_model()


class CheckoutFlowConverted(TestCase):
    """Test the basic add-to-cart and checkout flow."""

    def setUp(self):
        self.buyer = User.objects.create_user(username="himallz", password="demo123")
        self.vendor = User.objects.create_user(
            username="vendorx", password="vendorpass"
        )
        self.store = Store.objects.create(name="Flow Store", vendor=self.vendor)
        self.product = Product.objects.create(
            name="Flow Product",
            store=self.store,
            price=Decimal("3.33"),
            quantity=3,
            is_active=True,
        )
        self.client = Client()

    def test_checkout_flow_basic(self):
        logged = self.client.login(username="himallz", password="demo123")
        self.assertTrue(logged)
        add_resp = self.client.post(f"/cart/add/{self.product.id}/")
        self.assertIn(add_resp.status_code, (200, 302, 303))
        resp = self.client.post("/checkout/", {"shipping_address": "1 Flow St"})
        self.assertIn(resp.status_code, (200, 302))
