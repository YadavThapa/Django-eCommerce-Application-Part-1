from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from main.shop.models import Product, Store, Category, Order, OrderItem, Review

User = get_user_model()


class ReviewVerificationTests(TestCase):
    def setUp(self):
        # Create users
        self.buyer = User.objects.create_user(username="buyer", password="pass")
        self.browser = User.objects.create_user(username="browser", password="pass")

        # Create store, category, and product
        self.store = Store.objects.create(vendor=self.buyer, name="S1", description="d")
        self.category = Category.objects.create(name="C1", description="c")
        self.product = Product.objects.create(
            store=self.store,
            category=self.category,
            name="P1",
            description="desc",
            price=10.00,
            quantity=100,
        )

        # Create an order for buyer containing the product
        self.order = Order.objects.create(buyer=self.buyer, total_amount=10.00, shipping_address="addr")
        OrderItem.objects.create(order=self.order, product=self.product, quantity=1, price=10.00)

        self.client = Client()

    def test_purchaser_review_is_verified(self):
        # Log in as buyer, POST review
        self.client.login(username="buyer", password="pass")
        url = reverse("shop:add_review", kwargs={"product_id": self.product.pk})
        resp = self.client.post(url, {"rating": 5, "comment": "Nice"}, follow=True)
        self.assertEqual(resp.status_code, 200)
        review = Review.objects.get(product=self.product, user=self.buyer)
        self.assertTrue(review.is_verified, "Reviews by purchasers should be verified")

    def test_non_purchaser_review_is_unverified(self):
        # Log in as browser, POST review
        self.client.login(username="browser", password="pass")
        url = reverse("shop:add_review", kwargs={"product_id": self.product.pk})
        resp = self.client.post(url, {"rating": 4, "comment": "Looks good"}, follow=True)
        self.assertEqual(resp.status_code, 200)
        review = Review.objects.get(product=self.product, user=self.browser)
        self.assertFalse(review.is_verified, "Reviews by non-purchasers should be unverified")

    def test_duplicate_review_prevented(self):
        # Buyer posts once
        self.client.login(username="buyer", password="pass")
        url = reverse("shop:add_review", kwargs={"product_id": self.product.pk})
        resp = self.client.post(url, {"rating": 5, "comment": "Nice"}, follow=True)
        self.assertEqual(resp.status_code, 200)
        # Try posting again - should be prevented (error message and no new Review)
        resp2 = self.client.post(url, {"rating": 3, "comment": "Again"}, follow=True)
        self.assertEqual(resp2.status_code, 200)
        reviews = Review.objects.filter(product=self.product, user=self.buyer)
        self.assertEqual(
            reviews.count(),
            1,
            "User should not be able to create duplicate reviews",
        )
