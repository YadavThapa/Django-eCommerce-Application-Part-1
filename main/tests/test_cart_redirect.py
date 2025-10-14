"""Tests for add-to-cart redirect behavior."""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from shop.models import Product, Store


class AddToCartRedirectTest(TestCase):
    """Ensure POST to add_to_cart returns 303 See Other pointing to
    cart detail.
    """

    def setUp(self):
        # Create the minimal objects required to make a Product
        UserModel = get_user_model()
        self.user = UserModel.objects.create_user(username="tester", password="pass")
        self.store = Store.objects.create(
            vendor=self.user, name="Demo Store", description="x"
        )
        self.product = Product.objects.create(
            store=self.store,
            name="Test Product",
            description="Test",
            price=Decimal("9.99"),
            quantity=10,
        )

    def test_add_to_cart_posts_redirects_to_cart(self):
        """POST to add_to_cart should redirect (303 or 302) to cart detail."""
        url = reverse("shop:add_to_cart", args=[self.product.pk])
        res = self.client.post(url, {"quantity": 1}, follow=False)
        # Explicit 303 See Other expected
        self.assertIn(res.status_code, (303, 302))
        expected = reverse("shop:cart_detail")
        self.assertEqual(res["Location"], expected)
