# pylint: disable=no-member
"""Additional views for vendor functionality and password reset."""

from datetime import timedelta

import logging

from django.conf import settings  # type: ignore
from django.contrib import messages  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from django.core.paginator import Paginator  # type: ignore
from django.core.mail import EmailMultiAlternatives  # type: ignore
from django.db.models import Avg, Q  # type: ignore
from django.shortcuts import (  # type: ignore
    get_object_or_404,
    redirect,
    render,
)
from django.utils import timezone  # type: ignore
from main.shop_permissions import (
    admin_required,
    anonymous_required,
    vendor_required,
)

from .forms import (
    CategoryForm,
    PasswordResetForm,
    PasswordResetRequestForm,
    ProductForm,
    StoreForm,
)
from .models import Category, PasswordResetToken, Product, Store

logger = logging.getLogger(__name__)

# Resolve user model after imports to avoid executing code between imports
# (fixes E402 "module level import not at top of file" diagnostics).
User = get_user_model()


@vendor_required
def store_update(request, pk):
    """Update store - vendors only, must own store"""
    store = get_object_or_404(Store, pk=pk, vendor=request.user)
    if request.method == "POST":
        form = StoreForm(request.POST, request.FILES, instance=store)
        if form.is_valid():
            form.save()
            messages.success(request, "Store updated successfully!")
            return redirect("shop:store_detail", pk=store.pk)
    else:
        form = StoreForm(instance=store)
    context = {
        "form": form,
        "store": store,
    }
    return render(request, "shop/vendor/store_form.html", context)


@vendor_required
def store_delete(request, pk):
    """Delete store - vendors only, must own store"""
    store = get_object_or_404(Store, pk=pk, vendor=request.user)
    if request.method == "POST":
        store.delete()
        messages.success(request, "Store deleted successfully!")
        return redirect("shop:store_list")
    context = {"store": store}
    return render(request, "shop/vendor/store_confirm_delete.html", context)


@vendor_required
def product_create(request, store_id):
    """Create new product - vendors only, must own store"""
    store = get_object_or_404(Store, pk=store_id, vendor=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()
            messages.success(request, "Product created successfully!")
            return redirect("shop:product_detail", pk=product.pk)
    else:
        form = ProductForm()
    context = {
        "form": form,
        "store": store,
    }
    return render(request, "shop/vendor/product_form.html", context)


@vendor_required
def product_update(request, pk):
    """Update product - vendors only, must own product"""
    product = get_object_or_404(Product, pk=pk, store__vendor=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect("shop:product_detail", pk=product.pk)
    else:
        form = ProductForm(instance=product)
    context = {
        "form": form,
        "product": product,
    }
    return render(request, "shop/vendor/product_form.html", context)


@vendor_required
def product_delete(request, pk):
    """Delete product - vendors only, must own product"""
    product = get_object_or_404(Product, pk=pk, store__vendor=request.user)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect("shop:store_detail", pk=product.store.pk)
    context = {"product": product}
    return render(request, "shop/vendor/product_confirm_delete.html", context)


@vendor_required
def vendor_products(request):
    """List all products for vendor across all stores with filtering - vendors only"""

    # Get vendor's stores
    stores = Store.objects.filter(vendor=request.user)

    # Get all products from vendor's stores
    products = Product.objects.filter(store__vendor=request.user)

    # Filter by search
    search = request.GET.get("search")
    if search:
        products = products.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )

    # Filter by store
    store_filter = request.GET.get("store")
    if store_filter:
        products = products.filter(store_id=store_filter)

    # Filter by status
    status_filter = request.GET.get("status")
    if status_filter == "active":
        products = products.filter(is_active=True)
    elif status_filter == "inactive":
        products = products.filter(is_active=False)
    elif status_filter == "low_stock":
        products = products.filter(quantity__lte=5, quantity__gt=0)

    products = products.order_by("-created_at")

    # Pagination
    paginator = Paginator(products, 12)  # 12 products per page
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)

    context = {
        "products": page_obj,
        "page_obj": page_obj,
        "stores": stores,
        "is_paginated": page_obj.has_other_pages(),
    }
    return render(request, "shop/vendor/product_list.html", context)


# Password Reset Views


@anonymous_required
def password_reset_request(request):
    """Request password reset with enhanced security - anonymous users only"""
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                user = User.objects.get(email=email)

                # Invalidate any existing unused tokens for this user
                PasswordResetToken.objects.filter(user=user, is_used=False).update(
                    is_used=True
                )

                # Create new password reset token
                token = PasswordResetToken.objects.create(
                    user=user, expires_at=timezone.now() + timedelta(hours=1)
                )

                # Send email with HTML template support
                reset_url = request.build_absolute_uri(
                    f"/password-reset/{token.token}/"
                )

                subject = "Password Reset Request - Himalayan eCommerce"
                html_message = f"""
                <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">  # noqa: E501
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #007bff;">Password Reset Request</h2>
                        <p>Hello <strong>{user.get_full_name() or user.username}</strong>,</p>  # noqa: E501
                        <p>You have requested to reset your password for your Himalayan eCommerce account.</p>  # noqa: E501
                        <p>Click the button below to reset your password:</p>
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{reset_url}" style="background-color: #007bff; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; display: inline-block;">Reset My Password</a>  # noqa: E501
                        </div>
                        <p>Or copy and paste this link into your browser:</p>
                        <p style="word-break: break-all; background: #f8f9fa; padding: 10px; border-radius: 4px;"><a href="{reset_url}">{reset_url}</a></p>  # noqa: E501
                        <p><strong>Important:</strong> This link will expire in 1 hour for your security.</p>  # noqa: E501
                        <p>If you did not request this password reset, please ignore this email. Your password will remain unchanged.</p>  # noqa: E501
                        <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">  # noqa: E501
                        <p style="font-size: 12px; color: #666;">This is an automated message from Himalayan eCommerce. Please do not reply to this email.</p>  # noqa: E501
                    </div>
                </body>
                </html>
                """

                plain_message = f"""
                Password Reset Request - Himalayan eCommerce

                Hello {user.get_full_name() or user.username},

                You have requested to reset your password for your Himalayan eCommerce account.  # noqa: E501

                Click the link below to reset your password:
                {reset_url}

                This link will expire in 1 hour for your security.

                If you did not request this password reset, please ignore this email. Your password will remain unchanged.  # noqa: E501

                ---
                This is an automated message from Himalayan eCommerce.
                """

                # EmailMultiAlternatives already imported at module top; reuse it
                msg = EmailMultiAlternatives(
                    subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                )
                msg.attach_alternative(html_message, "text/html")
                msg.send()

                messages.success(
                    request,
                    f"Password reset email sent to {email}! "
                    f"Please check your inbox and follow the instructions. "
                    f"The link will expire in 1 hour.",
                )
                return redirect("shop:password_reset_request")

            except User.DoesNotExist:
                # For security, don't reveal that email doesn't exist
                messages.success(
                    request,
                    f"If an account with email {email} exists, "
                    f"a password reset link has been sent.",
                )
                return redirect("shop:password_reset_request")

    else:
        form = PasswordResetRequestForm()
    return render(request, "registration/password_reset_request.html", {"form": form})


@anonymous_required
def password_reset_confirm(request, token):
    """Confirm password reset with token and enhanced security - anonymous users only"""
    try:
        reset_token = PasswordResetToken.objects.get(token=token)

        # Check if token is expired or already used
        if reset_token.is_expired:
            messages.error(
                request,
                "This password reset link has expired. "
                "Please request a new password reset.",
            )
            return redirect("shop:password_reset_request")

        if reset_token.is_used:
            messages.error(
                request,
                "This password reset link has already been used. "
                "Please request a new password reset if needed.",
            )
            return redirect("shop:password_reset_request")

        if request.method == "POST":
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                # Update password with enhanced security
                user = reset_token.user
                new_password = form.cleaned_data["password1"]

                # Set new password
                user.set_password(new_password)
                user.save()

                # Mark token as used
                reset_token.is_used = True
                reset_token.save()

                # Invalidate all other tokens for this user
                PasswordResetToken.objects.filter(user=user, is_used=False).update(
                    is_used=True
                )

                # Send confirmation email
                try:
                    # Use the top-level import to avoid import-in-function lint
                    subject = "Password Successfully Reset - Himalayan eCommerce"

                    html_message = (
                        "<html>"
                        '<body style="font-family: Arial, sans-serif;">'
                        '<div style="max-width: 600px; margin: 0 auto; padding: 20px;">'
                        '<h2 style="color: #28a745;">Password Reset Successful</h2>'
                        f"<p>Hello <strong>{user.get_full_name() or user.username}</strong>,</p>"
                        "<p>Your password has been successfully reset.</p>"
                        "<p>You can now log in with your new password.</p>"
                        '<div style="text-align: center; margin: 30px 0;">'
                        f'<a href="{request.build_absolute_uri("/login/")}" '
                        'style="background-color: #28a745; color: white;'
                        " padding: 12px 25px; text-decoration: none;"
                        ' border-radius: 5px; display: inline-block;">'
                        "Login Now</a></div>"
                        "<p><strong>Security Note:</strong> If you did not reset your password,"
                        " please contact support immediately.</p>"
                        "</div></body></html>"
                    )

                    plain_message = (
                        f"Password Reset Successful - Himalayan eCommerce\n\n"
                        f"Hello {user.get_full_name() or user.username},\n\n"
                        "Your password has been successfully reset.\n"
                        "You can now log in with your new password.\n\n"
                        f"Login at: {request.build_absolute_uri('/login/')}\n\n"
                        "Security Note: If you did not reset your password,"
                        " please contact support immediately."
                    )

                    msg = EmailMultiAlternatives(
                        subject,
                        plain_message,
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                    )
                    msg.attach_alternative(html_message, "text/html")
                    msg.send()

                except Exception as e:  # pylint: disable=broad-except
                    # Log email error but don't fail the password reset
                    logger.exception(
                        "Failed to send confirmation email: %s",
                        e,
                    )

                messages.success(
                    request,
                    "Password reset successfully! You can now log in with your new password.",  # noqa: E501
                )
                return redirect("shop:login")
        else:
            form = PasswordResetForm()

        context = {
            "form": form,
            "token": token,
            "user": reset_token.user,
            "expires_in": (reset_token.expires_at - timezone.now()).total_seconds()
            // 60,
        }
        return render(request, "registration/password_reset_confirm.html", context)

    except PasswordResetToken.DoesNotExist:
        messages.error(
            request,
            "Invalid or expired password reset link. Please request a new password reset.",  # noqa: E501
        )
        return redirect("shop:password_reset_request")


# Category Management Views


@admin_required
def category_list(request):
    """List categories - admin only"""
    categories = Category.objects.all().order_by("name")
    context = {"categories": categories}
    return render(request, "shop/admin/category_list.html", context)


@admin_required
def category_create(request):
    """Create new category - admin only"""
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully!")
            return redirect("shop:category_list")
    else:
        form = CategoryForm()
    context = {"form": form}
    return render(request, "shop/admin/category_form.html", context)


@admin_required
def category_update(request, pk):
    """Update category - admin only"""
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully!")
            return redirect("shop:category_list")
    else:
        form = CategoryForm(instance=category)
    context = {
        "form": form,
        "category": category,
    }
    return render(request, "shop/admin/category_form.html", context)


@admin_required
def category_delete(request, pk):
    """Delete category - admin only"""
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted successfully!")
        return redirect("shop:category_list")
    context = {"category": category}
    return render(request, "shop/admin/category_confirm_delete.html", context)


# Search and filtering views


def search_products(request):
    """Advanced product search"""
    products = Product.objects.filter(is_active=True, quantity__gt=0)
    categories = Category.objects.all()
    # Search parameters
    query = request.GET.get("q", "")
    category_id = request.GET.get("category", "")
    min_price = request.GET.get("min_price", "")
    max_price = request.GET.get("max_price", "")
    sort_by = request.GET.get("sort", "newest")
    # Apply filters
    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(store__name__icontains=query)
        )
    if category_id:
        products = products.filter(category_id=category_id)
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass
    # Apply sorting
    if sort_by == "price_low":
        products = products.order_by("price")
    elif sort_by == "price_high":
        products = products.order_by("-price")
    elif sort_by == "name":
        products = products.order_by("name")
    elif sort_by == "rating":
        products = products.annotate(avg_rating=Avg("reviews__rating")).order_by(
            "-avg_rating"
        )
    else:  # newest
        products = products.order_by("-created_at")
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "categories": categories,
        "query": query,
        "selected_category": category_id,
        "min_price": min_price,
        "max_price": max_price,
        "sort_by": sort_by,
    }
    return render(request, "shop/product_list.html", context)
