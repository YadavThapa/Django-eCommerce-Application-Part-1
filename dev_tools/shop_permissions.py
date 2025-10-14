"""
Compatibility shim so legacy imports like `import shop_permissions`
continue to work while the codebase's canonical package lives under `main`.

This file re-exports symbols from `main.shop_permissions` when available.
"""
try:
    # Import the package module and re-export known symbols. Importing the
    # module as a whole avoids wildcard-import lint warnings while still
    # allowing us to expose the same API.
    import importlib

    _mp = importlib.import_module("main.shop_permissions")

    # List of names we intend to re-export from main.shop_permissions
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
        # keep has_permission for compatibility
        "has_permission",
    ]

    # Copy attributes from the imported module into this module's globals so
    # legacy imports like `import shop_permissions` still work.
    for _name in __all__:
        if hasattr(_mp, _name):
            globals()[_name] = getattr(_mp, _name)

except (ImportError, ModuleNotFoundError):
    # pragma: no cover - fallback for environments without main
    # Provide minimal fallback stubs so importing doesn't crash scripts.
    def has_permission(*_args, **_kwargs):
        return False

    # Simple identity decorator for permission decorators fallback.
    def _identity_decorator(func=None):
        if func is None:
            return lambda f: f
        return func

    admin_required = anonymous_required = api_permission_required = buyer_required = (
        group_required
    ) = login_required = owner_required = permission_required = role_required = (
        staff_required
    ) = superuser_required = vendor_required = _identity_decorator

    # Common utility fallbacks
    def wraps(f):
        return f

    messages = None

    def redirect(*_args, **_kwargs):
        return None

    def render(*_args, **_kwargs):
        return None

    # Permission-check fallback predicates
    def _false_predicate(*_args, **_kwargs):
        return False

    user_can_access_admin = user_has_role = user_is_admin = user_is_buyer = (
        user_is_vendor
    ) = user_owns_object = _false_predicate

    # Minimal HTTP/exception placeholders
    class HttpResponseForbidden(Exception):
        pass

    class PermissionDenied(Exception):
        pass

    class PermissionMixin:
        pass

    __all__ = [
        "has_permission",
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
        "HttpResponseForbidden",
        "PermissionDenied",
        "PermissionMixin",
    ]
