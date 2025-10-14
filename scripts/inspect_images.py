#!/usr/bin/env python3
"""Inspect product image URLs chosen by the product_images templatetag.

This script is read-only and will only print product IDs, names,
chosen image URL, and whether an uploaded media file was considered valid.
"""

import os
import sys
from pathlib import Path

# Ensure `main/` (the project package) is on sys.path like manage.py does.
ROOT = Path(__file__).resolve().parent.parent
# Add the `main/` package (where the Django project lives) to sys.path
# — this mirrors the behavior in manage.py so imports like `shop` work.
sys.path.insert(0, str(ROOT / "main"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce_project.settings")


def main() -> None:
    """Run the inspection. Imports Django-dependent modules at runtime."""
    # Configure Django (must happen before importing project modules)
    import django  # type: ignore  # pylint: disable=import-outside-toplevel

    django.setup()

    # Runtime-only imports: these must occur after Django is configured.
    # pylint: disable=import-outside-toplevel
    # pylint: disable=import-outside-toplevel
    from shop.models import Product
    from shop.templatetags.product_images import _media_file_exists, product_image

    # The Product model has a dynamic manager added at runtime; pylint may
    # warn about 'no-member' for Product.objects — silence that check only
    # for this loop.
    for p in Product.objects.all()[:50]:  # pylint: disable=no-member
        try:
            image_url = product_image(p)
        except Exception as exc:  # pylint: disable=broad-except
            image_url = f"<error: {exc}>"
        is_uploaded = _media_file_exists(getattr(p, "image", None))
        print(f"{p.pk}: {p.name} -> {image_url} (uploaded:{is_uploaded})")


if __name__ == "__main__":
    main()
