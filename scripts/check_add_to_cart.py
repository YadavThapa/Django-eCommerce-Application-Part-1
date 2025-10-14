"""
Quick script to test POST /cart/add/<id>/ returns 303 and Location
points to cart detail. Run from repo root with Django settings available
(e.g. `python scripts/check_add_to_cart.py`).
"""

# flake8: noqa
# pylint: disable=import-outside-toplevel,no-member,wrong-import-position
import os
import sys

# Ensure repo root is on path so the project packages can be imported
HERE = os.path.dirname(os.path.dirname(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce_project.settings")

from typing import Any

import django
from django.test import Client

django.setup()

from shop.models import Product as _Product

# Rebind for static analysis so linters recognize Django ORM attributes
Product: Any = _Product

client = Client()

PRODUCT_ID = 1
try:
    selected_product_id = PRODUCT_ID
    # If pk=1 doesn't exist, pick the first product available
    if not Product.objects.filter(pk=selected_product_id).exists():
        p = Product.objects.first()
        if not p:
            print("No Product found in DB. Please create one first.")
            sys.exit(1)
        selected_product_id = p.pk
except Exception as e:  # pylint: disable=broad-except
    print("Could not inspect Product model (run within Django env):", e)
    sys.exit(1)

print(f"Testing add-to-cart for product id={selected_product_id}")
res = client.post(f"/cart/add/{selected_product_id}/", {"quantity": 1}, follow=False)
print("POST status:", res.status_code)
location = res.get("Location")
print("Location header:", location)

if res.status_code in (303, 302) and location:
    follow_res = client.get(location)
    print("Follow GET status:", follow_res.status_code)
    body = follow_res.content.decode("utf-8")
    found = (
        str(selected_product_id) in body
        or "Add to Cart" in body
        or "Shopping Cart" in body
    )
    print("Cart page contains product id / cart strings:", found)
else:
    print("Did not receive redirect; response body length:", len(res.content))
