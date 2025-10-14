#!/usr/bin/env python
"""
Test specifically the add to cart functionality
"""
# This is a developer-facing script that performs runtime Django imports
# and intentionally uses broad excepts for friendly CLI output; disable
# the Pylint broad-except warning at module level.
# pylint: disable=broad-except
import os

import django  # type: ignore[import]

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce_project.settings")
django.setup()

from django.contrib.auth import get_user_model  # noqa: E402  # type: ignore[import]
from django.test import Client  # noqa: E402  # type: ignore[import]
from main.shop.models import Cart, Product  # noqa: E402  # type: ignore[import]
User = get_user_model()


def test_add_to_cart_functionality():
    """Test the add to cart feature step by step"""
    print("🛒 TESTING ADD TO CART FUNCTIONALITY")
    print("=" * 50)

    client = Client()

    # Step 1: Login as buyer
    print("1. Logging in as buyer...")
    response = client.post("/login/", {"username": "demo_buyer", "password": "demo123"})
    print(
        f"   Login status: {response.status_code} {'✅' if response.status_code == 302 else '❌'}"
    )

    if response.status_code != 302:
        print("❌ Login failed - cannot test add to cart")
        return False

    # Step 2: Check if products exist
    print("2. Checking available products...")
    products = Product.objects.filter(is_active=True, quantity__gt=0)[:3]
    print(f"   Available products: {products.count()}")

    if products.count() == 0:
        print("❌ No products available for testing")
        return False

    for product in products:
        print(
            f"   - {product.name} (ID: {product.id}) - ${product.price} - Stock: {product.quantity}"
        )

    # Step 3: Check initial cart state
    print("3. Checking initial cart state...")
    try:
        user = User.objects.get(username="demo_buyer")
        cart, _ = Cart.objects.get_or_create(user=user)
        initial_items = cart.items.count()
        print(f"   Initial cart items: {initial_items}")
    except Exception as e:  # pylint: disable=broad-except
        # This is a developer/test helper; broad-except kept to provide
        # friendly CLI output rather than raising inside a dev script.
        print(f"   ❌ Error checking cart: {e}")
        return False

    # Step 4: Test add to cart URL
    test_product = products.first()
    print(f"4. Testing add to cart for: {test_product.name} (ID: {test_product.id})")

    add_to_cart_url = f"/cart/add/{test_product.id}/"
    print(f"   URL: {add_to_cart_url}")

    response = client.post(add_to_cart_url)
    print(f"   Add to cart response: {response.status_code}")

    if response.status_code == 302:
        print("   ✅ Add to cart successful (302 redirect)")
        print(f"   Redirect location: {response.get('Location', 'Not specified')}")
    else:
        print(f"   ❌ Add to cart failed: {response.status_code}")
        if hasattr(response, "content"):
            print(f"   Response content: {response.content[:200]}")
        return False

    # Step 5: Verify item was added to cart
    print("5. Verifying item was added to cart...")
    cart.refresh_from_db()
    final_items = cart.items.count()
    print(f"   Cart items after add: {final_items}")

    if final_items > initial_items:
        print("   ✅ Item successfully added to cart!")

        # Show cart contents
        for item in cart.items.all():
            print(f"   - {item.product.name} x{item.quantity} = ${item.total_price}")

        print(f"   Total cart value: ${cart.total_price}")

    else:
        print("   ❌ Item was NOT added to cart")
        return False

    # Step 6: Test cart page shows the item
    print("6. Testing cart page displays items...")
    response = client.get("/cart/")
    print(f"   Cart page status: {response.status_code}")

    if response.status_code == 200:
        print("   ✅ Cart page loads successfully")
        if test_product.name.encode() in response.content:
            print(f"   ✅ Product '{test_product.name}' found in cart page")
        else:
            print(f"   ❌ Product '{test_product.name}' NOT found in cart page")
    else:
        print("   ❌ Cart page failed to load")

    print("=" * 50)
    return True


def check_add_to_cart_view():
    """Check the add to cart view implementation"""
    print("\n🔍 CHECKING ADD TO CART VIEW IMPLEMENTATION")
    print("-" * 50)

    # Check if the view exists and what it does
    from main.shop import views

    if hasattr(views, "add_to_cart"):
        print("✅ add_to_cart view exists")

        # Check URL pattern
        from main.shop.urls import urlpatterns

        add_to_cart_urls = [
            pattern for pattern in urlpatterns if "add_to_cart" in str(pattern.name)
        ]

        if add_to_cart_urls:
            print(f"✅ add_to_cart URL pattern exists: {add_to_cart_urls[0].pattern}")
        else:
            print("❌ add_to_cart URL pattern NOT found")
            return False

    else:
        print("❌ add_to_cart view NOT found")
        return False

    return True


def diagnose_add_to_cart_issues():
    """Diagnose specific issues with add to cart"""
    print("\n🔧 DIAGNOSING ADD TO CART ISSUES")
    print("-" * 50)

    # Check permissions on add_to_cart view
    try:
        import inspect

        from main.shop.views import add_to_cart

        # Get the function source to see decorators
        source = inspect.getsource(add_to_cart)
        print("Add to cart view source preview:")
        print(source[:300] + "..." if len(source) > 300 else source)

        # Check for permission decorators
        if "@buyer_required" in source:
            print("✅ Found @buyer_required decorator - correct for cart functionality")
        elif "@login_required" in source:
            print("✅ Found @login_required decorator")
        else:
            print("❌ No permission decorators found - this might be an issue")

    except Exception as e:  # pylint: disable=broad-except
        print(f"❌ Could not analyze add_to_cart view: {e}")


if __name__ == "__main__":
    try:
        # Check view implementation
        if not check_add_to_cart_view():
            print("❌ Add to cart view implementation issues found")
            exit(1)

        # Diagnose potential issues
        diagnose_add_to_cart_issues()

        # Test functionality
        if test_add_to_cart_functionality():
            print("\n✅ ADD TO CART FUNCTIONALITY TEST COMPLETED")
        else:
            print("\n❌ ADD TO CART FUNCTIONALITY TEST FAILED")

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
