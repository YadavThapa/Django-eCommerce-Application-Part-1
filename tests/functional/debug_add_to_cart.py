#!/usr/bin/env python
"""Debug helper: exercise the add-to-cart flow for local development.
"""

import os
import sys

import django  # type: ignore[import]
from typing import Any

# Add the project root to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(project_dir, "..", "..")
sys.path.insert(0, project_root)

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce_project.settings")
django.setup()

from django.contrib.auth import get_user_model  # noqa: E402
from django.test import Client  # noqa: E402
from main.shop.models import Cart, Product  # noqa: E402
User: Any = get_user_model()

# Create test client
client = Client()

# Get or create test user
try:
    user = User.objects.get(username="demo_buyer")
    print(f"✅ Found user: {user.username}")
except User.DoesNotExist:
    print("❌ demo_buyer user not found!")
    sys.exit(1)

# Check user profile
try:
    profile = user.profile  # type: ignore[attr-defined]
    print(f"✅ User profile role: {profile.role}")
except Exception as e:  # pylint: disable=broad-except
    print(f"❌ User profile not found! ({e})")
    sys.exit(1)

# Login
login_result = client.login(username="demo_buyer", password="buyer123")
print(f"✅ Login successful: {login_result}")

# Get a product
products = Product.objects.all()[:1]
if not products:
    print("❌ No products found!")
    sys.exit(1)

product = products[0]
print(f"✅ Testing with product: {product.name} (ID: {product.pk})")

# Check initial cart state
cart, created = Cart.objects.get_or_create(user=user)
initial_count = cart.items.count()  # type: ignore[attr-defined]
print(f"📊 Initial cart items: {initial_count}")

# Get add_to_cart URL
from django.urls import reverse  # noqa: E402  # type: ignore

add_url = reverse("shop:add_to_cart", kwargs={"product_id": product.pk})
print(f"🔗 Add to cart URL: {add_url}")

# Get the product detail page first to get CSRF token
detail_url = reverse("shop:product_detail", kwargs={"pk": product.pk})
response = client.get(detail_url)
print(f"📄 Product detail page status: {response.status_code}")

# Try to add to cart with proper POST data
csrftoken_present = "csrftoken" in client.cookies
csrf = client.cookies["csrftoken"].value if csrftoken_present else ""
response = client.post(add_url, {"quantity": 1, "csrfmiddlewaretoken": csrf})

print("🛒 Add to cart response status:", response.status_code)
if hasattr(response, "url"):
    print("🔄 Add to cart redirect URL:", response.url)
else:
    print("🔄 Add to cart redirect URL: None")

# Check final cart state
cart.refresh_from_db()
final_count = cart.items.count()  # type: ignore[attr-defined]
print(f"📊 Final cart items: {final_count}")

if final_count > initial_count:
    print("✅ SUCCESS: Item was added to cart!")
    # Show cart contents
    for item in cart.items.all():  # type: ignore[attr-defined]
        print(f"   - {item.product.name}: quantity {item.quantity}")
else:
    print("❌ FAILED: No item was added to cart")

    # Debug: Check if there were any validation errors
    print("\n🔍 Debug info:")
    print(f"Product quantity available: {product.quantity}")
    print(f"User authenticated: {user.is_authenticated}")
    print(f"User role: {profile.role}")

    # Try to call the view manually
    print("\n🧪 Manual view test:")
    from django.http import HttpRequest  # type: ignore
    from main.shop.views import add_to_cart

    request = HttpRequest()
    request.method = "POST"
    request.user = user
    from django.http import QueryDict  # type: ignore[import]

    request.POST = QueryDict("quantity=1")

    try:  # pylint: disable=broad-except
        view_response = add_to_cart(request, product.pk)
        print(f"Manual view response: {view_response}")
    except Exception as e:  # pylint: disable=broad-except
        print(f"Manual view error: {e}")
