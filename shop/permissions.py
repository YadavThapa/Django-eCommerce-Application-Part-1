"""Compatibility shim: re-export the real implementation from ``main.shop.permissions``.

This file allows code to use ``from shop.permissions import ...`` while the
actual implementation remains under ``main.shop.permissions``. Keeping this
shim avoids changing runtime behavior; it's a thin alias only.
"""

from importlib import import_module

# Import the real implementation from the existing location. Use import_module
# so this shim is safe to import in various startup orders.
_real = import_module("main.shop.permissions")

# Re-export the public names used across the codebase.
PermissionMixin = _real.PermissionMixin
admin_required = _real.admin_required
anonymous_required = _real.anonymous_required
api_permission_required = _real.api_permission_required
buyer_required = _real.buyer_required
group_required = _real.group_required
owner_required = _real.owner_required
permission_required = _real.permission_required
role_required = _real.role_required
staff_required = _real.staff_required
superuser_required = _real.superuser_required
user_can_access_admin = _real.user_can_access_admin
user_has_role = _real.user_has_role
user_is_admin = _real.user_is_admin
user_is_buyer = _real.user_is_buyer
user_is_vendor = _real.user_is_vendor
user_owns_object = _real.user_owns_object
vendor_required = _real.vendor_required

__all__ = [
    "PermissionMixin",
    "admin_required",
    "anonymous_required",
    "api_permission_required",
    "buyer_required",
    "group_required",
    "owner_required",
    "permission_required",
    "role_required",
    "staff_required",
    "superuser_required",
    "user_can_access_admin",
    "user_has_role",
    "user_is_admin",
    "user_is_buyer",
    "user_is_vendor",
    "user_owns_object",
    "vendor_required",
]
