"""Management command to create sample data.

This command is used during development to populate the DB with
categories, users, stores, products and reviews. Pylint reports a
number of false positives for Django model attributes; relax checks
locally for this dev-only script.
"""

# Pylint false-positives for Django model attributes (objects, create)
# and script complexity for a dev helper. Keep the disable list wrapped
# to respect project max-line-length.
# pylint: disable=import-error,no-member,too-many-locals,
#    too-many-branches,too-many-statements

import random
from decimal import Decimal

from django.contrib.auth import get_user_model  # type: ignore
from django.core.management.base import BaseCommand  # type: ignore
from shop.models import Category, Product, Review, Store

# Resolve the project user model after imports to avoid module-level code
User = get_user_model()


class Command(BaseCommand):
    """Management command to create sample data for the ecommerce site."""

    help = "Create sample data for testing"

    def handle(self, *args, **options):
        """Create sample data."""
        # Create categories
        categories_data = [
            {
                "name": "Electronics",
                "description": "Electronic devices and gadgets",
            },
            {
                "name": "Clothing",
                "description": "Fashion and apparel",
            },
            {
                "name": "Home & Garden",
                "description": ("Home improvement and garden items"),
            },
            {
                "name": "Books",
                "description": "Books and educational materials",
            },
            {
                "name": "Sports",
                "description": "Sports and fitness equipment",
            },
        ]
        categories = []
        for cat_data in categories_data:
            # pylint: disable=no-member
            category, created = Category.objects.get_or_create(
                name=cat_data["name"],
                defaults={"description": cat_data["description"]},
            )
            categories.append(category)
            if created:
                self.stdout.write(f"Created category: {cat_data['name']}")
        # Create vendor users
        vendors = []
        for i in range(1, 4):
            username = f"vendor{i}"
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f"vendor{i}@example.com",
                    password="password123",
                    first_name=f"Vendor{i}",
                    last_name="User",
                )
                # Update the auto-created profile
                profile = user.profile
                profile.role = "vendor"
                profile.phone = f"555-000{i}"
                profile.address = f"{i}23 Vendor Street, City"
                profile.save()
                vendors.append(user)
                self.stdout.write(f"Created vendor: {username}")
            else:
                vendors.append(User.objects.get(username=username))
        # Create buyer users
        buyers = []
        for i in range(1, 6):
            username = f"buyer{i}"
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f"buyer{i}@example.com",
                    password="password123",
                    first_name=f"Buyer{i}",
                    last_name="User",
                )
                # Update the auto-created profile
                profile = user.profile
                profile.role = "buyer"
                profile.phone = f"555-100{i}"
                profile.address = f"{i}45 Buyer Avenue, City"
                profile.save()
                buyers.append(user)
                self.stdout.write(f"Created buyer: {username}")
            else:
                buyers.append(User.objects.get(username=username))
        # Create stores
        store_names = [
            "Tech Haven",
            "Fashion World",
            "Sports Central",
        ]
        stores = []
        for vendor, store_name in zip(vendors, store_names):
            # pylint: disable=no-member
            store, created = Store.objects.get_or_create(
                vendor=vendor,
                name=store_name,
                defaults={"description": f"Welcome to {store_name}!"},
            )
            stores.append(store)
            if created:
                self.stdout.write(f"Created store: {store_name}")
        # Create products
        products_data = [
            # Electronics
            {
                "name": "Laptop",
                "price": 999.99,
                "quantity": 50,
                "category": 0,
                "store": 0,
            },
            {
                "name": "Smartphone",
                "price": 699.99,
                "quantity": 100,
                "category": 0,
                "store": 0,
            },
            {
                "name": "Headphones",
                "price": 149.99,
                "quantity": 200,
                "category": 0,
                "store": 0,
            },
            # Clothing
            {
                "name": "T-Shirt",
                "price": 29.99,
                "quantity": 500,
                "category": 1,
                "store": 1,
            },
            {
                "name": "Jeans",
                "price": 59.99,
                "quantity": 300,
                "category": 1,
                "store": 1,
            },
            {
                "name": "Sneakers",
                "price": 89.99,
                "quantity": 150,
                "category": 1,
                "store": 1,
            },
            # Home & Garden
            {
                "name": "Coffee Maker",
                "price": 79.99,
                "quantity": 75,
                "category": 2,
                "store": 2,
            },
            {
                "name": "Blender",
                "price": 49.99,
                "quantity": 100,
                "category": 2,
                "store": 2,
            },
            {
                "name": "Garden Tools Set",
                "price": 129.99,
                "quantity": 60,
                "category": 2,
                "store": 2,
            },
            # Books
            {
                "name": "Python Programming Guide",
                "price": 49.99,
                "quantity": 200,
                "category": 3,
                "store": 0,
            },
            {
                "name": "Web Development Handbook",
                "price": 39.99,
                "quantity": 150,
                "category": 3,
                "store": 0,
            },
            {
                "name": "Data Science for Beginners",
                "price": 45.99,
                "quantity": 180,
                "category": 3,
                "store": 1,
            },
            {
                "name": "The Great Novel Collection",
                "price": 29.99,
                "quantity": 250,
                "category": 3,
                "store": 1,
            },
            {
                "name": "History of Nepal",
                "price": 35.99,
                "quantity": 120,
                "category": 3,
                "store": 2,
            },
            {
                "name": "Cooking Masterclass",
                "price": 42.99,
                "quantity": 100,
                "category": 3,
                "store": 2,
            },
            # Sports
            {
                "name": "Football",
                "price": 25.99,
                "quantity": 300,
                "category": 4,
                "store": 0,
            },
            {
                "name": "Basketball",
                "price": 35.99,
                "quantity": 200,
                "category": 4,
                "store": 0,
            },
            {
                "name": "Tennis Racket",
                "price": 89.99,
                "quantity": 80,
                "category": 4,
                "store": 2,
            },
            {
                "name": "Yoga Mat",
                "price": 29.99,
                "quantity": 500,
                "category": 4,
                "store": 2,
            },
            {
                "name": "Dumbbells Set",
                "price": 149.99,
                "quantity": 60,
                "category": 4,
                "store": 2,
            },
            {
                "name": "Running Shoes",
                "price": 99.99,
                "quantity": 150,
                "category": 4,
                "store": 2,
            },
        ]
        products = []
        for prod_data in products_data:
            if not Product.objects.filter(  # pylint: disable=no-member
                name=prod_data["name"], store=stores[prod_data["store"]]
            ).exists():
                product = Product.objects.create(  # pylint: disable=no-member
                    store=stores[prod_data["store"]],
                    category=categories[prod_data["category"]],
                    name=prod_data["name"],
                    description=(
                        f"High-quality {prod_data['name']} " f"with excellent features."
                    ),
                    price=Decimal(str(prod_data["price"])),
                    quantity=prod_data["quantity"],
                )
                products.append(product)
                self.stdout.write(f"Created product: {prod_data['name']}")
        # Create reviews
        if products and buyers:
            for product in products[:6]:
                for buyer in buyers[:3]:
                    if not Review.objects.filter(  # pylint: disable=no-member
                        product=product, user=buyer
                    ).exists():
                        Review.objects.create(  # pylint: disable=no-member
                            product=product,
                            user=buyer,
                            rating=random.randint(3, 5),
                            comment=(
                                f"Great {product.name.lower()}! "
                                "Very satisfied with my purchase."
                            ),
                            is_verified=random.choice([True, False]),
                        )
            self.stdout.write("Created reviews for products")
        self.stdout.write(
            self.style.SUCCESS(  # pylint: disable=no-member
                (
                    "\nSample data created successfully!\n"
                    "Vendors: vendor1/password123, vendor2/password123\n"
                    "Buyers: buyer1/password123, buyer2/password123\n"
                )
            )
        )
