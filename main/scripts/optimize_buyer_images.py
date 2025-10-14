#!/usr/bin/env python3
"""Update all products with optimal realistic images for buyer view.

This maintenance script is intended to be executed manually. It updates
products that match a mapping to a curated static image intended for the
buyer-facing product list.
"""

# Removed unused os import and tightened spacing

# Use the best available realistic images for buyer product display
OPTIMAL_IMAGE_MAPPING = {
    # Books and educational picks: prefer the curated 'history_of_nepal' image
    "The Great Novel Collection": "product_images/14_history_of_nepal.jpg",
    "Web Development Handbook": ("product_images/15_cooking_masterclass.jpg",),
    "Python Programming Guide": "product_images/14_history_of_nepal.jpg",
    "Data Science for Beginners": "product_images/14_history_of_nepal.jpg",
    "History of Nepal": "product_images/14_history_of_nepal.jpg",
    # Cooking and kitchen
    "Cooking Masterclass": "product_images/15_cooking_masterclass.jpg",
    "Coffee Maker": "product_images/15_cooking_masterclass.jpg",
    "Blender": "product_images/15_cooking_masterclass.jpg",
    # Sports equipment
    "Running Shoes": "product_images/21_running_shoes.jpg",
    "Basketball": "product_images/17_basketball.jpg",
    "Football": "product_images/16_football.jpg",
    "Tennis Racket": "product_images/18_tennis_racket.jpg",
    "Yoga Mat": "product_images/19_yoga_mat.jpg",
    "Dumbbells Set": "product_images/20_dumbbells_set.jpg",
    # Clothing - default product images
    "T-shirt": "product_images/1_product_default.jpg",
    "T-Shirt": "product_images/2_product_default.jpg",
    "Jeans": "product_images/3_product_default.jpg",
    "Sneakers": ("product_images/21_running_shoes.jpg",),
    # Electronics
    "Laptop": "product_images/4_product_default.jpg",
    "Smartphone": "product_images/5_product_default.jpg",
    "Headphones": "product_images/6_product_default.jpg",
    # Garden
    "Garden Tools Set": ("product_images/14_history_of_nepal.jpg",),
    # Test products
    "Test Product": "product_images/1_product_default.jpg",
}


def _run_update(Product):
    print("Updating products with optimal realistic images for buyer view...")
    print()

    UPDATED_COUNT = 0
    # The ORM dynamically provides members like ``objects``; disable
    # pylint's ``no-member`` check for the loop below (no runtime effect).
    # pylint: disable=no-member
    for product_name, image_path in OPTIMAL_IMAGE_MAPPING.items():
        try:
            product = Product.objects.get(name=product_name)
            OLD_IMAGE = str(product.image)
            product.image = image_path
            product.save()
            UPDATED_COUNT += 1
            print(f"✅ {product_name}")
            # use multiple args to keep the source line short
            print("   📷", image_path)
            if OLD_IMAGE != image_path:
                print(f"   🔄 Changed from: {OLD_IMAGE}")
            print()
        except Product.DoesNotExist:  # type: ignore[attr-defined]
            # Product not found in the database
            print(f"❌ Product not found: {product_name}")
    # pylint: enable=no-member

    print(
        "🚀 Successfully updated",
        UPDATED_COUNT,
        "products with realistic images!",
    )
    print(
        "💡 All products now use high-quality, realistic images for better "
        "buyer experience."
    )


def main() -> None:
    import django  # type: ignore

    django.setup()
    from shop.models import Product  # type: ignore[import]

    _run_update(Product)


if __name__ == "__main__":
    main()
