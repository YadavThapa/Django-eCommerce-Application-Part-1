#!/usr/bin/env python
"""
Script to set up and verify user roles and functionality demonstration.
This will create test users with proper roles and sample data.
"""
import os
import sys

import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce_project.settings")
django.setup()

from django.contrib.auth import get_user_model  # noqa: E402
User = get_user_model()  # noqa: E402
from main.shop.models import Category, Product, Profile, Store  # noqa: E402


# The function intentionally defines names that are also used at module
# level when the script is executed; silence the redefined-name warning.
# No outer-name redefinition expected after main assignment rename.
def create_demo_users():
    """Create demonstration users with proper roles"""
    print("🚀 Setting up demonstration users...")

    # Create or update buyer user
    buyer_user, _ = User.objects.get_or_create(
        username="demo_buyer",
        defaults={
            "email": "buyer@demo.com",
            "first_name": "Demo",
            "last_name": "Buyer",
        },
    )
    buyer_user.set_password("demo123")
    buyer_user.save()

    # Ensure buyer profile
    buyer_profile, _ = Profile.objects.get_or_create(
        user=buyer_user,
        defaults={
            "role": "buyer",
            "phone": "123-456-7890",
            "address": "123 Demo St",
        },
    )
    buyer_profile.role = "buyer"
    buyer_profile.save()

    print(f"✅ Buyer user: {buyer_user.username} (role: {buyer_profile.role})")

    # Create or update vendor user
    vendor_user, _ = User.objects.get_or_create(
        username="demo_vendor",
        defaults={
            "email": "vendor@demo.com",
            "first_name": "Demo",
            "last_name": "Vendor",
        },
    )
    vendor_user.set_password("demo123")
    vendor_user.save()

    # Ensure vendor profile
    vendor_profile, _ = Profile.objects.get_or_create(
        user=vendor_user,
        defaults={
            "role": "vendor",
            "phone": "987-654-3210",
            "address": "456 Vendor Ave",
        },
    )
    vendor_profile.role = "vendor"
    vendor_profile.save()

    print(f"✅ Vendor user: {vendor_user.username} (role: {vendor_profile.role})")

    return buyer_user, vendor_user


def create_demo_data():
    """Create demonstration stores and products"""
    print("🏪 Setting up demonstration data...")

    # Get vendor user
    vendor_user = User.objects.get(username="demo_vendor")

    # Create categories
    categories_data = [
        {
            "name": "Electronics",
            "description": "Electronic devices and gadgets",
        },
        {"name": "Clothing", "description": "Fashion and apparel"},
        {"name": "Books", "description": "Books and literature"},
        {
            "name": "Home & Garden",
            "description": "Home improvement and gardening",
        },
    ]

    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data["name"],
            defaults={"description": cat_data["description"]},
        )
        if created:
            print(f"✅ Created category: {category.name}")

    # Create demo store
    demo_store, created = Store.objects.get_or_create(
        vendor=vendor_user,
        name="Demo Electronics Store",
        defaults={
            "description": "Your one-stop shop for quality electronics and gadgets",
            "is_active": True,
        },
    )
    if created:
        print(f"✅ Created store: {demo_store.name}")

    # Create demo products
    electronics_category = Category.objects.get(name="Electronics")
    clothing_category = Category.objects.get(name="Clothing")

    products_data = [
        {
            "name": "Wireless Bluetooth Headphones",
            "description": "High-quality wireless headphones with noise cancellation",
            "price": 89.99,
            "quantity": 50,
            "category": electronics_category,
        },
        {
            "name": "Smart Fitness Watch",
            "description": "Track your fitness goals with this advanced smartwatch",
            "price": 199.99,
            "quantity": 25,
            "category": electronics_category,
        },
        {
            "name": "Premium Cotton T-Shirt",
            "description": "Comfortable and stylish cotton t-shirt",
            "price": 24.99,
            "quantity": 100,
            "category": clothing_category,
        },
    ]

    for product_data in products_data:
        product, created = Product.objects.get_or_create(
            store=demo_store,
            name=product_data["name"],
            defaults={
                "description": product_data["description"],
                "price": product_data["price"],
                "quantity": product_data["quantity"],
                "category": product_data["category"],
                "is_active": True,
            },
        )
        if created:
            print(f"✅ Created product: {product.name} (${product.price})")


def display_login_info():
    """Display login information for testing"""
    print("\n" + "=" * 60)
    print("🎯 DEMO USERS READY - LOGIN INFORMATION")
    print("=" * 60)
    print("\n👤 BUYER ACCOUNT:")
    print("   Username: demo_buyer")
    print("   Password: demo123")
    print("   Features: Cart, Checkout, Order History, Product Reviews")
    print("   Dashboard: /customer/")

    print("\n🏪 VENDOR ACCOUNT:")
    print("   Username: demo_vendor")
    print("   Password: demo123")
    print("   Features: Store Management, Product Management, Vendor Dashboard")
    print("   Dashboard: /vendor/")

    print("\n🌐 ACCESS THE SITE:")
    print("   URL: http://127.0.0.1:8000/")
    print("   Login: http://127.0.0.1:8000/login/")

    print("\n📋 FUNCTIONALITY TO TEST:")
    print("   ✅ User Registration (with role selection)")
    print("   ✅ Vendor: Create/Edit/Delete Stores")
    print("   ✅ Vendor: Add/Edit/Delete Products")
    print("   ✅ Buyer: Browse Products, Add to Cart")
    print("   ✅ Buyer: Checkout Process")
    print("   ✅ Buyer: Leave Product Reviews")
    print("   ✅ Role-based Navigation")
    print("=" * 60)


def verify_current_functionality():
    """Verify current state of functionality"""
    print("\n🔍 VERIFYING CURRENT FUNCTIONALITY...")

    # Check users and roles
    users = User.objects.all()
    print(f"👥 Total users: {users.count()}")
    for user in users:
        if hasattr(user, "profile") and user.profile:
            print(f"   - {user.username}: {user.profile.role}")
        else:
            print(f"   - {user.username}: No profile")

    # Check stores
    stores = Store.objects.all()
    print(f"🏪 Total stores: {stores.count()}")
    for store in stores:
        print(f"   - {store.name} (Vendor: {store.vendor.username})")

    # Check products
    products = Product.objects.all()
    print(f"📦 Total products: {products.count()}")
    for product in products[:5]:  # Show first 5
        print(f"   - {product.name} (${product.price}) in {product.store.name}")

    # Check categories
    categories = Category.objects.all()
    print(f"🏷️ Total categories: {categories.count()}")
    for category in categories:
        print(f"   - {category.name}")


if __name__ == "__main__":
    print("🎬 DJANGO E-COMMERCE FUNCTIONALITY SETUP")
    print("=" * 50)

    try:
        # Verify current state
        verify_current_functionality()
        # Create demo users
        demo_buyer_user, demo_vendor_user = create_demo_users()

        # Create demo data
        create_demo_data()

        # Show login info
        display_login_info()

        print("\n✅ Setup completed successfully!")
        print("🚀 Start the Django server and test the functionality.")

    except Exception as e:  # pylint: disable=broad-except
        # Top-level script: catch-all here is acceptable for friendly CLI output.
        print(f"❌ Error during setup: {e}")
        sys.exit(1)
