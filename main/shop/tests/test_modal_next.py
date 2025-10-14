from django.test import TestCase, Client
from django.urls import reverse

from shop.models import Product, Store
from django.contrib.auth import get_user_model
from shop.models import Order, OrderItem


class ModalNextRedirectTests(TestCase):
    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            password='safepass',
            email='test@example.com',
        )
        # create a store required by Product.store (store.vendor is the user)
        self.store = Store.objects.create(
            vendor=self.user,
            name='Test Store',
            description='store desc',
        )
        # create a product to redirect to
        self.product = Product.objects.create(
            store=self.store,
            name='Test Product',
            price=10.0,
            description='desc',
            quantity=5,
            is_active=True,
        )

    def test_login_redirects_to_next(self):
        login_url = reverse('shop:login')
        next_path = reverse('shop:product_detail', args=[self.product.pk])

        resp = self.client.post(
            login_url,
            {
                'username': 'testuser',
                'password': 'safepass',
                'next': next_path,
            },
        )
        # Should redirect to next path
        self.assertEqual(resp.status_code, 302)
        self.assertIn(next_path, resp['Location'])

    def test_register_redirects_to_next(self):
        register_url = reverse('shop:register')
        next_path = reverse('shop:product_detail', args=[self.product.pk])

        # register new user via POST
        resp = self.client.post(
            register_url,
            {
                'username': 'newuser',
                'password1': 'complexpass123',
                'password2': 'complexpass123',
                'email': 'newuser@example.com',
                'first_name': 'New',
                'last_name': 'User',
                'role': 'buyer',
                'next': next_path,
            },
        )
        # After registration the view logs user in and should redirect to next
        self.assertEqual(resp.status_code, 302)
        self.assertIn(next_path, resp['Location'])

    def test_login_then_submit_review_creates_unverified(self):
        # login via next redirect
        login_url = reverse('shop:login')
        next_path = reverse('shop:product_detail', args=[self.product.pk])
        resp = self.client.post(
            login_url,
            {
                'username': 'testuser',
                'password': 'safepass',
                'next': next_path,
            },
        )
        # follow the redirect to the product detail
        self.assertEqual(resp.status_code, 302)
        # client should now be authenticated
        self.assertIn('_auth_user_id', self.client.session)
        # GET the product detail page (should be accessible after login)
        resp = self.client.get(next_path)
        self.assertEqual(resp.status_code, 200)

        # Post a review using the add_review view
        add_url = reverse('shop:add_review', args=[self.product.pk])
        resp = self.client.post(
            add_url, {"rating": "5", "comment": "Great product!"}
        )
        # After posting, should redirect back to product detail
        self.assertEqual(resp.status_code, 302)

        # Review should exist and be unverified (no purchase)
        from shop.models import Review

        self.assertTrue(
            Review.objects.filter(product=self.product, user=self.user).exists()
        )
        review = Review.objects.get(product=self.product, user=self.user)
        self.assertFalse(review.is_verified)

    def test_purchaser_can_submit_verified_review(self):
        # create an order for this user and an order item for the product
        order = Order.objects.create(
            buyer=self.user,
            total_amount=100.00,
            shipping_address='123 Demo St',
        )
        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=1,
            price=self.product.price,
        )

        # login
        self.client.login(username='testuser', password='safepass')

        # post a review
        add_url = reverse('shop:add_review', args=[self.product.pk])
        resp = self.client.post(add_url, {'rating': '4', 'comment': 'Purchased and liked it'})
        self.assertEqual(resp.status_code, 302)

        from shop.models import Review
        self.assertTrue(Review.objects.filter(product=self.product, user=self.user).exists())
        review = Review.objects.get(product=self.product, user=self.user)
        # purchaser reviews should be verified
        self.assertTrue(review.is_verified)
