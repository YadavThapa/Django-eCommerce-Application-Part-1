#!/usr/bin/env python3
"""Implementation: check final product-store assignments.

This is a direct copy of the earlier script, placed under the
validation package for clearer organization.
"""

import os
import django  # type: ignore


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "ecommerce_project.settings",
)


def main() -> None:
    """Print store product assignments and potential mismatches."""
    print("=== FINAL STORE ASSIGNMENTS ===")

    django.setup()
    # Imported at runtime after django.setup() — static analyzers often
    # cannot infer model attributes (reverse relations). Silence a
    # specific mypy error where the `Store` type appears to have no
    # `products` attribute.
    # pylint: disable=import-outside-toplevel
    from main.shop.models import Store  # type: ignore[import]

    # pylint: enable=import-outside-toplevel

    # pylint: disable=no-member
    for store in Store.objects.filter(is_active=True).order_by("name"):
        # type: ignore[attr-defined]
        products = store.products.all()  # type: ignore[attr-defined]
        if products.exists():
            print(f"\n{store.name}:")
            for product in products:
                category_name = (
                    product.category.name if product.category else "No category"
                )
                print(f"  - {product.name} ({category_name})")

    print("\n=== POTENTIAL MISMATCHES TO WATCH ===")

    mismatches: list[str] = []

    for store in Store.objects.filter(is_active=True):
        # type: ignore[attr-defined]
        for product in store.products.all():  # type: ignore[attr-defined]
            store_name = store.name.lower()
            category_name = product.category.name.lower() if product.category else ""

            if "sports" in store_name and category_name not in ["sports"]:
                if category_name not in ["electronics"]:
                    part = f"  - {product.name} ({product.category.name})"
                    mismatches.append(part + f" in {store.name}")
            elif "fashion" in store_name and category_name not in ["clothing"]:
                part = f"  - {product.name} ({product.category.name})"
                mismatches.append(part + f" in {store.name}")
            elif "home" in store_name and category_name not in [
                "home & garden",
                "books",
            ]:
                part = f"  - {product.name} ({product.category.name})"
                mismatches.append(part + f" in {store.name}")
            elif "tech" in store_name and category_name not in [
                "electronics",
                "books",
            ]:
                part = f"  - {product.name} ({product.category.name})"
                mismatches.append(part + f" in {store.name}")

    if mismatches:
        print("Found potential mismatches:")
        for m in mismatches:
            print(m)
    else:
        print("No obvious mismatches found! ✅")


if __name__ == "__main__":
    main()
