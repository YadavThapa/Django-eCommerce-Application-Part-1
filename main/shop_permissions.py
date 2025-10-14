"""Compatibility shim: re-export selected names from shop.permissions.

This file is a thin compatibility layer kept at project root so legacy
imports like ``from shop_permissions import role_required`` continue to
work. All implementations live in ``shop/permissions.py``.
"""

from main.shop.permissions import (
    HttpResponseForbidden,
    PermissionDenied,
    PermissionMixin,
    admin_required,
    anonymous_required,
    api_permission_required,
    buyer_required,
    group_required,
    login_required,
    messages,
    owner_required,
    permission_required,
    redirect,
    render,
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
    wraps,
)

__all__ = [
    "HttpResponseForbidden",
    "PermissionDenied",
    "PermissionMixin",
    "admin_required",
    "anonymous_required",
    "api_permission_required",
    "buyer_required",
    "group_required",
    "login_required",
    "messages",
    "owner_required",
    "permission_required",
    "redirect",
    "render",
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
    "wraps",
]
