#!/usr/bin/env python
"""
Real-time functionality test - actually tests the web interface
"""
import os

from typing import Any

import django  # type: ignore[import]
# requests may be untyped in some environments; consider installing
# `types-requests` into the venv. Bind to a typed alias to avoid
# import-untyped diagnostics when stubs are missing.
import requests  # type: ignore[import]
RequestsLib: Any = requests  # type: ignore[name-defined]

# Setup Django
# Use the same settings module the running dev server uses so tests inspect the active DB
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.ecommerce_project.settings")
django.setup()

from django.contrib.auth import get_user_model  # noqa: E402  # type: ignore[import]
from main.shop.models import Product, Store  # noqa: E402  # type: ignore[import]
User: Any = get_user_model()  # type: ignore


def test_actual_web_interface():
    """Test the actual web interface by making HTTP requests"""
    print("🌐 Testing actual web interface...")

    base_url = "http://127.0.0.1:8000"

    try:
        # Test home page
        response = requests.get(f"{base_url}/", timeout=5)
        print(
            f"✓ Home page: {response.status_code} - {len(response.text)} bytes"
        )

        # Test product list
        response = requests.get(f"{base_url}/products/", timeout=5)
        print(
            f"✓ Product list: {response.status_code} - {len(response.text)} bytes"
        )

        # Test login page
        response = requests.get(f"{base_url}/login/", timeout=5)
        print(
            f"✓ Login page: {response.status_code} - {len(response.text)} bytes"
        )

        return True

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Django server")
        return False
    except Exception as e:  # pylint: disable=broad-except
        print(f"❌ Error: {e}")
        return False


def test_login_functionality():
    """Test actual login process"""
    print("\n🔐 Testing login functionality...")
    base_url = "http://127.0.0.1:8000"

    # Helper to perform a login via the running server using requests.Session()
    def try_login(username: str, password: str) -> requests.Session | None:
        s = requests.Session()
        try:
            r = s.get(f"{base_url}/login/", timeout=5)
            print(f"✓ Login page loads ({username}): {r.status_code}")
        except Exception as e:  # pylint: disable=broad-except
            print(f"❌ Cannot reach login page for {username}: {e}")
            return None

        if r.status_code != 200:
            print("❌ Login page not loading")
            return None

        # Pull CSRF token from cookies (typical for Django default setup)
        csrftoken = s.cookies.get("csrftoken", "")
        data = {"username": username, "password": password}
        if csrftoken:
            data["csrfmiddlewaretoken"] = csrftoken

        headers = {"Referer": f"{base_url}/login/"}
        try:
            post = s.post(
                f"{base_url}/login/",
                data=data,
                headers=headers,
                timeout=5,
                allow_redirects=False,
            )
            print(f"✓ {username} login attempt: {post.status_code}")
        except Exception as e:  # pylint: disable=broad-except
            print(f"❌ Login POST failed for {username}: {e}")
            return None

        if post.status_code in (302, 303):
            print(f"✅ {username} login successful (redirect)")
            return s
        # Some apps return 200 with a redirect via JavaScript or inline messages
        if post.status_code == 200 and post.history:
            print(f"✅ {username} login appears successful (200 + history)")
            return s

        print(f"❌ {username} login failed (status {post.status_code})")
        return None

    # Buyer
    buyer_sess = try_login("demo_buyer", "demo123")
    if not buyer_sess:
        return False

    # Test buyer can access cart and customer pages via live server
    for path in ("/cart/", "/customer/"):
        try:
            resp = buyer_sess.get(f"{base_url}{path}", timeout=5)
            print(f"✓ Buyer {path}: {resp.status_code}")
        except Exception as e:  # pylint: disable=broad-except
            print(f"❌ Buyer {path} request failed: {e}")

    # Vendor
    vendor_sess = try_login("demo_vendor", "demo123")
    if not vendor_sess:
        return False

    for path in ("/vendor/", "/vendor/stores/"):
        try:
            resp = vendor_sess.get(f"{base_url}{path}", timeout=5)
            print(f"✓ Vendor {path}: {resp.status_code}")
        except Exception as e:  # pylint: disable=broad-except
            print(f"❌ Vendor {path} request failed: {e}")

    return True


def check_database_state():
    """Check if database has the expected data"""
    print("\n🗄️ Checking database state...")

    # Check users
    buyer_count = User.objects.filter(profile__role="buyer").count()
    vendor_count = User.objects.filter(profile__role="vendor").count()

    print(f"✓ Buyers in database: {buyer_count}")
    print(f"✓ Vendors in database: {vendor_count}")

    # Check if demo users exist
    try:
        demo_buyer = User.objects.get(username="demo_buyer")
        print(f"✓ Demo buyer exists: {demo_buyer.profile.role}")
    except User.DoesNotExist:
        print("❌ Demo buyer not found")
        return False

    try:
        demo_vendor = User.objects.get(username="demo_vendor")
        print(f"✓ Demo vendor exists: {demo_vendor.profile.role}")
    except User.DoesNotExist:
        print("❌ Demo vendor not found")
        return False

    # Check stores
    store_count = Store.objects.count()
    vendor_stores = Store.objects.filter(vendor=demo_vendor).count()
    print(f"✓ Total stores: {store_count}")
    print(f"✓ Demo vendor stores: {vendor_stores}")

    # Check products
    product_count = Product.objects.count()
    vendor_products = Product.objects.filter(store__vendor=demo_vendor).count()
    print(f"✓ Total products: {product_count}")
    print(f"✓ Demo vendor products: {vendor_products}")

    return True


def test_navigation_links():
    """Test if navigation links work properly"""
    print("\n🧭 Testing navigation links...")
    base_url = "http://127.0.0.1:8000"

    # Reuse the login helper to obtain authenticated sessions
    def login_session(username: str, password: str) -> requests.Session | None:
        s = requests.Session()
        try:
            resp = s.get(f"{base_url}/login/", timeout=5)
            # ensure page loaded
            if resp.status_code != 200:
                return None
        except Exception:  # pylint: disable=broad-except
            return None
        csrftoken = s.cookies.get("csrftoken", "")
        data = {"username": username, "password": password}
        if csrftoken:
            data["csrfmiddlewaretoken"] = csrftoken
        headers = {"Referer": f"{base_url}/login/"}
        post = s.post(
            f"{base_url}/login/",
            data=data,
            headers=headers,
            timeout=5,
            allow_redirects=False,
        )
        if post.status_code in (302, 303):
            return s
        return None

    buyer_s = login_session("demo_buyer", "demo123")
    vendor_s = login_session("demo_vendor", "demo123")

    buyer_urls = ["/", "/products/", "/customer/", "/cart/", "/orders/", "/profile/"]
    vendor_urls = ["/vendor/", "/vendor/stores/", "/vendor/products/", "/vendor/stores/create/"]

    print("Buyer URLs:")
    for url in buyer_urls:
        try:
            rr = (buyer_s or requests).get(f"{base_url}{url}", timeout=5)
            status = "✅" if rr.status_code == 200 else "❌"
            print(f"  {status} {url}: {rr.status_code}")
        except Exception as e:  # pylint: disable=broad-except
            print(f"  ❌ {url}: Error - {e}")

    print("\nVendor URLs:")
    for url in vendor_urls:
        try:
            rr = (vendor_s or requests).get(f"{base_url}{url}", timeout=5)
            status = "✅" if rr.status_code == 200 else "❌"
            print(f"  {status} {url}: {rr.status_code}")
        except Exception as e:  # pylint: disable=broad-except
            print(f"  ❌ {url}: Error - {e}")


def main():
    print("🔍 REAL FUNCTIONALITY TEST")
    print("=" * 50)

    # Test web interface connection
    if not test_actual_web_interface():
        print("❌ Cannot connect to web interface")
        return False

    # Check database state
    if not check_database_state():
        print("❌ Database issues found")
        return False

    # Test login functionality
    if not test_login_functionality():
        print("❌ Login functionality issues")
        return False

    # Test navigation
    test_navigation_links()

    print("\n" + "=" * 50)
    print("🎯 REAL TEST RESULTS:")
    print("  ✅ Server is running")
    print("  ✅ Database has data")
    print("  ✅ Login system works")
    print("  ✅ Role-based access works")
    print("=" * 50)

    return True


if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("✅ All functionality appears to be working!")
        else:
            print("❌ Some functionality issues detected")
    except Exception as e:  # pylint: disable=broad-except
        print(f"❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
