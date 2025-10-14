#!/usr/bin/env python3
"""
Comprehensive check of all product images to ensure they're using the
template tag correctly.

This script is a lightweight maintenance utility. To allow importing
the module in editor sessions without side-effects it configures Django
and imports the app-specific modules at runtime inside ``main()``.
"""

import os


def main() -> None:
    """Run the comprehensive product image audit.

    Configures Django, loads the product model and the template tag,
    then prints a per-product status line and a summary count.
    """
    # Configure Django only when running the script directly so the
    # module can be imported by tooling without importing Django.
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "ecommerce_project.settings",
    )

    # These imports are intentionally performed at runtime after Django is
    # configured. Static analyzers (pylint) will normally warn about
    # imports inside functions; disable that check for this region.
    # pylint: disable=import-outside-toplevel
    import django  # type: ignore

    django.setup()

    # Import app-level helpers after Django is configured. Some editors
    # and static analyzers can't resolve Django app modules (they may
    # lack package stubs or be reachable only via Django's app path),
    # so we import at runtime and use ``type: ignore`` to silence
    # spurious analyzer errors.
    from shop.models import Product  # type: ignore[import]
    from shop.templatetags.product_images import product_image  # type: ignore[import]

    # Re-enable the import-outside-toplevel check for the rest of the file.
    # pylint: enable=import-outside-toplevel

    print("=== COMPREHENSIVE PRODUCT IMAGE CHECK ===")

    # The ORM attributes are dynamically provided by Django; pylint and
    # other static checkers may warn about 'no-member'. Disable that
    # check for the ORM usage below (no runtime effect).
    # pylint: disable=no-member
    products = Product.objects.all().order_by("name")
    for product in products:
        image_url = product_image(product)
        store_name = product.store.name if product.store else "No Store"
        category_name = product.category.name if product.category else "No Category"

        # Check if it's using a good external image or falling back to default
        if "unsplash.com" in image_url:
            status = "✅ Unsplash"
        elif "static" in image_url:
            status = "🟡 Static"
        elif image_url.endswith("svg"):
            status = "❌ SVG placeholder"
        else:
            status = "🟡 Other"

        # Keep each string literal below the line-length limit by
        # concatenating short f-strings.
        print(
            f"{product.name:25} | "
            f"{store_name:15} | "
            f"{category_name:12} | {status}"
        )

    # Re-enable the pylint check for the remainder of the file.
    # pylint: enable=no-member

    # Summary (split into two prints to keep lines short).
    print()
    print("📊 Total products checked:", products.count())
    print("✅ = High-quality Unsplash image")
    print("🟡 = Static/other image")
    print("❌ = Placeholder/problematic image")


if __name__ == "__main__":
    main()
