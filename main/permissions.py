"""
Compatibility shim: top-level `permissions.py` proxies to `shop.permissions`.
"""

from shop.permissions import (
    PermissionMixin,
    admin_required,
    anonymous_required,
    api_permission_required,
    buyer_required,
    group_required,
    owner_required,
    permission_required,
    role_required,
    staff_required,
    superuser_required,
    user_can_access_admin,
    user_has_role,
    user_is_admin,
    user_is_buyer,
    user_is_vendor,
    user_owns_object,
    vendor_required,
)

__all__ = [
    "role_required",
    "admin_required",
    "staff_required",
    "superuser_required",
    "vendor_required",
    "buyer_required",
    "anonymous_required",
    "owner_required",
    "group_required",
    "permission_required",
    "PermissionMixin",
    "api_permission_required",
    "user_has_role",
    "user_is_vendor",
    "user_is_buyer",
    "user_is_admin",
    "user_can_access_admin",
    "user_owns_object",
]
