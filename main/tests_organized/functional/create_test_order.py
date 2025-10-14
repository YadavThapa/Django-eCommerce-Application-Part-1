#!/usr/bin/env python
"""Developer utility: create a small test order used by vendor dashboard.

This script runs Django setup at runtime and imports models afterwards so
static analyzers don't complain about application imports in editor
environments. Use only for local development.
"""

# pylint: disable=import-outside-toplevel

import os
from decimal import Decimal
from typing import Optional


def create_test_order() -> Optional[object]:
    """Create a small test order with a couple of items.

    Returns the created Order instance (runtime Django model) or None on
    error (e.g., missing vendor user).
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.ecommerce_project.settings")
    import django  # type: ignore[import]

    django.setup()

    # Import models after setup so runtime works. Static analyzers may not
    # resolve the Django app layout in the editor environment.
    # pylint: disable=import-error,wrong-import-position,no-member
    from main.shop.models import (
        Order,
        OrderItem,
        Product,
        Store,
    )  # noqa: E402  # type: ignore[import]

    # These Django modules lack stubs in some envs; if you want stricter
    # static typing locally, install `django-stubs` into the venv. Keep
    # runtime imports after django.setup() so the script is usable standalone.
    from django.contrib.auth import get_user_model  # noqa: E402  # type: ignore[import]
    from django.core.exceptions import ObjectDoesNotExist  # noqa: E402  # type: ignore[import]

    User = get_user_model()

    buyer, _ = User.objects.get_or_create(
        username="testbuyer", defaults={"email": "testbuyer@example.com"}
    )

    try:
        vendor = User.objects.get(username="vendor1")
    except ObjectDoesNotExist:
        print("vendor1 user missing; create one before running this script")
        return None

    store = Store.objects.filter(vendor=vendor).first()
    if not store:
        store = Store.objects.create(name="Test Vendor Store", vendor=vendor, is_active=True)

    if not Product.objects.filter(store=store).exists():
        Product.objects.create(
            name="Laptop", price=Decimal("999.99"), quantity=10, store=store
        )
        Product.objects.create(
            name="Mouse", price=Decimal("29.99"), quantity=50, store=store
        )

    products = list(Product.objects.filter(store=store)[:3])

    order = Order.objects.create(buyer=buyer, total_amount=Decimal("0.00"))

    total = Decimal("0.00")
    for idx, product in enumerate(products, start=1):
        qty = idx
        OrderItem.objects.create(order=order, product=product, quantity=qty, price=product.price)
        total += product.price * qty

    order.total_amount = total
    order.save()

    print(f"Created order {order}")
    return order


if __name__ == "__main__":
    create_test_order()
