#!/usr/bin/env python
import os
import sys

import django

# Set up Django environment
# Add project root to Python path
project_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
sys.path.insert(0, project_root)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce_project.settings")
django.setup()

# Runtime imports placed after django.setup() so this script can run
# standalone in developer environments. If you want stricter static
# checking locally install `django-stubs` into the workspace venv.
from django.contrib.auth import get_user_model  # noqa: E402  # type: ignore[import]
User = get_user_model()  # noqa: E402  # type: ignore
from django.test import Client  # noqa: E402  # type: ignore[import]
from main.shop.models import Cart, Product  # noqa: E402  # type: ignore[import]

print("=== WEB FORM TEST ===")

# Create test client
client = Client()

# Get demo buyer
user = User.objects.get(username="demo_buyer")
print(f"✅ User: {user.get_username()} (Password: buyer123)")

# Force login (bypassing the login form)
client.force_login(user)
print("✅ Force login successful")

# Get a product
product = Product.objects.first()
print(f"✅ Product: {product.name} (ID: {product.pk})")

# Check initial cart
cart, _ = Cart.objects.get_or_create(user=user)
initial_count = cart.items.count()
print(f"📊 Initial cart items: {initial_count}")

# Post to add_to_cart
response = client.post(f"/cart/add/{product.pk}/", {"quantity": 1})

print(f"🛒 Add to cart response: {response.status_code}")
if hasattr(response, "url"):
    print(f"🔄 Redirect to: {response.url}")

# Check final cart
cart.refresh_from_db()
final_count = cart.items.count()
print(f"📊 Final cart items: {final_count}")

if final_count > initial_count:
    print("✅ SUCCESS: Item added via web form!")
else:
    print("❌ FAILED: Item not added via web form")

    # Let's check what the add_to_cart view actually receives
    print("\n🔍 Debugging web form...")

    # Check if user is properly authenticated in the view
    response = client.get(f"/products/{product.pk}/")
    print(f"Product page status: {response.status_code}")

    # Check messages framework
    from django.contrib.messages import get_messages

    messages = list(get_messages(response.wsgi_request))
    if messages:
        print("Messages:")
        for message in messages:
            print(f"  - {message}")

print("\n📦 Current Cart Contents:")
for item in cart.items.all():
    print(f"  - {item.product.name}: {item.quantity} x ${item.product.price}")
