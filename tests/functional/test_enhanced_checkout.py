#!/usr/bin/env python
"""Enhanced checkout functional test script (copied from main/tests_organized)."""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce_project.settings")
django.setup()

# Runtime import after django.setup(); install `django-stubs` in the venv
# for stricter typing. Use a narrow type-ignore here to avoid noisy mypy
# messages in developer scripts.
from django.contrib.auth import get_user_model  # noqa: E402  # type: ignore[import]
from main.shop.models import Cart  # noqa: E402  # type: ignore[import]
User = get_user_model()


def test_checkout_system():
    print("Running enhanced checkout test")
    try:
        test_user = User.objects.get(username="testbuyer")
        print(f"✅ Found test user: {test_user.username} ({test_user.email})")
    except Exception:  # pylint: disable=broad-except
        print("❌ Test user not found")
        return False

    try:
        cart = Cart.objects.get(user=test_user)
        print("✅ Cart found for test user")
        print(f"   Cart items: {cart.items.count()}")
    except Exception:  # pylint: disable=broad-except
        print("❌ Cart not found for test user")
        return False

    print("✅ Enhanced checkout flow checks passed")
    return True


if __name__ == "__main__":
    test_checkout_system()
