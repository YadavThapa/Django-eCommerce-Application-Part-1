#!/usr/bin/env python
import os
import sys

import django
from typing import Any

# Set up Django environment
# Add project root to Python path
project_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
sys.path.insert(0, project_root)
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce_project.settings")
django.setup()

from django.contrib.auth import get_user_model

User: Any = get_user_model()  # noqa: E402
from main.shop.models import Cart, CartItem, Product  # noqa: E402

print("=== QUICK CART TEST ===")

# Get demo buyer
user = User.objects.get(username="demo_buyer")
print(f"✅ User: {user.username}")

# Get a product
product = Product.objects.first()
print(f"✅ Product: {product.name} (Stock: {product.quantity})")

# Get/create cart
cart, created = Cart.objects.get_or_create(user=user)
print(f"✅ Cart: {'Created new' if created else 'Found existing'}")

# Check initial items
initial_count = cart.items.count()
print(f"📊 Initial cart items: {initial_count}")

# Simulate add to cart
cart_item, item_created = CartItem.objects.get_or_create(
    cart=cart, product=product, defaults={"quantity": 1}
)

if not item_created:
    cart_item.quantity += 1
    cart_item.save()
    print(f"✅ Updated existing item quantity to: {cart_item.quantity}")
else:
    print(f"✅ Created new cart item with quantity: {cart_item.quantity}")

# Check final items
final_count = cart.items.count()
print(f"📊 Final cart items: {final_count}")

print("\n📦 Cart Contents:")
for item in cart.items.all():
    print(f"  - {item.product.name}: {item.quantity} x ${item.product.price}")

print(
    f"\n💰 Total: ${sum(item.quantity * item.product.price for item in cart.items.all())}"
)
