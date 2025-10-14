#!/usr/bin/env python3
"""
Test Runner Script
==================
Convenient script to run different categories of tests
"""

import os
import subprocess
import sys
from pathlib import Path

# Ensure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_settings")


def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {cmd}")
    print(f"{'='*50}")

    try:
        subprocess.run(cmd, shell=True, check=True, capture_output=False, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with return code {e.returncode}")
        return False


def main():
    """Main test runner function"""
    if len(sys.argv) < 2:
        print(
            """
Test Runner Usage:
==================
python run_tests.py [category]

Categories:
    functional   - Run functional tests (auth, checkout, etc.)
    unit         - Run unit tests
    integration  - Run integration tests
    utilities    - Run utility/debug scripts
    data_setup   - Run data setup scripts
    all          - Run all test categories

Examples:
    python run_tests.py functional
    python run_tests.py all
"""
        )
        return

    category = sys.argv[1].lower()
    tests_dir = Path(__file__).parent

    if category == "all":
        categories = [
            "functional",
            "unit",
            "integration",
            "utilities",
            "data_setup",
        ]
        for cat in categories:
            cat_dir = tests_dir / cat
            if cat_dir.exists():
                cmd = f'python -m pytest "{cat_dir}"'
                desc = f"{cat.title()} Tests"
                run_command(cmd, desc)

    elif category in [
        "functional",
        "unit",
        "integration",
        "utilities",
        "data_setup",
    ]:
        cat_dir = tests_dir / category
        if cat_dir.exists():
            cmd = f'python -m pytest "{cat_dir}"'
            desc = f"{category.title()} Tests"
            run_command(cmd, desc)
        else:
            print(f"❌ Category directory not found: {cat_dir}")

    else:
        print(f"❌ Unknown category: {category}")
        print(
            "Valid categories: functional, unit, integration, utilities,"
            " data_setup, all"
        )


if __name__ == "__main__":
    main()
