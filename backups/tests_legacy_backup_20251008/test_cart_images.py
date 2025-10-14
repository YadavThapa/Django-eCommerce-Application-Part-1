#!/usr/bin/env python3

import os

import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce_project.settings")
from django.test import Client  # noqa: E402
from main.shop.models import Product  # noqa: E402

django.setup()
import json  # noqa: E402


def test_cart_images():
    """Test cart image URLs"""
    print("🔍 Testing Cart Image URLs")
    print("=" * 50)

    # Get first product
    product = Product.objects.first()
    if not product:
        print("❌ No products found!")
        return

    print(f"📦 Product: {product.name}")
    print(f"🏪 Store: {product.store.name}")
    print(f"🖼️ Image field: {product.image}")

    if product.image:
        print(f"📸 Image URL: {product.image.url}")
        print(f"📁 Image path: {product.image.path}")

        # Check if file exists
        if os.path.exists(product.image.path):
            print("✅ Image file exists on disk")
        else:
            print("❌ Image file NOT found on disk")
    else:
        print("❌ No image assigned to product")

    # Test cart API
    print("\n🛒 Testing Cart API")
    print("-" * 30)

    client = Client()

    # Add product to cart
    add_response = client.post(f"/cart/add/{product.id}/", {"quantity": 1})
    print(f"➕ Add to cart status: {add_response.status_code}")

    # Get cart API
    api_response = client.get("/cart/api/")
    print(f"📡 API response status: {api_response.status_code}")

    if api_response.status_code == 200:
        data = json.loads(api_response.content)
        print(f"📊 Items in cart: {len(data.get('items', []))}")

        for i, item in enumerate(data.get("items", [])):
            print(f"\n📝 Item {i + 1}:")
            print(f"   Name: {item['product']['name']}")
            print(f"   Price: ${item['product']['price']}")
            print(f"   Image URL: {item['product']['image']}")

            if item["product"]["image"]:
                # Check if it's a relative or absolute URL
                if item["product"]["image"].startswith("/"):
                    print("   🔗 Relative URL (needs MEDIA_URL prefix)")
                else:
                    print("   🔗 Full URL")
            else:
                print("   ❌ No image URL")
    else:
        print(f"❌ API Error: {api_response.content}")


if __name__ == "__main__":
    test_cart_images()
