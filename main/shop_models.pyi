from typing import Any, Iterable, Protocol, TypeVar

# Canonical permissive stubs used by editor/type-checkers. These mirror
# the minimal shapes used at runtime so static analysis doesn't raise false
# positives for common Django patterns (e.g. .objects, DoesNotExist).
T = TypeVar("T", covariant=True)

class ManagerProtocol(Protocol[T]):
    def filter(self, *args: Any, **kwargs: Any) -> Iterable[T]: ...
    def get(self, *args: Any, **kwargs: Any) -> T: ...
    def create(self, *args: Any, **kwargs: Any) -> T: ...
    def all(self) -> Iterable[T]: ...
    def count(self) -> int: ...
    def latest(self, *args: Any, **kwargs: Any) -> T: ...

class Profile:
    user: Any
    role: Any
    objects: ManagerProtocol["Profile"]
    DoesNotExist: Any

class Product:
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
    id: Any
    name: Any
    vendor: Any
    is_active: Any
    objects: ManagerProtocol["Store"]
    DoesNotExist: Any

class Order:
    order_id: Any
    buyer: Any
    total_amount: Any
    shipping_address: Any
    items: Any
    objects: ManagerProtocol["Order"]
    DoesNotExist: Any

class OrderItem:
    id: Any
    order: Any
    product: Any
    quantity: Any
    price: Any
    total_price: Any
    objects: ManagerProtocol["OrderItem"]
    DoesNotExist: Any

class Review:
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
    id: Any
    user: Any
    items: Any
    objects: Any
    DoesNotExist: Any

class User:
    id: Any
    username: Any
    email: Any
    password: Any
    objects: Any
    DoesNotExist: Any

class PasswordResetToken:
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
