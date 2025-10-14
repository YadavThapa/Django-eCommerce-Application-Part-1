#!/usr/bin/env python
"""
Comprehensive test for the password reset system
"""
# flake8: noqa
# pylint: disable=import-outside-toplevel,no-member,wrong-import-position

import os

import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce_project.settings")
django.setup()

from datetime import timedelta  # noqa: E402

from django.contrib.auth import get_user_model  # noqa: E402  # type: ignore[import]

User = get_user_model()  # type: ignore
from django.utils import timezone  # noqa: E402
from main.shop.models import (  # type: ignore  # noqa: E402
    PasswordResetToken as _PasswordResetToken,
)
from typing import Any

# Rebind to Any for static analysis (Django ORM dynamic members)
PasswordResetToken: Any = _PasswordResetToken


def test_password_reset_system():
    print("🔑 TESTING PASSWORD RESET SYSTEM")
    print("=" * 50)

    # Get or create test user
    test_user, created = User.objects.get_or_create(
        username="password_test_user",
        defaults={
            "email": "passwordtest@example.com",
            "first_name": "Password",
            "last_name": "Tester",
        },
    )

    if created:
        test_user.set_password("oldpassword123")
        test_user.save()
        print(f"✅ Created test user: {test_user.username}")
    else:
        print(f"✅ Found existing test user: {test_user.username}")

    # Test token creation
    try:
        PasswordResetToken.objects.filter(user=test_user).delete()
        token = PasswordResetToken.objects.create(
            user=test_user,
            expires_at=timezone.now() + timedelta(hours=1),
        )

        print("✅ Token created successfully")
        print(f"   Token: {token.token}")

    except Exception as e:  # pylint: disable=broad-except
        print(f"❌ Token creation failed: {e}")
        return

    # Create expired token
    expired_token = PasswordResetToken.objects.create(
        user=test_user,
        expires_at=timezone.now() - timedelta(minutes=30),
    )

    print("✅ Expired token test:")
    print(f"   Is expired: {expired_token.is_expired}")

    # Cleanup
    deleted_count = PasswordResetToken.objects.filter(user=test_user).delete()[0]
    print(f"   Deleted {deleted_count} test tokens")

    print("\n✅ PASSWORD RESET SYSTEM TEST COMPLETE!")


if __name__ == "__main__":
    test_password_reset_system()
