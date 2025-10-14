#!/usr/bin/env python
"""Developer helper: create a test order (dev variant).

This script populates a test order and supporting objects so the vendor
dashboard has sample data. Run locally only; it performs an in-file
django.setup().
"""

# pylint: disable=wrong-import-position,import-error,no-member,broad-except
import os
from decimal import Decimal

import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce_project.settings")
django.setup()

# Runtime imports must occur after django.setup() so the Django apps are
# configured correctly. Use `django-stubs` in the venv for stricter typing
# if desired. Add narrow ignores here to reduce editor/mypy/flake8 noise.
from django.contrib.auth import get_user_model  # noqa: E402  # type: ignore[import]
User = get_user_model()  # noqa: E402  # type: ignore
from django.core.exceptions import ObjectDoesNotExist  # noqa: E402  # type: ignore[import]

# Use the full project import path so static analyzers inside this workspace
# can resolve the module. Keep type-ignore to avoid mypy/stub noise when
# stubs aren't installed.
from main.shop.models import Order, OrderItem, Product, Store  # noqa: E402  # type: ignore[import]


def create_test_order():
    """Create a small test order for the vendor dashboard.

    Creates a buyer, vendor store (if needed), a few products, and a
    single order with up to three items.
    """
    print("Creating Test Order for Vendor Dashboard")

    # Get or create test buyer
    try:
        buyer = User.objects.get(username="testbuyer")
        print(f"Found test buyer: {buyer.username}")
    except ObjectDoesNotExist:
        buyer = User.objects.create_user(
            username="testbuyer",
            email="testbuyer@example.com",
            password="testpass123",
        )
        print(f"Created test buyer: {buyer.username}")

    # Get vendor user
    try:
        vendor = User.objects.get(username="vendor1")
        print(f"Found vendor: {vendor.username}")
    except ObjectDoesNotExist:
        print("Vendor 'vendor1' not found; aborting")
        return

    # Get or create vendor store
    try:
        store = Store.objects.filter(vendor=vendor).first()
        if not store:
            store = Store.objects.create(
                name="Test Vendor Store",
                description="A test store for orders",
                vendor=vendor,
                is_active=True,
            )
            print(f"Created test store: {store.name}")
        else:
            print(f"Found vendor store: {store.name}")
    except Exception as exc:
        print(f"Error fetching/creating store: {exc}")
        return

    # Ensure products exist
    products = Product.objects.filter(store=store)
    if not products:
        test_products = [
            ("Laptop Computer", Decimal("999.99"), "High-performance laptop"),
            ("Wireless Mouse", Decimal("29.99"), "Ergonomic wireless mouse"),
            ("USB Cable", Decimal("9.99"), "Premium USB-C cable"),
        ]

        products = []
        for name, price, desc in test_products:
            product = Product.objects.create(
                name=name,
                description=desc,
                price=price,
                quantity=50,
                store=store,
            )
            products.append(product)
            print(f"Created product: {product.name} - ${product.price}")
    else:
        print(f"Found {len(products)} existing products")

    # Create order and items
    total_amount = Decimal("0.00")
    order = Order.objects.create(
        buyer=buyer,
        total_amount=total_amount,
        shipping_address="123 Test Street, Test City",
    )

    for i, product in enumerate(products[:3]):
        qty = i + 1
        item_total = product.price * qty
        total_amount += item_total
        OrderItem.objects.create(
            order=order, product=product, quantity=qty, price=product.price
        )
        print(f"Added {qty}x {product.name} to order")

    order.total_amount = total_amount
    order.save()

    print(f"Test order created: id={order.order_id}")
    return order


if __name__ == "__main__":
    create_test_order()
