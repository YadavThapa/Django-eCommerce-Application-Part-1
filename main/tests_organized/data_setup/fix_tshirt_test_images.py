#!/usr/bin/env python3
"""Create and assign SVG test images for T-shirt and a generic product.

This script is intended for local test-data setup during development. It
performs a runtime Django setup and updates Product.image fields with
generated SVG files under ``media/product_images``. Pylint import-order and
name conventions are respected in this file.
"""

import os

# Standard-library import placed before third-party imports to satisfy
# linting rules.
from pathlib import Path

# The file performs runtime Django setup and uses ORM attributes that
# static analyzers can't always see. Silence those analyzer false
# positives while keeping runtime behavior unchanged.
# pylint: disable=wrong-import-position,import-outside-toplevel,
# pylint: disable=no-member,no-name-in-module
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce_project.settings")
django.setup()

from main.shop.shop_models import Product  # noqa: E402  # type: ignore[attr-defined]


def create_tshirt_svg():
    """Create a proper T-shirt image"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg width="400" height="300" viewBox="0 0 400 300"
    xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="tshirtGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#3498db;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#2980b9;stop-opacity:1" />
        </linearGradient>
    </defs>

    <!-- Background -->
    <rect width="400" height="300" fill="url(#tshirtGrad)" rx="10"/>

    <!-- T-shirt Shape -->
    <path d="M140 100 L160 80 L240 80 L260 100 L260 120 L240 120"
        " L240 220 L160 220 L160 120 L140 120 Z"
        fill="#ecf0f1" stroke="#bdc3c7" stroke-width="2"/>

    <!-- Neck -->
    <ellipse cx="200" cy="80" rx="15" ry="8" fill="#ecf0f1"/>

    <!-- T-shirt Details -->
    <rect x="170" y="130" width="60" height="4" fill="#3498db" opacity="0.3"/>
    <rect x="170" y="140" width="40" height="4" fill="#3498db" opacity="0.3"/>

    <!-- Size Label -->
    <circle cx="350" cy="50" r="20" fill="#e74c3c"/>
    <text x="350" y="55" font-family="Arial" font-size="14" font-weight="bold"
          text-anchor="middle" fill="white">M</text>

    <!-- Product Label -->
    <text x="200" y="260" font-family="Arial, sans-serif" font-size="18"
          font-weight="bold" text-anchor="middle" fill="white">
        Premium T-Shirt
    </text>
    <text x="200" y="280" font-family="Arial, sans-serif" font-size="12"
          text-anchor="middle" fill="white" opacity="0.8">
        100% Cotton
    </text>
</svg>"""


def create_test_product_svg():
    """Create a generic product image"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg width="400" height="300" viewBox="0 0 400 300"
    xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="productGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#9b59b6;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#8e44ad;stop-opacity:1" />
        </linearGradient>
    </defs>

    <!-- Background -->
    <rect width="400" height="300" fill="url(#productGrad)" rx="10"/>

    <!-- Product Box -->
    <rect x="120" y="90" width="160" height="120" fill="#ecf0f1" rx="10"
          stroke="#bdc3c7" stroke-width="2"/>

    <!-- Product Icon -->
    <circle cx="200" cy="150" r="30" fill="#9b59b6" opacity="0.3"/>
    <rect x="185" y="135" width="30" height="30" fill="white" rx="5"/>
    <circle cx="200" cy="150" r="8" fill="#9b59b6"/>

    <!-- Quality Badge -->
    <polygon points="350,30 370,50 350,70 330,50" fill="#f39c12"/>
    <text x="350" y="55" font-family="Arial" font-size="10" font-weight="bold"
          text-anchor="middle" fill="white">✓</text>

    <!-- Product Label -->
    <text x="200" y="240" font-family="Arial, sans-serif" font-size="18"
          font-weight="bold" text-anchor="middle" fill="white">
        Quality Product
    </text>
    <text x="200" y="260" font-family="Arial, sans-serif" font-size="12"
          text-anchor="middle" fill="white" opacity="0.8">
        Premium Quality
    </text>
</svg>"""


# Create the image files
media_dir = Path("media/product_images")
media_dir.mkdir(parents=True, exist_ok=True)

# Create T-shirt image
TSHIRT_SVG = create_tshirt_svg()
with open(media_dir / "tshirt_proper.svg", "w", encoding="utf-8") as f:
    f.write(TSHIRT_SVG)

# Create test product image
TEST_PRODUCT_SVG = create_test_product_svg()
with open(media_dir / "test_product_proper.svg", "w", encoding="utf-8") as f:
    f.write(TEST_PRODUCT_SVG)

# Update the products
try:
    tshirt_product = Product.objects.get(name="T-shirt")
    tshirt_product.image = "product_images/tshirt_proper.svg"
    tshirt_product.save()
    print("✅ Updated T-shirt with proper clothing image")
except Product.DoesNotExist:
    print("❌ T-shirt product not found")

try:
    test_product = Product.objects.get(name="Test Product")
    test_product.image = "product_images/test_product_proper.svg"
    test_product.save()
    print("✅ Updated Test Product with proper generic product image")
except Product.DoesNotExist:
    print("❌ Test Product not found")

print("🎨 Created and assigned proper product images!")
