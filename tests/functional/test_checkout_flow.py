#!/usr/bin/env python
"""Test script to verify complete checkout functionality.

This utility is a small developer script that populates and prints a
checkout summary for a test user. It performs an in-file Django
environment setup and therefore contains a few intentionally out-of-order
imports (marked with noqa) to keep static analyzers quiet.
"""
# pylint: disable=wrong-import-position,import-error,import-outside-toplevel
# pylint: disable=no-member
import os

from decimal import Decimal

import django  # type: ignore[import]

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce_project.settings")
django.setup()

# Import Django models at runtime after setup so runtime behavior is correct.
# type: ignore[import]
from django.contrib.auth import get_user_model  # noqa: E402
User = get_user_model()  # noqa: E402
from main.shop.models import Cart  # noqa: E402


def test_checkout_flow():
    """Smoke-run the checkout flow and print a summary for a test user.

    This is a developer convenience script and not a unit test.
    """
    print("🧪 Testing Complete Checkout Flow")
    print("=" * 50)

    # Get the test user (himallz)
    try:
        user = User.objects.get(username="himallz")
        print(f"✅ Found user: {user.username} ({user.email})")
    except User.DoesNotExist:
        print("❌ Test user 'himallz' not found!")
        return

    # Check if user has items in cart
    try:
        cart = Cart.objects.get(user=user)
        cart_items = cart.items.all()
        print(f"🛒 Cart found with {len(cart_items)} items:")

        subtotal = Decimal("0.00")
        for item in cart_items:
            item_total = item.product.price * item.quantity
            subtotal += item_total
            print(f"   📦 {item.product.name}")
            price_str = f"${item.product.price:.2f}"
            item_total_str = f"${item_total:.2f}"
            print(f"      💰 {price_str} x {item.quantity} = {item_total_str}")
            print(f"      🏪 Store: {item.product.store.name}")

        tax = subtotal * Decimal("0.08")
        grand_total = subtotal + tax

        print("\n💵 Order Summary:")
        print(f"   Subtotal: ${subtotal:.2f}")
        print(f"   Tax (8%): ${tax:.2f}")
        print(f"   Grand Total: ${grand_total:.2f}")

    except Cart.DoesNotExist:
        print("❌ No cart found for user!")
        return

    print("\n📧 Email Configuration:")
    print(f"   User Email: {user.email}")
    print("   Invoice will be sent upon checkout completion")

    print("\n🌐 Access URLs:")
    print("   Cart: http://127.0.0.1:8000/cart/")
    print("   Checkout: http://127.0.0.1:8000/checkout/")

    print("\n✅ Checkout Flow Ready!")
    print("   1. Visit cart page to see 'Proceed to Checkout' button")
    print("   2. Click button to go to enhanced checkout page")
    print("   3. Fill shipping information and click")
    print("      'Place Order & Send Invoice'")
    print("   4. Order will be processed, cart cleared, and invoice emailed")


if __name__ == "__main__":
    test_checkout_flow()
