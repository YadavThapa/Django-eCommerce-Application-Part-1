"""Simple in-process smoke tests using Django's test Client.

Checks:
- GET / (homepage)
- GET /shop/ (product list) if present
- GET product detail for an existing product ID
- GET cart page and checkout page

This runs using main.ecommerce_project.settings (Postgres) by default.
"""

from pathlib import Path
import sys
import os
from typing import List, Tuple, Any

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    """Run in-process smoke tests against Postgres-backed settings.

    We modify sys.path and set environment variables at runtime so imports
    that depend on Django happen after the settings are configured.
    """
    # Ensure project root and main package are importable
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(ROOT / "main"))

    # Ensure the script uses the Postgres-aware settings
    settings_mod = "main.ecommerce_project.settings"
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_mod)
    os.environ.setdefault("DB_ENGINE", "postgres")
    os.environ.setdefault("DB_NAME", "ecommerce_db")
    os.environ.setdefault("DB_USER", "postgres")
    os.environ.setdefault("DB_PASSWORD", "postgres")
    os.environ.setdefault("DB_HOST", "127.0.0.1")
    os.environ.setdefault("DB_PORT", "15433")

    # Django imports are performed here because they require the
    # DJANGO_SETTINGS_MODULE to be set first. Linters may warn about
    # import-outside-toplevel but this is intentional for this script.
    # pylint: disable=import-outside-toplevel
    import django

    django.setup()
    from django.test import Client
    from django.apps import apps

    # pylint: enable=import-outside-toplevel

    client = Client()
    results: List[Tuple[str, Any, Any]] = []

    # 1. Homepage
    resp = client.get("/")
    results.append(("homepage", resp.status_code, resp.get("Location")))

    # 2. Try product list - common paths: /products/, /shop/, /shop/products/
    paths = [
        "/products/",
        "/shop/",
        "/products",
        "/shop",
        "/",
    ]
    for p in paths:
        r = client.get(p)
        if r.status_code == 200 and b"product" in r.content.lower():
            results.append(("product_list", p, r.status_code))
            break
        results.append(("product_list_probe", p, r.status_code))

    # 3. Product detail - pick an existing product id from DB
    product_model = apps.get_model("shop", "Product")
    prod = product_model.objects.first()
    if prod is not None:
        # Guess common detail URL patterns
        detail_paths = [
            f"/product/{prod.pk}/",
            f"/products/{prod.pk}/",
            f"/shop/product/{prod.pk}/",
            f"/shop/{prod.pk}/",
        ]
        for dp in detail_paths:
            r = client.get(dp)
            results.append(("product_detail_probe", dp, r.status_code))
            if r.status_code == 200:
                break
        # record product name
        results.append(("product_present", prod.pk, prod.name))
    else:
        results.append(("no_products", None, None))

    # 4. Cart and checkout pages - common paths
    for p in [
        "/cart/",
        "/cart",
        "/checkout/",
        "/checkout",
        "/shop/checkout/",
    ]:
        r = client.get(p)
        results.append(("probe", p, r.status_code))

    # Print results
    for row in results:
        print(row)

    # exit with non-zero if any 5xx
    if any((isinstance(r[2], int) and r[2] >= 500) for r in results):
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
