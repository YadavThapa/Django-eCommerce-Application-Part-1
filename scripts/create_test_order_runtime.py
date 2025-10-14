#!/usr/bin/env python
"""Runtime helper: create a minimal test order.

Small helper for runtime smoke checks. Creates a buyer, a vendor store if
missing, ensures a product exists, and creates a single order with one
item.
"""

# pylint: disable=wrong-import-position,import-error,no-member
import os
from decimal import Decimal

import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce_project.settings")
django.setup()

# Runtime imports (after django.setup()) so the script runs standalone.
# If you want strict local typing, install `django-stubs` in the venv.
from django.contrib.auth import get_user_model  # noqa: E402  # type: ignore[import]
User = get_user_model()  # noqa: E402  # type: ignore
from django.core.exceptions import ObjectDoesNotExist  # noqa: E402  # type: ignore[import]

# Use the project import path so workspace static analysis finds the module.
from main.shop.models import Order, OrderItem, Product, Store  # noqa: E402  # type: ignore[import]


def create_test_order():
    """Create a minimal test order for runtime checks."""
    print("Creating runtime test order")

    try:
        buyer = User.objects.get(username="testbuyer")
    except ObjectDoesNotExist:
        buyer = User.objects.create_user(
            username="testbuyer",
            email="testbuyer@example.com",
            password="testpass123",
        )

    try:
        vendor = User.objects.get(username="vendor1")
    except ObjectDoesNotExist:
        print("Vendor not found, skipping")
        return

    store = Store.objects.filter(vendor=vendor).first()
    if not store:
        store = Store.objects.create(
            name="Runtime Test Store",
            description=("A store created by runtime helper"),
            vendor=vendor,
            is_active=True,
        )

    product = Product.objects.filter(store=store).first()
    if not product:
        product = Product.objects.create(
            name="Runtime Widget",
            description="A runtime product",
            price=Decimal("19.99"),
            quantity=10,
            store=store,
        )

    order = Order.objects.create(buyer=buyer, total_amount=Decimal("0.00"))
    OrderItem.objects.create(
        order=order, product=product, quantity=1, price=product.price
    )
    order.total_amount = product.price
    order.save()

    print(f"Runtime order created: {order.order_id}")
    return order


if __name__ == "__main__":
    create_test_order()
