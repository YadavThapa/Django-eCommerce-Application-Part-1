"""Legacy shim re-exports for shop form classes.

Provides backward-compatible import paths for code that expects
forms under ``legacy_root_files.forms``. This module only re-exports
selected forms from ``shop.forms``.
"""

from main.shop.forms import (
    CategoryForm,
    CheckoutForm,
    ContactForm,
    CustomUserCreationForm,
    PasswordResetForm,
    PasswordResetRequestForm,
    ProductForm,
    ProfileUpdateForm,
    ReviewForm,
    StoreForm,
)

__all__ = [
    "CustomUserCreationForm",
    "ProfileUpdateForm",
    "StoreForm",
    "ProductForm",
    "ReviewForm",
    "CategoryForm",
    "CheckoutForm",
    "PasswordResetRequestForm",
    "PasswordResetForm",
    "ContactForm",
]
