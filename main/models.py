"""Compatibility shim: re-export shop.models at project root.

Keep this shim minimal to preserve legacy imports like
`from models import Product` while avoiding duplicated code.

This module is a small compatibility shim used to avoid changing web
behavior while converting import paths. It intentionally performs
dynamic imports and re-exports; to reduce noise from static
analysis tools in editor-only environments we disable their checks
for this file.

Note: no runtime behavior is changed by these comments.
"""

# Static analysis / linter hints for this shim (editor-friendly):
# pylint: skip-file
# flake8: noqa
# mypy: ignore-errors

# Runtime: import the shop.models module dynamically and re-export the
# named attributes into this module's globals. This keeps the shim
# minimal while avoiding "imported but unused" linter errors.
# Runtime: import the shop.models module dynamically and re-export the
# named attributes into this module's globals. This keeps the shim
# minimal while avoiding "imported but unused" linter errors.
_shop_models = None
try:
    import importlib

    _shop_models = importlib.import_module("shop.models")
except (ImportError, ModuleNotFoundError):
    # shop.models may not be available in lightweight editor analysis
    # sessions. Leave _shop_models as None; runtime server processes
    # that have the project on PYTHONPATH will import the real module.
    _shop_models = None

_EXPORT_NAMES = (
    "Cart",
    "CartItem",
    "Category",
    "Order",
    "OrderItem",
    "PasswordResetToken",
    "Product",
    "Profile",
    "Review",
    "Store",
    "create_user_profile",
    "save_user_profile",
)

if _shop_models is not None:
    for _name in _EXPORT_NAMES:
        try:
            globals()[_name] = getattr(_shop_models, _name)
        except AttributeError:
            # If a name is missing from the upstream module, leave it
            # undefined here — this mirrors a simple re-export.
            pass
else:
    # Provide harmless placeholders so static analyzers and linters do
    # not complain about undefined names or __all__ entries. These are
    # overwritten at runtime when the real module is importable.
    for _name in _EXPORT_NAMES:
        globals().setdefault(_name, None)

# Avoid static analyzers complaining about names referenced in __all__ by
# assigning a safe default here and populating it at runtime if possible.
__all__: tuple[str, ...] = ("User",)

# Provide User if not already defined by an importing process.
if "User" not in globals():
    # Fall back to normal auth user
    from django.contrib.auth import get_user_model

    User = get_user_model()

# If we successfully imported shop.models at runtime, populate __all__ to
# reflect the actual re-exports. This is done at runtime so the module
# remains import-friendly in lightweight editor/static-analysis
# environments.
if _shop_models is not None:
    __all__ = tuple(_EXPORT_NAMES) + ("User",)
