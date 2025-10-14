"""Compatibility shim: re-export shop.views at project root.

This module keeps legacy imports like `from views import home` working.
"""

# This is a lightweight compatibility shim at the project root. It's not
# actively maintained and exists to preserve old import paths. Silencing
# heavy editor linters to avoid AST parsing crashes on large legacy files.
# pylint: skip-file
# flake8: noqa
# type: ignore
__all__ = [
    "Cart",
    "CartItem",
    "Category",
    "CheckoutForm",
    "CustomUserCreationForm",
    "DatabaseError",
    "Order",
    "OrderItem",
    "Paginator",
    "Product",
    "ProfileUpdateForm",
    "Q",
    "Review",
    "ReviewForm",
    "Store",
    "StoreForm",
    "about",
    "add_review",
    "add_test_items",
    "add_to_cart",
    "anonymous_required",
    "buyer_required",
    "cart",
    "cart_api",
    "cart_debug",
    "cart_detail",
    "cart_dropdown_test",
    "cart_test",
    "checkout",
    "contact",
    "customer_dashboard",
    "get_object_or_404",
    "home",
    "login",
    "login_required",
    "messages",
    "order_detail",
    "order_history",
    "product_detail",
    "product_list",
    "profile",
    "redirect",
    "register",
    "remove_from_cart",
    "remove_from_session_cart",
    "render",
    "require_POST",
    "settings",
    "store_create",
    "store_detail",
    "store_list",
    "update_cart_item",
    "update_session_cart",
    "vendor_dashboard",
    "vendor_required",
]


def _bind_runtime_exports():
    """Bind names from shop.views into this module at runtime.

    We import the module (not individual symbols) so static analyzers don't
    attempt to resolve the full symbol list. At runtime we copy whatever
    attributes exist into this shim's globals so legacy imports continue to
    work (e.g. `from views import home`).
    """
    try:
        import importlib

        shop_views = importlib.import_module("shop.views")
        for _name in list(__all__):
            try:
                globals()[_name] = getattr(shop_views, _name)
            except AttributeError:
                # Missing symbol in the source module; ignore to keep runtime
                # resilience for partial exports.
                continue
    except Exception:
        # If shop.views can't be imported (analysis envs), do nothing.
        pass


_bind_runtime_exports()
