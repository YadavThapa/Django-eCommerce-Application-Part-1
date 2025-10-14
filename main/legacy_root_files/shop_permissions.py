"""Legacy shim: re-export shop permission helpers.

This module is an archived backup moved on 2025-10-07. It re-exports
symbols from :mod:`shop.permissions` so older import paths continue to work.
"""

from main.shop.permissions import (
    PermissionMixin,
    admin_required,
    anonymous_required,
    buyer_required,
    group_required,
    owner_required,
    permission_required,
    role_required,
    staff_required,
    superuser_required,
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
]
