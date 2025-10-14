"""Quick check to print MEDIA_ROOT and a sample product image path.

Run this from the repo root; it configures Django and then queries a single
Product instance to show its image path and existence on disk.
"""

import os

import django

# Configure Django settings before importing ORM modules
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "main.ecommerce_project.settings",
)
django.setup()


def main() -> None:
    """Print MEDIA_ROOT and an example product image path if available."""

    from django.conf import settings
    from django.apps import apps

    print("MEDIA_ROOT:", settings.MEDIA_ROOT)
    Product = apps.get_model("shop", "Product")
    prod = Product.objects.first()
    if prod:
        print("Sample product:", prod.pk, prod.name)
        try:
            path = prod.image.path
            print("Image path:", path)
            print("Exists:", os.path.exists(path))
        except AttributeError as exc:
            # prod.image may be a string field or empty; report succinctly
            print("Image path not available:", exc)
    else:
        print("No products in DB")


if __name__ == "__main__":
    main()
