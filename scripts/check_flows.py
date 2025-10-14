import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.ecommerce_project.settings")

try:
    import django

    django.setup()
    from django.test import Client
    from django.contrib.auth import get_user_model

    User = get_user_model()

    c = Client()
    print("Attempting login as demo_buyer...")
    resp = c.post(
        "/login/", {"username": "demo_buyer", "password": "demo123"}, follow=True
    )
    print("Login status code:", resp.status_code)

    # Find a product id to add
    from main.shop.models import Product

    product = Product.objects.first()
    if not product:
        print("No product found to add to cart")
        sys.exit(2)
    add_url = f"/cart/add/{product.pk}/"
    print("Posting add-to-cart to", add_url)
    # Do not follow redirects here because some views intentionally return
    # a 303 with a Location header (HttpResponse with Location) which the
    # test client follow logic expects a .url attribute on redirects.
    resp2 = c.post(add_url, follow=False)
    print("Add-to-cart status code:", resp2.status_code)

    # If the view issued a redirect via Location header, follow it manually
    if resp2.status_code in (301, 302, 303, 307, 308) and "Location" in resp2:
        loc = resp2["Location"]
        print("Redirect Location:", loc)
        follow_resp = c.get(loc)
        print("Followed redirect status code:", follow_resp.status_code)
        print("Response snippet:", follow_resp.content[:200].decode(errors="replace"))
    else:
        # print a short snippet of response
        print("Response snippet:", resp2.content[:200].decode(errors="replace"))
except Exception:
    import traceback

    print("Flow check FAILED")
    traceback.print_exc()
    sys.exit(2)
