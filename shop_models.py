"""Runtime-friendly shim for editor/type checkers and runtime shimming.

This module tries to import the real Django model classes from
``shop.models`` at runtime (after :mod:`django` has been configured).
When the real models can't be imported (for example during static
analysis or outside a configured Django project) permissive local
stub classes are provided so ``from shop_models import Profile`` and
similar imports succeed without side effects. The file intentionally
keeps runtime imports inside a try/except to avoid import-time errors.
"""

from typing import Any

try:  # pragma: no cover - runtime import behavior
    # Prefer the real models when available (after django.setup()).
    from main.shop.models import (
        Profile,
        Product,
        Store,
        Order,
        OrderItem,
        Review,
    )  # type: ignore
except Exception:  # pylint: disable=broad-except
    # Fallback permissive stubs used when the Django ORM isn't importable.
    # Use a narrow pylint disable for this broad except which is a
    # deliberate runtime shim pattern.
    # pylint: disable=broad-except
    class Profile:  # type: ignore
        """Fallback stub for the Profile model used by runtime shims."""

        user: Any
        role: Any
        objects: Any

    class Product:  # type: ignore
        """Fallback stub for the Product model used by runtime shims."""

        id: Any
        name: Any
        price: Any
        description: Any
        store: Any
        quantity: Any
        objects: Any

    class Store:  # type: ignore
        """Fallback stub for the Store model used by runtime shims."""

        id: Any
        name: Any
        vendor: Any
        is_active: Any
        objects: Any

    class Order:  # type: ignore
        """Fallback stub for the Order model used by runtime shims."""

        order_id: Any
        buyer: Any
        total_amount: Any
        shipping_address: Any
        items: Any
        objects: Any

    class OrderItem:  # type: ignore
        """Fallback stub for the OrderItem model used by runtime shims."""

        id: Any
        order: Any
        product: Any
        quantity: Any
        price: Any
        total_price: Any
        objects: Any

    class Review:  # type: ignore
        """Fallback stub for the Review model used by runtime shims."""

        id: Any
        product: Any
        user: Any
        rating: Any
        comment: Any
        is_verified: Any
        created_at: Any
        objects: Any


__all__ = [
    "Profile",
    "Product",
    "Store",
    "Order",
    "OrderItem",
    "Review",
]
