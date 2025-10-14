"""Django models for the ecommerce application.

This module contains all the database models including:
- User profiles with role-based access
- Product catalog with categories and stores
- Shopping cart and order management
- Review system and password reset functionality
"""

# pylint: disable=too-few-public-methods
# Many Django model attributes (like the automatic "objects" manager) are
# added at runtime; static analyzers may raise false positives. Disable the
# "no-member" check for this module to reduce noise.
# pylint: disable=no-member
# type: ignore
# mypy: ignore-errors

import uuid
import sys

from django.contrib.auth import get_user_model  # type: ignore

from django.db import models  # type: ignore
from django.db.models.signals import post_save  # type: ignore
from django.dispatch import receiver  # type: ignore
from django.urls import reverse  # type: ignore
from django.utils import timezone  # type: ignore
from django.apps import apps as _django_apps  # type: ignore

# Prevent duplicate Django model registration by ensuring alternate
# module names map to this same module object. Some legacy code imports
# ``shop.models`` directly which can cause the models to be loaded under
# a different module identity than ``main.shop.models``. Map those
# names to this module so Django registers models only once.
try:  # pragma: no cover - defensive runtime mapping
    sys.modules["shop.models"] = sys.modules.get(
        __name__, sys.modules.get("main.shop.models")
    )
    # Also map the package name to main.shop when possible
    if "main.shop" in sys.modules:
        # only set if not already present
        sys.modules.setdefault("shop", sys.modules.get("main.shop"))
except (KeyError, ImportError):
    # Best-effort only; if mapping fails, proceed normally and let errors surface
    pass

# If another module already provided the models under the name 'shop.models',
# reuse those symbols instead of redefining the classes here. This covers the
# case where import order causes the same file to be loaded under two module
# names (e.g. 'shop.models' and 'main.shop.models'), which would otherwise
# cause Django to register models twice and raise RuntimeError.
_existing_shop_models = sys.modules.get("shop.models")
_reused_from_registry = False
if (
    _existing_shop_models is not None
    and getattr(_existing_shop_models, "Profile", None) is not None
):
    # Rebind names from the existing module and skip class redefinitions
    Profile = getattr(_existing_shop_models, "Profile")
    Category = getattr(_existing_shop_models, "Category")
    Store = getattr(_existing_shop_models, "Store")
    Product = getattr(_existing_shop_models, "Product")
    Cart = getattr(_existing_shop_models, "Cart")
    CartItem = getattr(_existing_shop_models, "CartItem")
    Order = getattr(_existing_shop_models, "Order")
    OrderItem = getattr(_existing_shop_models, "OrderItem")
    Review = getattr(_existing_shop_models, "Review")
    PasswordResetToken = getattr(_existing_shop_models, "PasswordResetToken")
    # Also copy any signal handlers or helpers if present
    try:
        create_user_profile = getattr(_existing_shop_models, "create_user_profile")
        save_user_profile = getattr(_existing_shop_models, "save_user_profile")
    except Exception:
        pass
    # Export list
    __all__ = [
        "Profile",
        "Category",
        "Store",
        "Product",
        "Cart",
        "CartItem",
        "Order",
        "OrderItem",
        "Review",
        "PasswordResetToken",
    ]
    # Done - skip the rest of the module which defines the classes
    _SKIP = True
else:
    _SKIP = False

# Additional defensive check: if Django's app registry already contains
# model classes for the 'shop' app (for example because 'shop.models'
# was loaded earlier), reuse those and skip redefining classes. This
# handles cases where apps have been initialized before this module is
# imported under the 'main.shop.models' name.
try:
    try:
        _reg_profile = _django_apps.get_model("shop", "Profile")
    except LookupError:
        _reg_profile = None

    if _reg_profile is not None:
        # Rebind commonly used models from the registry and skip definitions
        Profile = _django_apps.get_model("shop", "Profile")
        Category = _django_apps.get_model("shop", "Category")
        Store = _django_apps.get_model("shop", "Store")
        Product = _django_apps.get_model("shop", "Product")
        Cart = _django_apps.get_model("shop", "Cart")
        CartItem = _django_apps.get_model("shop", "CartItem")
        Order = _django_apps.get_model("shop", "Order")
        OrderItem = _django_apps.get_model("shop", "OrderItem")
        Review = _django_apps.get_model("shop", "Review")
        PasswordResetToken = _django_apps.get_model("shop", "PasswordResetToken")
        _SKIP = True
except Exception:
    # No-op: continue to define models normally
    pass

# Resolve the user model after imports and registry checks to avoid
# executing code before all imports are declared (fixes E402 diagnostics).
User = get_user_model()

# Only define the models and signal handlers if we didn't reuse an
# already-loaded module's definitions above.
if not _SKIP:

    class Profile(models.Model):
        """Extended user profile with role-based access"""

        ROLE_CHOICES = [
            ("buyer", "Buyer"),
            ("vendor", "Vendor"),
            ("admin", "Admin"),
        ]
        user = models.OneToOneField(
            User, on_delete=models.CASCADE, related_name="profile"
        )
        role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="buyer")
        phone = models.CharField(max_length=15, blank=True, null=True)
        address = models.TextField(blank=True, null=True)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self) -> str:
            # pylint: disable=no-member
            return f"{self.user.username} - {self.role}"

        class Meta:
            """Meta configuration for Profile model."""

            app_label = "shop"

    class Category(models.Model):
        """Product category model."""

        name = models.CharField(max_length=100, unique=True)
        description = models.TextField(blank=True)
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self) -> str:
            return str(self.name)

        class Meta:
            """Meta configuration for Category model."""

            verbose_name_plural = "Categories"
            app_label = "shop"

    class Store(models.Model):
        """Vendor store model"""

        vendor = models.ForeignKey(
            User, on_delete=models.CASCADE, related_name="stores"
        )
        name = models.CharField(max_length=200)
        description = models.TextField()
        logo = models.ImageField(upload_to="store_logos/", blank=True, null=True)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        is_active = models.BooleanField(default=True)

        def __str__(self) -> str:
            return str(self.name)

        def get_absolute_url(self) -> str:
            """Return absolute URL for store detail page."""
            return reverse("shop:store_detail", kwargs={"pk": self.pk})

        class Meta:
            """Meta configuration for Store model."""

            app_label = "shop"

    class Product(models.Model):
        """Product model"""

        store = models.ForeignKey(
            Store, on_delete=models.CASCADE, related_name="products"
        )
        category = models.ForeignKey(
            Category,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name="products",
        )
        name = models.CharField(max_length=200)
        description = models.TextField()
        price = models.DecimalField(max_digits=10, decimal_places=2)
        quantity = models.PositiveIntegerField(default=0)
        image = models.ImageField(upload_to="product_images/", blank=True, null=True)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        is_active = models.BooleanField(default=True)

        def __str__(self) -> str:
            return str(self.name)

        def get_absolute_url(self) -> str:
            """Return absolute URL for product detail page."""
            return reverse("shop:product_detail", kwargs={"pk": self.pk})

        @property
        def is_in_stock(self) -> bool:
            """Check if product is in stock."""
            return self.quantity > 0

        class Meta:
            """Meta configuration for Product model."""

            app_label = "shop"
            ordering = ["-created_at"]

    class Cart(models.Model):
        """Shopping cart model"""

        user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self) -> str:
            return f"Cart for {self.user.username}"  # pylint: disable=no-member

        @property
        def total_items(self) -> int:
            """Total number of items in cart."""
            # pylint: disable=no-member
            return sum(item.quantity for item in self.items.all())

        @property
        def total_price(self) -> float:
            """Total price of all items in cart."""
            # pylint: disable=no-member
            return sum(item.total_price for item in self.items.all())

        class Meta:
            """Meta configuration for Cart model."""

            app_label = "shop"

    class CartItem(models.Model):
        """Individual items in shopping cart"""

        cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
        product = models.ForeignKey(Product, on_delete=models.CASCADE)
        quantity = models.PositiveIntegerField(default=1)
        added_at = models.DateTimeField(auto_now_add=True)

        def __str__(self) -> str:
            return f"{self.quantity} x {self.product.name}"

        @property
        def total_price(self) -> float:
            """Calculate total price for this cart item."""
            # pylint: disable=no-member
            return self.product.price * self.quantity

        class Meta:
            """Meta configuration for CartItem model."""

            app_label = "shop"
            unique_together = ("cart", "product")

    class Order(models.Model):
        """Customer order model"""

        STATUS_CHOICES = [
            ("pending", "Pending"),
            ("processing", "Processing"),
            ("shipped", "Shipped"),
            ("delivered", "Delivered"),
            ("cancelled", "Cancelled"),
        ]

        order_id = models.CharField(max_length=100, unique=True, editable=False)
        buyer = models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            related_name="orders",
            null=True,
            blank=True,
        )
        guest_name = models.CharField(max_length=100, blank=True, null=True)
        guest_email = models.EmailField(blank=True, null=True)
        status = models.CharField(
            max_length=20, choices=STATUS_CHOICES, default="pending"
        )
        total_amount = models.DecimalField(max_digits=10, decimal_places=2)
        shipping_address = models.TextField()
        payment_method = models.CharField(max_length=50, default="cod")
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def save(self, *args, **kwargs) -> None:
            """Override save to generate unique order ID."""
            if not self.order_id:
                self.order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
            super().save(*args, **kwargs)

        def __str__(self) -> str:
            return f"Order {self.order_id}"

        class Meta:
            """Meta configuration for Order model."""

            app_label = "shop"
            ordering = ["-created_at"]

    class OrderItem(models.Model):
        """Items in customer order"""

        order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
        product = models.ForeignKey(Product, on_delete=models.CASCADE)
        quantity = models.PositiveIntegerField()
        price = models.DecimalField(max_digits=10, decimal_places=2)

        def __str__(self) -> str:
            return f"{self.quantity} x {self.product.name}"

        @property
        def total_price(self) -> float:
            """Calculate total price for this order item."""
            return self.price * self.quantity

        class Meta:
            """Meta configuration for OrderItem model."""

            app_label = "shop"

    class Review(models.Model):
        """Product review model"""

        product = models.ForeignKey(
            Product, on_delete=models.CASCADE, related_name="reviews"
        )
        user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
        rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
        comment = models.TextField(blank=True)
        is_verified = models.BooleanField(default=False)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self) -> str:
            # pylint: disable=no-member
            return f"{self.user.username} - {self.product.name} ({self.rating}★)"

        class Meta:
            """Meta configuration for Review model."""

            app_label = "shop"
            unique_together = ("product", "user")
            ordering = ["-created_at"]

    class PasswordResetToken(models.Model):
        """Password reset token model with secure token generation"""

        user = models.ForeignKey(User, on_delete=models.CASCADE)
        token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
        created_at = models.DateTimeField(auto_now_add=True)
        expires_at = models.DateTimeField()
        is_used = models.BooleanField(default=False)

        def save(self, *args, **kwargs) -> None:
            """Override save to set expiry time and generate token."""
            if not self.expires_at:
                self.expires_at = timezone.now() + timezone.timedelta(hours=1)
            super().save(*args, **kwargs)

        @property
        def is_expired(self) -> bool:
            """Check if token is expired."""
            return timezone.now() > self.expires_at

        def __str__(self) -> str:
            # pylint: disable=no-member
            return f"Reset token for {self.user.username}"

        class Meta:
            """Meta configuration for PasswordResetToken model."""

            app_label = "shop"

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs) -> None:
        # pylint: disable=unused-argument
        """Create user profile when user is created."""
        if created:
            Profile.objects.get_or_create(  # pylint: disable=no-member
                user=instance, defaults={"role": "buyer"}
            )

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs) -> None:
        # pylint: disable=unused-argument
        """Save user profile when user is saved."""
        if hasattr(instance, "profile"):
            instance.profile.save()
        else:
            # Ensure profile exists
            Profile.objects.get_or_create(user=instance, defaults={"role": "buyer"})
