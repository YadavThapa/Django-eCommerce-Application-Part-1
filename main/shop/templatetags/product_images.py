"""shop.templatetags.product_images
Centralized product image selection utility for templates.

Usage in templat    if 'dumbbell' in name or 'dumbbells' in name:
        return (
            'https://images.unsplash.com/photo-1517963879433-6ad2b056d712'
            '?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'
        )    {% load product_images %}
    <img src="{% product_image product %}" alt="...">

Logic:
 - If product.image is set and file exists on disk under MEDIA_ROOT,
     return product.image.url
 - Otherwise, pick a curated static image based on keywords found in
     product.name
 - If no keyword matches, return a default static product image
"""

import os

from django import template
from django.conf import settings

register = template.Library()

# Optional homepage overrides: map specific product IDs to a curated image URL.
# This is a small, explicit, and reversible override used only for the featured
# products shown on the home page so we can ensure the visuals match the
# curated design even when an uploaded media file exists but is not the desired
# hero image.
_HOMEPAGE_IMAGE_OVERRIDES = {
    # product id: static image path relative to STATIC_URL
    20: settings.STATIC_URL + "images/featured/dumbbells_set.jpg",
    19: settings.STATIC_URL + "images/featured/yoga_mat.jpg",
    21: settings.STATIC_URL + "images/featured/running_shoes.jpg",
    15: settings.STATIC_URL + "images/featured/cooking_masterclass.jpg",
}


def _media_file_exists(image_field):
    """Return True if the ImageFieldFile points to an existing file on disk."""
    if not image_field:
        return False
    # image_field.name is the relative path inside MEDIA_ROOT
    name = getattr(image_field, "name", "")
    if not name:
        return False
    # Treat known placeholder/default filenames as missing so templates
    # fall back to curated images. Many placeholder uploads are named
    # like '14_product_placeholder.svg' or '6_product_default.jpg'.
    if "product_placeholder" in name or "product_default" in name:
        return False
    path = os.path.join(settings.MEDIA_ROOT, name)
    if not os.path.exists(path):
        return False

    # If the uploaded file is an SVG icon or very small file, treat it as a
    # placeholder (many default/icon uploads are small SVGs). This forces the
    # templates to use curated static or external fallbacks that match product
    # semantics better (e.g., blender, coffee maker, garden tools).
    try:
        _, ext = os.path.splitext(path)
        ext = ext.lower()
        if ext == ".svg":
            return False
        size = os.path.getsize(path)
        # Treat files smaller than 15KB as likely placeholders
        if size < 15 * 1024:
            return False
    except OSError:
        # Filesystem access errors (missing file, permissions) should be
        # treated as 'no media file'. Narrowly catch OSError instead of
        # all Exceptions.
        return False

    return True


@register.simple_tag
def product_image(product, mode=None):
    """Return a URL (absolute or static) for the product's image.

    Prefer uploaded media when it actually exists on disk. Otherwise return a
    curated static image or external image URL based on product naming
    heuristics.
    """
    # Only apply the homepage/list overrides when the caller explicitly
    # indicates this is a list rendering (mode == 'list'). This keeps other
    # places (detail pages, featured widgets) using the normal heuristics.
    try:
        pid = int(getattr(product, "id", 0) or 0)
    except (TypeError, ValueError):
        # int() may raise TypeError if given None or a non-convertible type,
        # or ValueError for invalid string values; treat these as missing id.
        pid = 0
    if mode == "list" and pid in _HOMEPAGE_IMAGE_OVERRIDES:
        return _HOMEPAGE_IMAGE_OVERRIDES[pid]

    # Prefer valid uploaded image
    img_field = getattr(product, "image", None)

    if _media_file_exists(img_field):
        # Use the storage-backed URL (this will be MEDIA_URL + path)
        try:
            return img_field.url
        except AttributeError:
            # If the image field doesn't expose a URL for some reason,
            # fall back to static heuristics.
            pass

    # Lowercase name for heuristics
    name = (getattr(product, "name", "") or "").lower()

    # Mapping heuristics (mirrors previous template logic)
    if "headphone" in name or "headphones" in name:
        return (
            "https://images.unsplash.com/photo-1505740420928-5e560c06d30e"
            "?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
        )
    if any(
        k in name
        for k in (
            "smartphone",
            "phone",
            "mobile",
            "iphone",
            "samsung",
        )
    ):
        return (
            "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9"
            "?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
        )
    if any(k in name for k in ("laptop", "computer", "macbook")):
        return (
            "https://images.unsplash.com/photo-1496181133206-80ce9b88a853"
            "?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
        )
    # Running shoes / sneakers - include common variants
    if any(
        k in name
        for k in (
            "running",
            "running shoe",
            "running shoes",
            "sneaker",
            "sneakers",
            "shoe",
            "shoes",
        )
    ):
        return (
            "https://images.unsplash.com/photo-1600180758891-8a9a1a6f3b5f"
            "?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
        )
    if "dumbbell" in name or "dumbbells" in name:
        return (
            "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b"
            "?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
        )
    # Yoga-related: prefer mat images when mentioned
    if ("yoga" in name and "mat" in name) or any(
        k in name for k in ("yoga mat", "yoga")
    ):
        return (
            "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b"
            "?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
        )
    if "tennis" in name and "racket" in name:
        return (
            "https://images.unsplash.com/photo-1551698618-1dfe5d97d256"
            "?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
        )
    if "basketball" in name:
        return (
            "https://images.unsplash.com/photo-1546519638-68e109498ffc"
            "?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
        )
    if "football" in name and "american" not in name:
        return (
            "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa"
            "?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
        )
    if "t-shirt" in name or "tshirt" in name or name == "t-shirt":
        return (
            "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab"
            "?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
        )
    if "jeans" in name:
        return (
            "https://images.unsplash.com/photo-1542272604-787c3835535d"
            "?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
        )
    if "sneaker" in name and "running" not in name:
        return (
            "https://images.unsplash.com/photo-1549298916-b41d501d3772"
            "?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
        )
    if "python" in name and "programming" in name:
        return (
            "https://images.unsplash.com/photo-1515879218367-8466d910aaa4"
            "?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
        )
    if "web" in name and "development" in name:
        return (
            "https://images.unsplash.com/photo-1461749280684-dccba630e2f6"
            "?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
        )
    if "data" in name and "science" in name:
        return (
            "https://images.unsplash.com/photo-1551288049-bebda4e38f71"
            "?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
        )
    if "cooking" in name and "masterclass" in name:
        return (
            "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136"
            "?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
        )
    if "history" in name and "nepal" in name:
        return (
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4"
            "?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
        )
    if "novel" in name and "collection" in name:
        return (
            "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d"
            "?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
        )
    if "coffee" in name and "maker" in name:
        return (
            "https://images.unsplash.com/photo-1509042239860-f550ce710b93"
            "?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
        )
    if "blender" in name:
        return (
            "https://images.unsplash.com/photo-1553062407-98eeb64c6a62"
            "?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
        )
    if "garden" in name and "tools" in name:
        return (
            "https://images.unsplash.com/photo-1523348837708-15d4a09cfac2"
            "?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
        )

    # Watch and smartwatch handling
    if any(
        k in name
        for k in (
            "watch",
            "smartwatch",
            "fitness watch",
            "smart watch",
        )
    ):
        return (
            "https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d"
            "?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
        )

    # Wireless and Bluetooth devices
    if any(
        k in name
        for k in (
            "wireless",
            "bluetooth",
            "headphones",
            "earbuds",
        )
    ):
        return (
            "https://images.unsplash.com/photo-1505740420928-5e560c06d30e"
            "?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
        )

    # Cotton and fabric products
    if any(k in name for k in ("cotton", "premium cotton", "fabric")):
        return (
            "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab"
            "?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
        )

    # Default high-quality fallback
    return (
        "https://images.unsplash.com/photo-1560472354-b33ff0c44a43"
        "?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
    )


# End of shop/templatetags/product_images.py
