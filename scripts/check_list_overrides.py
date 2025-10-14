"""Small helper: print the list-mode image chosen for a few products.

This is a read-only diagnostic script intended to be run from the repo root.
It intentionally performs imports after configuring Django. To keep linters
happy we put runtime imports inside ``main()`` and add focused pylint
disables only where necessary.
"""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    """Bootstrap Django and print the list-mode image chosen for a few PKs.

    This function is intentionally performing imports after configuring
    Django so it can be used as a standalone read-only script.
    """

    # Mirror manage.py: add main/ on sys.path so imports like `shop` work
    sys.path.insert(0, str(ROOT / "main"))
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "ecommerce_project.settings",
    )

    # Local import after env setup
    import django  # type: ignore  # pylint: disable=import-outside-toplevel

    django.setup()

    # Imports that require Django to be configured.
    # The pylint disable is on the line above to keep the import line short.
    # pylint: disable=import-outside-toplevel
    from main.shop.templatetags.product_images import product_image
    from shop.models import Product  # pylint: disable=import-outside-toplevel

    # Query a few known product PKs and show the list-mode image chosen.
    product_pks = [19, 20, 21]
    # pylint: disable=no-member
    for p in Product.objects.filter(
        pk__in=product_pks,
    ):
        chosen = product_image(p, "list")
        print(f"{p.pk}: {chosen}")


if __name__ == "__main__":
    main()
