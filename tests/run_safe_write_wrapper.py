"""Wrapper to run the safe_write_test under the correct Django settings.
This sets DJANGO_SETTINGS_MODULE and calls django.setup() before importing the test.
"""
import os
import django  # type: ignore[import]

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.ecommerce_project.settings")
# Ensure settings are configured
django.setup()

# Import the safe write test module; it performs its work at import-time.
# Keep noqa/type-ignore so linters don't complain about import position
# or missing stubs in some environments.
import tests.safe_write_test as sw  # noqa: E402  # type: ignore[import]

# Module reference used to silence unused-import linters without
# re-running side-effectful logic.
_ = sw

print("Wrapper completed")
