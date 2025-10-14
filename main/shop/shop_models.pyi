"""Top-level typing stubs for editor/static analysis.

These permissive stubs allow imports like `from shop_models import Profile`
in test scripts and developer utilities without requiring the Django
runtime. They are only used by static analyzers and editors.
"""

from typing import Any, Iterable, Protocol, TypeVar

# Use a covariant type variable for manager return types so Protocol is valid.
# Pylint expects covariant type variables to be named with a `_co` suffix.
T_co = TypeVar("T_co", covariant=True)

class ManagerProtocol(Protocol[T_co]):
    """Minimal protocol describing commonly-used Django manager methods.

    The goal is to provide just enough surface area for static analyzers
    (mypy/pylint) to understand common calls like .filter(), .get(),
    .create(), .all(), .count(), and .latest(). This intentionally
    does not try to mirror Django's Manager API completely.
    """

    def filter(self, *args: Any, **kwargs: Any) -> Iterable[T_co]: ...
    def get(self, *args: Any, **kwargs: Any) -> T_co: ...
    def create(self, *args: Any, **kwargs: Any) -> T_co: ...
    def all(self) -> Iterable[T_co]: ...
    def count(self) -> int: ...
    def latest(self, *args: Any, **kwargs: Any) -> T_co: ...

class Profile:
    """Permissive stub for the Profile model used by static analysis."""

    user: Any
    role: str
    # Django models provide a manager and DoesNotExist exception class.
    objects: ManagerProtocol["Profile"]
    DoesNotExist: Any

class Product:
    """Permissive stub for the Product model used by static analysis."""

    id: Any
    name: Any
    price: Any
    description: Any
    store: Any
    quantity: Any
    image: Any
    def save(self) -> None: ...
    objects: ManagerProtocol["Product"]
    DoesNotExist: Any

class Store:
    """Permissive stub for the Store model used by static analysis."""

    id: Any
    name: Any
    vendor: Any
    is_active: Any
    objects: ManagerProtocol["Store"]
    DoesNotExist: Any

class Order:
    """Permissive stub for the Order model used by static analysis."""

    order_id: Any
    buyer: Any
    total_amount: Any
    shipping_address: Any
    items: Any
    objects: ManagerProtocol["Order"]
    DoesNotExist: Any

class OrderItem:
    """Permissive stub for the OrderItem model used by static analysis."""

    id: Any
    order: Any
    product: Any
    quantity: Any
    price: Any
    total_price: Any
    objects: ManagerProtocol["OrderItem"]
    DoesNotExist: Any

class Review:
    """Permissive stub for the Review model used by static analysis."""

    id: Any
    product: Any
    user: Any
    rating: Any
    comment: Any
    is_verified: Any
    created_at: Any
    objects: ManagerProtocol["Review"]
    DoesNotExist: Any

__all__ = [
    "Profile",
    "Product",
    "Store",
    "Order",
    "OrderItem",
    "Review",
]
