"""Django admin configuration for the ecommerce shop application.

This module defines admin interfaces for all ecommerce models including
products, stores, orders, reviews, and user profiles.
"""

from django.contrib import admin  # type: ignore

from .models import (
    Cart,
    CartItem,
    Category,
    Order,
    OrderItem,
    PasswordResetToken,
    Product,
    Profile,
    Review,
    Store,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin interface for user profiles."""

    list_display = ["user", "role", "phone", "created_at"]
    list_filter = ["role", "created_at"]
    search_fields = ["user__username", "user__email", "phone"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for product categories."""

    list_display = ["name", "created_at"]
    search_fields = ["name"]
    readonly_fields = ["created_at"]


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    """Admin interface for vendor stores."""

    list_display = ["name", "vendor", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "vendor__username"]
    readonly_fields = ["created_at", "updated_at"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("vendor")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for products."""

    list_display = [
        "name",
        "store",
        "category",
        "price",
        "quantity",
        "is_active",
        "created_at",
    ]
    list_filter = [
        "is_active",
        "category",
        "created_at",
    ]
    search_fields = [
        "name",
        "store__name",
        "store__vendor__username",
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]
    list_editable = [
        "price",
        "quantity",
        "is_active",
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("store", "category", "store__vendor")


class CartItemInline(admin.TabularInline):
    """Inline admin for cart items."""

    model = CartItem
    extra = 0
    readonly_fields = ["added_at"]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin interface for shopping carts."""

    list_display = [
        "user",
        "total_items",
        "total_price",
        "created_at",
    ]
    search_fields = ["user__username"]
    readonly_fields = ["created_at", "updated_at"]
    inlines = [CartItemInline]

    def total_items(self, obj):
        """Display total items in cart."""
        return obj.total_items

    total_items.short_description = "Total Items"  # type: ignore

    def total_price(self, obj):
        """Display formatted total price."""
        return f"${obj.total_price:.2f}"

    total_price.short_description = "Total Price"  # type: ignore


class OrderItemInline(admin.TabularInline):
    """Inline admin for order items."""

    model = OrderItem
    extra = 0
    readonly_fields = ["total_price"]

    def total_price(self, obj):
        """Display formatted total price for order item."""
        return f"${obj.total_price:.2f}"

    total_price.short_description = "Total"  # type: ignore


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for customer orders."""

    list_display = [
        "order_id",
        "buyer",
        "status",
        "total_amount",
        "created_at",
    ]
    list_filter = [
        "status",
        "created_at",
    ]
    search_fields = [
        "order_id",
        "buyer__username",
        "buyer__email",
    ]
    readonly_fields = [
        "order_id",
        "created_at",
        "updated_at",
    ]
    list_editable = ["status"]
    inlines = [OrderItemInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("buyer")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin interface for product reviews."""

    list_display = [
        "product",
        "user",
        "rating",
        "is_verified",
        "created_at",
    ]
    list_filter = [
        "rating",
        "is_verified",
        "created_at",
    ]
    search_fields = [
        "product__name",
        "user__username",
        "comment",
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]
    list_editable = ["is_verified"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("product", "user")


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    """Admin interface for password reset tokens."""

    list_display = [
        "user",
        "token",
        "is_used",
        "is_expired_display",
        "created_at",
        "expires_at",
    ]
    list_filter = [
        "is_used",
        "created_at",
    ]
    search_fields = [
        "user__username",
        "user__email",
    ]
    readonly_fields = [
        "token",
        "created_at",
    ]

    def is_expired_display(self, obj):
        """Display expired status as boolean."""
        return obj.is_expired

    is_expired_display.boolean = True  # type: ignore
    is_expired_display.short_description = "Expired"  # type: ignore


# Customize admin site headers
admin.site.site_header = "Himalayan eCommerce Admin"
admin.site.site_title = "Himalayan eCommerce"
admin.site.index_title = "Admin Dashboard"
