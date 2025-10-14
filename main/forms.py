"""
Compatibility shim: top-level `forms.py` proxies to `shop.forms`.
"""

from shop.forms import (
    Category,
    CategoryForm,
    CheckoutForm,
    ContactForm,
    CustomUserCreationForm,
    PasswordResetForm,
    PasswordResetRequestForm,
    Product,
    ProductForm,
    Profile,
    ProfileUpdateForm,
    Review,
    ReviewForm,
    Store,
    StoreForm,
    User,
    UserCreationForm,
)

__all__ = [
    "Category",
    "CategoryForm",
    "CheckoutForm",
    "ContactForm",
    "CustomUserCreationForm",
    "PasswordResetForm",
    "PasswordResetRequestForm",
    "Product",
    "ProductForm",
    "Profile",
    "ProfileUpdateForm",
    "Review",
    "ReviewForm",
    "Store",
    "StoreForm",
    "User",
    "UserCreationForm",
]
