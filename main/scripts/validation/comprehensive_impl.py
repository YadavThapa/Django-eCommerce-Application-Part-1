#!/usr/bin/env python3
"""Implementation: comprehensive product image check.

Copied from the scripts implementation to provide a stable import
location under `main.scripts.validation`.
"""

import os


def main() -> None:
    """Run the comprehensive product image audit."""
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "ecommerce_project.settings",
    )

    # Import Django at runtime and configure. Static checkers will flag
    # this as an import outside the module top-level; it's intentional
    # because we must call `django.setup()` first.
    import django  # type: ignore  # pylint: disable=import-outside-toplevel

    django.setup()

    # The model import is runtime-only; silence the 'import-outside-
    # toplevel' warning on the following line.
    # pylint: disable=import-outside-toplevel
    from shop.models import Product  # type: ignore[import]

    # pylint: disable=import-outside-toplevel
    from shop.templatetags.product_images import product_image  # type: ignore[import]

    # pylint: enable=import-outside-toplevel

    print("=== COMPREHENSIVE PRODUCT IMAGE CHECK ===")

    # pylint: disable=no-member
    products = Product.objects.all().order_by("name")
    for product in products:
        image_url = product_image(product)
        store_name = product.store.name if product.store else "No Store"
        category_name = product.category.name if product.category else "No Category"

        if "unsplash.com" in image_url:
            status = "✅ Unsplash"
        elif "static" in image_url:
            status = "🟡 Static"
        elif image_url.endswith("svg"):
            status = "❌ SVG placeholder"
        else:
            status = "🟡 Other"

        # Keep the print line short by splitting the formatted parts.
        left = f"{product.name:25} | {store_name:15} | "
        right = f"{category_name:12} | {status}"
        print(left + right)

    print()
    print("📊 Total products checked:", products.count())


if __name__ == "__main__":
    main()
