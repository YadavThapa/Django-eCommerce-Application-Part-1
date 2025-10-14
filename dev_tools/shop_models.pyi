"""Lightweight runtime stubs for the shop models used by editors/type-checkers.

These permissive .pyi shapes mirror the minimal attributes used at runtime so
static analyzers don't raise false positives for common Django patterns
(for example: ``.objects`` and ``DoesNotExist``).
"""

from typing import Any, Iterable, Protocol, TypeVar

# Use a covariant name for the TypeVar to match pylint conventions.
T_co = TypeVar("T_co", covariant=True)

class ManagerProtocol(Protocol[T_co]):
    """Protocol describing a minimal Django-like manager used in tests/stubs.

    Methods mirror a very small subset of Django's Manager API needed for
    lightweight static checks.
    """

    def filter(self, *args: Any, **kwargs: Any) -> Iterable[T_co]:
        """Return an iterable of matching model instances."""

    def get(self, *args: Any, **kwargs: Any) -> T_co:
        """Return a single model instance matching the query."""

    def create(self, *args: Any, **kwargs: Any) -> T_co:
        """Create and return a new model instance."""

    def all(self) -> Iterable[T_co]:
        """Return all instances for the manager."""

    def count(self) -> int:
        """Return the number of instances in the queryset/manager."""

    def latest(self, *args: Any, **kwargs: Any) -> T_co:
        """Return the latest instance according to a date field."""

class Profile:
    """Stub for a user profile attached to Django's User model."""

    user: Any
    role: Any
    objects: ManagerProtocol["Profile"]
    DoesNotExist: Any

class Product:
    """Minimal Product stub exposing attributes used in templates and tests."""

    id: Any
    name: Any
    price: Any
    description: Any
    store: Any
    quantity: Any
    image: Any

    def save(self) -> None:
        """Persist the product instance (stub).

        This is a no-op in the type stub but documents the expected
        behaviour for static analyzers.
        """
    pass

    objects: ManagerProtocol["Product"]
    DoesNotExist: Any

class Store:
    """Stub representing a vendor store."""

    id: Any
    name: Any
    vendor: Any
    is_active: Any

    objects: ManagerProtocol["Store"]
    DoesNotExist: Any

class Order:
    """Order stub with the primary attributes referenced in code/tests."""

    order_id: Any
    buyer: Any
    total_amount: Any
    shipping_address: Any
    items: Any

    objects: ManagerProtocol["Order"]
    DoesNotExist: Any

class OrderItem:
    """Individual order item stub."""

    id: Any
    order: Any
    product: Any
    quantity: Any
    price: Any
    total_price: Any

    objects: ManagerProtocol["OrderItem"]
    DoesNotExist: Any

class Review:
    """Product review stub used by templates and tests."""

    id: Any
    product: Any
    user: Any
    rating: Any
    comment: Any
    is_verified: Any
    created_at: Any

    objects: ManagerProtocol["Review"]
    DoesNotExist: Any

# Common test/dev stubs
class Cart:
    """Shopping cart stub (session or DB-backed shapes)."""

    id: Any
    user: Any
    items: Any
    objects: Any
    DoesNotExist: Any

class User:
    """Lightweight User stub with common attributes used in tests."""

    id: Any
    username: Any
    email: Any
    password: Any
    objects: Any
    DoesNotExist: Any

class PasswordResetToken:
    """Stub for a password reset token record used in tests and utilities."""

    id: Any
    user: Any
    token: Any
    created_at: Any
    objects: Any
    DoesNotExist: Any

timezone: Any

__all__ = [
    "Profile",
    "Product",
    "Store",
    "Order",
    "OrderItem",
    "Review",
]
