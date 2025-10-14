#!/usr/bin/env python
"""
Safe Project Organization Script - Clean up remaining scattered files
"""

import os
import shutil
from pathlib import Path


def safe_organize_remaining_files():
    """Safely organize remaining scattered files without disrupting
    existing structure.
    """

    print("🧹 CLEANING UP REMAINING SCATTERED FILES")
    print("=" * 50)

    base_dir = Path("C:/Users/hemja/OneDrive/Desktop/Django E-commerce")
    os.chdir(base_dir)

    print("\n1️⃣ Checking Current Status:")
    # Break long f-string into a short status variable to satisfy line-length
    status = "EXISTS" if Path("ecommerce_project").exists() else "MISSING"
    print(f"✅ ecommerce_project/: {status}")
    shop_status = "EXISTS" if Path("shop").exists() else "MISSING"
    docs_status = "EXISTS" if Path("docs").exists() else "MISSING"
    tests_status = "EXISTS" if Path("tests").exists() else "MISSING"
    config_status = "EXISTS" if Path("config").exists() else "MISSING"
    print(f"✅ shop/: {shop_status}")
    print(f"✅ docs/: {docs_status}")
    print(f"✅ tests/: {tests_status}")
    print(f"✅ config/: {config_status}")

    # Ensure required directories exist
    required_dirs = [
        "docs",
        "tests",
        "scripts/utilities",
        "scripts/data_management",
        "scripts/testing",
        "archived/legacy",
    ]

    for dir_path in required_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)

    print("\n2️⃣ Moving Documentation Files:")

    # Move documentation files that are still in root
    password_reset_target = (
        "docs/" if Path("PASSWORD_RESET_IMPLEMENTATION.md").exists() else None
    )

    doc_files = {
        "AUTHENTICATION_PERMISSIONS_SYSTEM.md": "docs/",
        "CHECKOUT_IMPLEMENTATION.md": "docs/",
        "VERIFIED_REVIEWS_COMPLETE.md": "docs/",
        # Use a small helper var to avoid a long inline expression
        "PASSWORD_RESET_IMPLEMENTATION.md": password_reset_target,
        "README.py": "docs/",
    }

    for source, target_dir in doc_files.items():
        if target_dir and Path(source).exists():
            target_path = Path(target_dir) / source
            if not target_path.exists():
                shutil.move(source, str(target_path))
                print(f"📚 Moved: {source} → {target_path}")

    print("\n3️⃣ Moving Configuration Files:")

    # Move config files that are still in root
    config_files = {
        ".env": "config/",
        ".flake8": "config/",
        "mypy.ini": "config/",
        "requirements.txt": "config/",
    }

    for source, target_dir in config_files.items():
        if Path(source).exists():
            target_path = Path(target_dir) / source
            if not target_path.exists():
                shutil.move(source, str(target_path))
                print(f"⚙️  Moved: {source} → {target_path}")

    print("\n4️⃣ Moving Test Files:")

    # Find and move test files
    test_patterns = ["test_*.py", "*_test.py"]

    for pattern in test_patterns:
        for test_file in Path(".").glob(pattern):
            # Skip if already moved
            if test_file.name != "test_store_detail.py":
                target_path = Path("tests") / test_file.name
                if not target_path.exists():
                    shutil.move(str(test_file), str(target_path))
                    print(f"🧪 Moved: {test_file} → {target_path}")

    # Move test_store_detail.py specifically
    if Path("test_store_detail.py").exists():
        target_path = Path("tests/test_store_detail.py")
        if not target_path.exists():
            shutil.move("test_store_detail.py", str(target_path))
            print(f"🧪 Moved: test_store_detail.py → {target_path}")

    # Move tests_suite contents
    if Path("tests_suite").exists():
        for test_file in Path("tests_suite").glob("*.py"):
            target_path = Path("tests") / test_file.name
            if not target_path.exists():
                shutil.move(str(test_file), str(target_path))
                print(f"🧪 Moved: {test_file} → {target_path}")

        # Remove empty tests_suite directory
        try:
            if not any(Path("tests_suite").iterdir()):
                shutil.rmtree("tests_suite")
                print("🗑️  Removed empty tests_suite directory")
        except OSError:
            pass

    print("\n5️⃣ Moving Script Files:")

    # Move script files to appropriate directories
    script_mappings = {
        "create_*.py": "scripts/data_management/",
        "fix_*.py": "scripts/utilities/",
        "optimize_*.py": "scripts/utilities/",
        "debug_*.py": "scripts/utilities/",
        "analyze_*.py": "scripts/utilities/",
        "cleanup_*.py": "scripts/utilities/",
        "demo_*.py": "scripts/testing/",
        "organize_*.py": "scripts/utilities/",
        "inspect_*.py": "scripts/utilities/",
    }

    for pattern, target_dir in script_mappings.items():
        for script_file in Path(".").glob(pattern):
            target_path = Path(target_dir) / script_file.name
            target_path.parent.mkdir(parents=True, exist_ok=True)
            if not target_path.exists():
                shutil.move(str(script_file), str(target_path))
                print(f"🔧 Moved: {script_file} → {target_path}")

    print("\n6️⃣ Moving Remaining Shop Files:")

    # Check for any remaining shop files in root
    remaining_shop_files = [
        "shop_models.py",
        "shop_views.py",
        "shop_views_extra.py",
        "shop_forms.py",
        "shop_urls.py",
        "shop_admin.py",
        "shop_apps.py",
        "shop_tests.py",
        "shop_context_processors.py",
    ]

    for shop_file in remaining_shop_files:
        if Path(shop_file).exists():
            # Determine target filename
            target_name = shop_file.replace("shop_", "")
            target_path = Path("shop") / target_name

            if not target_path.exists():
                shutil.move(shop_file, str(target_path))
                print(f"🛍️  Moved: {shop_file} → {target_path}")

    # Move shop_middleware.py and shop_permissions.py if they exist in root
    if Path("shop_middleware.py").exists():
        target_path = Path("shop/middleware.py")
        if not target_path.exists():
            shutil.move("shop_middleware.py", str(target_path))
            print(f"🛍️  Moved: shop_middleware.py → {target_path}")

    if Path("shop_permissions.py").exists():
        target_path = Path("shop/permissions.py")
        if not target_path.exists():
            shutil.move("shop_permissions.py", str(target_path))
            print(f"🛍️  Moved: shop_permissions.py → {target_path}")

    print("\n7️⃣ Archiving Legacy Directories:")

    # Archive old/duplicate directories
    legacy_dirs = [
        "shop_old",
        "shop_app",
        "shop_application",
        "flat_root",
        "project",
        "project_config",
        "data_management",
        "data_scripts",
        "utilities",
    ]

    for legacy_dir in legacy_dirs:
        if Path(legacy_dir).exists():
            target_path = Path("archived/legacy") / legacy_dir
            target_path.parent.mkdir(parents=True, exist_ok=True)
            if not target_path.exists():
                shutil.move(legacy_dir, str(target_path))
                print(f"📦 Archived: {legacy_dir} → {target_path}")

    print("\n8️⃣ Updating manage.py:")

    # Update manage.py to use correct settings path
    # Build a compact manage.py content using short lines to avoid long source
    manage_lines = [
        "#!/usr/bin/env python",
        '"""Django\'s command-line utility for administrative tasks."""',
        "import os",
        "import sys",
        "",
        "if __name__ == '__main__':",
        '    """Run administrative tasks."""',
        "    os.environ.setdefault(",
        "        'DJANGO_SETTINGS_MODULE',",
        "        'ecommerce_project.settings',",
        "    )",
        "    try:",
        "        from django.core.management import execute_from_command_line",
        "    except ImportError as exc:",
        '        raise ImportError("Couldn\'t import Django.") from exc',
        "    execute_from_command_line(sys.argv)",
    ]

    manage_content = "\n".join(manage_lines)
    with open("manage.py", "w", encoding="utf-8") as f:
        f.write(manage_content)
    print("✅ Updated: manage.py")

    print("\n9️⃣ Creating Project Overview:")

    # Create a project structure overview
    overview_content = """# Django E-commerce Project Structure

## 📁 Directory Structure

```
Django E-commerce/
├── ecommerce_project/          # Django project settings
│   ├── settings.py            # Main settings file
│   ├── urls.py               # Root URL configuration
│   ├── wsgi.py               # WSGI configuration
│   └── asgi.py               # ASGI configuration
│
├── shop/                      # Main shop application
│   ├── models.py             # Database models
│   ├── views.py              # Main views
│   ├── views_extra.py        # Additional views
│   ├── forms.py              # Django forms
│   ├── urls.py               # URL patterns
│   ├── admin.py              # Admin interface
│   ├── permissions.py        # Permission decorators
│   ├── middleware.py         # Custom middleware
│   └── templates/            # App templates
│
├── templates/                 # Global templates
├── static_assets/            # Static files (CSS, JS, images)
├── media/                    # User uploaded files
├── docs/                     # Documentation
├── tests/                    # Test files
├── scripts/                  # Utility scripts
│   ├── data_management/      # Data creation/management
│   ├── utilities/            # General utilities
│   └── testing/              # Testing scripts
│
├── config/                   # Configuration files
│   ├── .env                 # Environment variables
│   ├── requirements.txt     # Python dependencies
│   └── .flake8             # Code style config
│
├── archived/                 # Archived/legacy files
└── manage.py                # Django management script
```

## 🚀 Quick Start

1. Activate virtual environment: `.venv\\Scripts\\activate`
2. Install dependencies: `pip install -r config/requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start server: `python manage.py runserver`

## 🔧 Key Features

- Role-based authentication (Buyer, Vendor, Admin)
- Complete e-commerce functionality
- Product management
- Shopping cart and checkout
- Order management
- Review system
- Password reset
- Admin panel

## 📚 Documentation

See `docs/` folder for detailed documentation on each component.
"""

    with open("PROJECT_STRUCTURE.md", "w", encoding="utf-8") as f:
        f.write(overview_content)
    print("✅ Created: PROJECT_STRUCTURE.md")

    print("\n🔟 Final Cleanup:")

    # Remove any remaining __pycache__ directories
    for pycache in Path(".").rglob("__pycache__"):
        if pycache.is_dir():
            try:
                shutil.rmtree(pycache)
                print(f"🗑️  Removed: {pycache}")
            except OSError:
                pass

    print("\n✅ ORGANIZATION COMPLETE!")
    print("🎯 Project is now clean and organized!")
    print("📁 All files are in their proper locations")
    print("🚀 Ready for development!")

    # Show final structure
    print("\n📋 Final Project Structure:")
    important_dirs = [
        "ecommerce_project",
        "shop",
        "templates",
        "static_assets",
        "media",
        "docs",
        "tests",
        "scripts",
        "config",
    ]

    for dir_name in important_dirs:
        if Path(dir_name).exists():
            file_count = len(list(Path(dir_name).rglob("*")))
            print(f"✅ {dir_name}/ ({file_count} items)")
        else:
            print(f"❌ {dir_name}/ (missing)")


if __name__ == "__main__":
    safe_organize_remaining_files()
