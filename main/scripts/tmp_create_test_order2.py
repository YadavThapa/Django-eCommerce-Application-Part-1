#!/usr/bin/env python
"""Create test data to make vendor dashboard functional (alternative).

This variant uses imports from app modules instead of top-level stubs.
"""

# pylint: disable=wrong-import-position,broad-except,no-member
import os
from decimal import Decimal

import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce_project.settings")
django.setup()

from django.contrib.auth import get_user_model  # noqa: E402
from django.core.exceptions import ObjectDoesNotExist  # noqa: E402

User = get_user_model()


def create_test_order():
    """Create a small test order and supporting data for the
    vendor dashboard.
    """
    print("🛒 Creating Test Order for Vendor Dashboard")

    # Import app models at runtime after Django is configured to avoid
    # importing ORM classes before django.setup(). This also keeps the
    # module import clean for static analysis.
    from shop.models import (  # type: ignore[import]
        Order,
        OrderItem,
        Product,
        Store,
    )

    # Get or create test buyer
    try:
        buyer = User.objects.get(username="testbuyer")
        print(f"✅ Found test buyer: {buyer.username}")
    except ObjectDoesNotExist:
        buyer = User.objects.create_user(
            username="testbuyer",
            email="testbuyer@example.com",
            password="testpass123",
        )
        print(f"✅ Created test buyer: {buyer.username}")

    # Get vendor user
    try:
        vendor = User.objects.get(username="vendor1")
        print(f"✅ Found vendor: {vendor.username}")
    except ObjectDoesNotExist:
        print("❌ Vendor 'vendor1' not found!")
        return

    # Get vendor's store
    try:
        store = Store.objects.filter(vendor=vendor).first()
        if not store:
            # Create a test store
            store = Store.objects.create(
                name="Test Vendor Store",
                description="A test store for orders",
                vendor=vendor,
                is_active=True,
            )
            print(f"✅ Created test store: {store.name}")
        else:
            print(f"✅ Found vendor store: {store.name}")
    except Exception as e:  # broad exception is acceptable in a small
        # test script
        print(f"❌ Error with store: {e}")
        return

    # Get or create test products in the store
    products = Product.objects.filter(store=store)
    if not products:
        # Create test products
        test_products = [
            {
                "name": "Laptop Computer",
                "price": Decimal("999.99"),
                "description": "High-performance laptop",
            },
            {
                "name": "Wireless Mouse",
                "price": Decimal("29.99"),
                "description": "Ergonomic wireless mouse",
            },
            {
                "name": "USB Cable",
                "price": Decimal("9.99"),
                "description": "Premium USB-C cable",
            },
        ]

        products = []
        for product_data in test_products:
            product = Product.objects.create(
                name=product_data["name"],
                description=product_data["description"],
                price=product_data["price"],
                quantity=50,
                store=store,
            )
            products.append(product)
            print(f"✅ Created product: {product.name} - ${product.price}")
    else:
        print(f"✅ Found {len(products)} existing products")

    # Create test order
    total_amount = Decimal("0.00")
    order = Order.objects.create(
        buyer=buyer,
        total_amount=total_amount,  # Will update after creating items
        shipping_address=("123 Test Street, Test City, TC 12345"),
    )

    # Create order items
    for i, product in enumerate(products[:3]):  # Use first 3 products
        quantity = i + 1  # 1, 2, 3
        item_total = product.price * quantity
        total_amount += item_total

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price,
        )
        print(f"✅ Added {quantity}x {product.name} to order")

    # Update order total
    order.total_amount = total_amount
    order.save()

    print("\n🎉 Test Order Created Successfully!")
    print(f"   Order ID: {order.order_id}")
    print(f"   Buyer: {buyer.username}")
    print(f"   Total: ${total_amount:.2f}")
    print(f"   Items: {order.items.count()}")

    # Show vendor dashboard stats
    print("\n📊 Vendor Dashboard Stats:")
    total_products = Product.objects.filter(store__vendor=vendor).count()
    total_sales = sum(
        item.total_price
        for item in OrderItem.objects.filter(product__store__vendor=vendor)
    )
    recent_orders = OrderItem.objects.filter(product__store__vendor=vendor).count()

    print(f"   Total Products: {total_products}")
    print(f"   Total Sales: ${total_sales:.2f}")
    print(f"   Recent Orders: {recent_orders}")

    return order


if __name__ == "__main__":
    create_test_order()
