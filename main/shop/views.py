# pylint: disable=no-member,import-error
"""Main views for the ecommerce shop application."""

import logging
from decimal import Decimal

from django.contrib import messages  # type: ignore
from django.contrib.auth import login  # type: ignore
from django.contrib.auth.decorators import login_required  # type: ignore
from django.core.paginator import Paginator  # type: ignore

# Email functionality imported in functions as needed
from django.db.models import Q  # type: ignore
from django.db import DatabaseError  # type: ignore
from django.shortcuts import (  # type: ignore
    get_object_or_404,
    redirect,
    render,
)
from django.http import HttpResponse  # type: ignore
from django.urls import reverse  # type: ignore
from django.views.decorators.http import require_POST  # type: ignore

from django.http import JsonResponse  # type: ignore
from django.db import transaction  # type: ignore

from .cart import Cart as SessionCart
from .email_service import send_order_confirmation_email

from .forms import (
    CheckoutForm,
    CustomUserCreationForm,
    ProfileUpdateForm,
    ReviewForm,
    StoreForm,
)
from .models import (
    Cart,
    CartItem,
    Category,
    Order,
    OrderItem,
    Product,
    Review,
    Store,
)
from .permissions import (
    anonymous_required,
    buyer_required,
    vendor_required,
)

# Module logger
logger = logging.getLogger(__name__)


def home(request):
    """Homepage view"""
    featured_products = Product.objects.filter(is_active=True, quantity__gt=0).order_by(
        "-created_at"
    )[:8]
    categories = Category.objects.all()[:6]
    context = {
        "featured_products": featured_products,
        "categories": categories,
    }
    return render(request, "shop/home.html", context)


@anonymous_required
def register(request):
    """User registration view - anonymous users only"""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            # Log the user in
            login(request, user)
            # Redirect based on role
            if hasattr(user, "profile") and user.profile.role == "vendor":
                return redirect("shop:vendor_dashboard")
            else:
                return redirect("shop:home")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@buyer_required
def customer_dashboard(request):
    """Customer/Buyer dashboard with shopping overview"""

    try:
        # Get cart items count
        cart_items_count = 0
        try:
            user_cart = Cart.objects.get(user=request.user)
            cart_items_count = user_cart.total_items
        except Cart.DoesNotExist:
            pass

        # Get total orders
        total_orders = Order.objects.filter(buyer=request.user).count()

        # Get recent orders
        recent_orders = Order.objects.filter(buyer=request.user).order_by(
            "-created_at"
        )[:5]

        # Get total reviews
        total_reviews = Review.objects.filter(user=request.user).count()

        # Get featured products
        featured_products = Product.objects.filter(
            is_active=True, quantity__gt=0
        ).order_by("-created_at")[:6]

        # Get categories
        categories = Category.objects.all()[:6]

        context = {
            "cart_items_count": cart_items_count,
            "total_orders": total_orders,
            "recent_orders": recent_orders,
            "total_reviews": total_reviews,
            "featured_products": featured_products,
            "categories": categories,
            "favorite_products": 0,  # Placeholder for future wishlist feature
        }
        return render(request, "shop/customer/dashboard.html", context)

    except DatabaseError as e:
        logger.exception("Database error in customer dashboard: %s", e)
        messages.error(request, "Error loading dashboard. Please try again.")
        return redirect("shop:home")
    # pylint: disable=broad-except
    except Exception as e:
        # Fallback for unexpected runtime errors; log for diagnostics.
        logger.exception("Unexpected error in customer dashboard: %s", e)
        messages.error(request, "Error loading dashboard. Please try again.")
        return redirect("shop:home")


@login_required
def profile(request):
    """User profile view"""
    if request.method == "POST":
        form = ProfileUpdateForm(
            request.POST,
            instance=request.user.profile,
            user=request.user,
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("shop:profile")
    else:
        form = ProfileUpdateForm(
            instance=request.user.profile,
            user=request.user,
        )
    return render(request, "shop/profile_update.html", {"form": form})


def product_list(request):
    """Display list of all products with filtering and search"""

    # Get all active products
    products = Product.objects.filter(is_active=True)

    # Search functionality
    search_query = request.GET.get("search", "")
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(store__name__icontains=search_query)
        )

    # Category filter
    category_id = request.GET.get("category")
    if category_id:
        products = products.filter(category_id=category_id)

    # Store filter
    store_id = request.GET.get("store")
    if store_id:
        products = products.filter(store_id=store_id)

    # Price range filter
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
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

    # Sorting
    sort_by = request.GET.get("sort", "-created_at")
    if sort_by in ["name", "-name", "price", "-price", "-created_at"]:
        products = products.order_by(sort_by)
    else:
        products = products.order_by("-created_at")

    # Get filter options
    categories = Category.objects.all()
    stores = Store.objects.filter(is_active=True)
    total_products = Product.objects.filter(is_active=True).count()

    # Pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Determine which template to use
    template_name = (
        "shop/product_list_enhanced.html"
        if request.GET.get("enhanced")
        else "shop/product_list.html"
    )

    return render(
        request,
        template_name,
        {
            "products": page_obj,
            "categories": categories,
            "stores": stores,
            "total_products": total_products,
            "page_obj": page_obj,
            "is_paginated": page_obj.has_other_pages(),
        },
    )


def product_detail(request, pk):
    """Product detail view"""
    product = get_object_or_404(Product, pk=pk, is_active=True)
    reviews = product.reviews.all().order_by("-created_at")

    # Calculate review statistics
    verified_reviews = reviews.filter(is_verified=True)
    unverified_reviews = reviews.filter(is_verified=False)
    verified_count = verified_reviews.count()
    unverified_count = unverified_reviews.count()

    # Check if user has already reviewed this product
    user_review = None
    if request.user.is_authenticated:
        try:
            user_review = Review.objects.get(product=product, user=request.user)
        except Review.DoesNotExist:
            pass

    # Related products
    related_products = Product.objects.filter(
        category=product.category, is_active=True, quantity__gt=0
    ).exclude(pk=product.pk)[:4]

    context = {
        "product": product,
        "reviews": reviews,
        "user_review": user_review,
        "related_products": related_products,
        "verified_reviews": verified_reviews,
        "unverified_reviews": unverified_reviews,
        "verified_count": verified_count,
        "unverified_count": unverified_count,
        "total_reviews": reviews.count(),
    }
    # Defensive: expose whether the product's store is present and active.
    store_obj = getattr(product, "store", None)
    context["store_active"] = bool(store_obj and store_obj.is_active)
    return render(request, "shop/product_detail.html", context)


def add_to_cart(request, product_id):
    """Add product to session cart - works for anonymous users"""
    # Use module-level SessionCart to avoid import inside function
    session_cart = SessionCart(request)
    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))

        # Check stock availability
        if quantity > product.quantity:
            messages.error(request, "Not enough stock available!")
            return redirect("shop:product_detail", pk=product_id)

        # Check if adding this quantity would exceed stock
        current_quantity = 0
        if str(product_id) in session_cart.cart:
            current_quantity = session_cart.cart[str(product_id)]["quantity"]

        if current_quantity + quantity > product.quantity:
            available = product.quantity - current_quantity
            messages.error(request, f"Only {available} more items can be added.")
            return redirect("shop:product_detail", pk=product_id)

        session_cart.add(product=product, quantity=quantity)
        messages.success(request, f"{product.name} added to cart!")
        # Explicitly return 303 See Other so user-agents perform a GET on the
        # cart detail page after POST. This is more explicit than a 302
        # and signals that the client should retrieve the Location with GET.
        resp = HttpResponse(status=303)
        resp["Location"] = reverse("shop:cart_detail")
        return resp

    # Non-POST requests should simply redirect back to product detail
    return redirect("shop:product_detail", pk=product_id)


@buyer_required
def cart(request):
    """Shopping cart view - buyers only"""
    try:
        user_cart = Cart.objects.get(user=request.user)
        cart_items = user_cart.items.all()
    except Cart.DoesNotExist:
        cart_items = []
    context = {
        "cart_items": cart_items,
    }
    return render(request, "shop/cart.html", context)


@buyer_required
@require_POST
def update_cart_item(request, item_id):
    """Update cart item quantity - buyers only"""
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    quantity = int(request.POST.get("quantity", 1))
    if quantity <= 0:
        cart_item.delete()
        messages.success(request, "Item removed from cart!")
    elif quantity > cart_item.product.quantity:
        messages.error(request, "Not enough stock available!")
    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, "Cart updated!")
    return redirect("shop:cart_detail")


@buyer_required
def remove_from_cart(request, item_id):
    """Remove item from cart - buyers only"""
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart!")
    return redirect("shop:cart_detail")


def checkout(request):
    """Checkout process with session cart and email invoice"""
    # Use module-level Decimal, transaction, SessionCart and
    # send_order_confirmation_email to avoid inline imports.
    # Get session cart
    session_cart = SessionCart(request)

    if len(session_cart) == 0:
        messages.error(request, "Your cart is empty!")
        return redirect("shop:cart_detail")

    if request.method == "POST":
        form = CheckoutForm(request.POST, user=request.user)
        if form.is_valid():
            # Require name and email for guests
            if not request.user.is_authenticated:
                guest_name = form.cleaned_data.get("name", "").strip()
                guest_email = form.cleaned_data.get("email", "").strip()
                if not guest_name or not guest_email:
                    messages.error(
                        request,
                        "Name and email are required for guest checkout.",
                    )
                    # Precompute totals to keep mapping lines short
                    _total = session_cart.get_total_price()
                    _tax = _total * Decimal("0.08")
                    _grand = _total * Decimal("1.08")

                    return render(
                        request,
                        "shop/checkout.html",
                        {
                            "form": form,
                            "cart": session_cart,
                            "total": _total,
                            "tax": _tax,
                            "grand_total": _grand,
                        },
                    )
            # Check stock availability for all items first
            for item in session_cart:
                product = item["product"]
                quantity = item["quantity"]
                # Use product.quantity instead of product.stock
                if quantity > product.quantity:
                    messages.error(
                        request,
                        (
                            f"Not enough stock for {product.name}! "
                            f"Only {product.quantity} available."
                        ),
                    )
                    return redirect("shop:cart_detail")
            try:
                with transaction.atomic():
                    # Calculate order totals
                    subtotal = session_cart.get_total_price()
                    tax = subtotal * Decimal("0.08")  # 8% tax
                    total = subtotal + tax

                    # Create order
                    order = Order.objects.create(
                        buyer=(request.user if request.user.is_authenticated else None),
                        total_amount=total,
                        shipping_address=form.cleaned_data["shipping_address"],
                        guest_name=(
                            guest_name if not request.user.is_authenticated else ""
                        ),
                        guest_email=(
                            guest_email if not request.user.is_authenticated else ""
                        ),
                    )

                    # Create order items and update stock
                    for item in session_cart:
                        product = item["product"]
                        quantity = item["quantity"]

                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=quantity,
                            price=product.price,
                        )

                        # Update product stock
                        product.quantity -= quantity
                        product.save()

                    # Clear session cart
                    session_cart.clear()
                    print(
                        ("🛒 Session cart cleared for user " f"{request.user.username}")
                    )

                    # Also ensure any DB-backed Cart for this user is cleared
                    # so tests and legacy code that rely on the Cart model
                    # do not observe leftover items. Best-effort and silent on
                    # any error to avoid breaking a successful checkout.
                    try:
                        if request.user.is_authenticated:
                            db_cart = Cart.objects.filter(user=request.user).first()
                            if db_cart:
                                try:
                                    db_cart.items.all().delete()
                                except DatabaseError:
                                    # Best-effort cleanup: log DB errors but do not
                                    # fail the checkout. Narrow exception to
                                    # DatabaseError to avoid masking unexpected
                                    # issues.
                                    logger.exception(
                                        "Failed to delete cart items for user %s",
                                        request.user,
                                    )
                                try:
                                    db_cart.delete()
                                except DatabaseError:
                                    logger.exception(
                                        "Failed to delete DB-backed cart for user %s",
                                        request.user,
                                    )
                    except DatabaseError:
                        # Only catch database-related errors here; other
                        # unexpected exceptions should surface to the outer
                        # checkout error handler.
                        logger.exception(
                            "Database error while clearing DB-backed cart for user %s",
                            request.user,
                        )

                    # Send confirmation email with PDF invoice.
                    # Email sending and PDF generation may raise a variety of
                    # exceptions (SMTP errors, file errors, third-party libs).
                    # Allow a broad catch here but document and log it.
                    try:
                        email_sent = send_order_confirmation_email(order)
                        if email_sent:
                            messages.success(
                                request,
                                (
                                    "✅ Order placed successfully! "
                                    "Your invoice has been sent to your email."
                                ),
                            )
                        else:
                            # For anonymous (guest) buyers, prompt them to log in
                            # so they can receive invoice information in their
                            # account/email. Authenticated users keep the
                            # original fallback message.
                            if not request.user.is_authenticated:
                                messages.success(
                                    request,
                                    (
                                        "✅ Order placed successfully! "
                                        "Please login to get an invoice information in your email."
                                    ),
                                )
                            else:
                                messages.success(
                                    request,
                                    (
                                        "✅ Order placed successfully! "
                                        "(Invoice email could not be sent.)"
                                    ),
                                )
                    # Email sending may raise many different exceptions
                    # (smtplib.SMTPException, file errors, PDF lib errors).
                    # We intentionally catch Exception here but keep a
                    # pylint disable comment and a short rationale.
                    # pylint: disable=broad-except
                    except Exception as email_error:
                        # Documented fallback: various email/PDF errors may
                        # occur. For guests, ask them to login to receive the
                        # invoice information via email.
                        logger.exception("Email sending failed: %s", email_error)
                        if not request.user.is_authenticated:
                            messages.success(
                                request,
                                (
                                    "✅ Order placed successfully! "
                                    "Please login to get an invoice information in your email."
                                ),
                            )
                        else:
                            messages.success(
                                request,
                                (
                                    "✅ Order placed successfully! "
                                    "(Invoice email will be sent shortly.)"
                                ),
                            )

                    # Log the successful order
                    print(f"📦 Order {order.order_id} created successfully")
                    # Show success notification and redirect to order detail
                    return redirect("shop:order_detail", order_id=order.order_id)

            except DatabaseError as e:
                # Database-related errors should be surfaced as a friendly
                # message and not retried blindly.
                logger.exception("Database error during checkout: %s", e)
                messages.error(
                    request,
                    (
                        "Error processing your order (database error). "
                        "Please try again."
                    ),
                )
                return redirect("shop:cart_detail")
            # The outermost fallback catches unexpected runtime errors
            # during checkout to avoid leaving the user in an unknown
            # state; keep this broad catch but document it for reviewers.
            # pylint: disable=broad-except
            except Exception as e:
                # Log unexpected exceptions for diagnosis but present a
                # generic message to the user.
                logger.exception("Unexpected error during checkout: %s", e)
                messages.error(
                    request,
                    ("Error processing your order: " f"{str(e)}. Please try again."),
                )
                return redirect("shop:cart_detail")
    else:
        form = CheckoutForm(user=request.user)

    # Calculate totals for display
    subtotal = session_cart.get_total_price()
    tax = subtotal * Decimal("0.08")
    grand_total = subtotal + tax

    context = {
        "form": form,
        "cart": session_cart,
        "total": subtotal,
        "tax": tax,
        "grand_total": grand_total,
    }
    return render(request, "shop/checkout.html", context)


# Email function moved to email_service.py


@buyer_required
def order_detail(request, order_id):
    """Order detail view - buyers only, must own order"""
    order = get_object_or_404(Order, order_id=order_id, buyer=request.user)
    context = {"order": order}
    return render(request, "shop/order_detail.html", context)


@buyer_required
def order_history(request):
    """User's order history - buyers only"""
    orders = Order.objects.filter(buyer=request.user).order_by("-created_at")
    paginator = Paginator(orders, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}
    return render(request, "shop/order_history.html", context)


@login_required
def add_review(request, product_id):
    """Add product review"""
    product = get_object_or_404(Product, pk=product_id)

    # Check if user already reviewed this product
    if Review.objects.filter(product=product, user=request.user).exists():
        messages.error(request, "You have already reviewed this product!")
        return redirect("shop:product_detail", pk=product_id)

    # Check if user has purchased this product (verified purchase)
    has_purchased = OrderItem.objects.filter(
        product=product, order__buyer=request.user
    ).exists()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            # Set verification status based on purchase history
            review.is_verified = has_purchased
            review.save()

            # Show success messages for verified vs unverified reviews
            if has_purchased:
                messages.success(
                    request,
                    "Verified review added successfully! "
                    "Thank you for your feedback as a verified purchaser.",
                )
            else:
                messages.success(
                    request,
                    "Review added successfully! Your review will be marked as "
                    "unverified since you haven't purchased this product.",
                )
            return redirect("shop:product_detail", pk=product_id)
    else:
        form = ReviewForm()

    context = {
        "form": form,
        "product": product,
        "has_purchased": has_purchased,  # Pass to template for display
    }
    return render(request, "shop/add_review.html", context)


# Vendor Views
@vendor_required
def vendor_dashboard(request):
    """Vendor dashboard - vendors only"""

    try:
        stores = Store.objects.filter(vendor=request.user)
        recent_orders = []
        total_sales = 0
        total_products = 0

        # Get total products count
        try:
            total_products = Product.objects.filter(store__vendor=request.user).count()
        except DatabaseError as e:  # pragma: no cover - defensive logging
            # for DB issues
            logger.warning("Could not fetch product count: %s", e)

        # Try to get order items safely
        try:
            recent_orders = OrderItem.objects.filter(
                product__store__vendor=request.user
            ).order_by("-order__created_at")[:10]
            # Calculate total sales
            total_sales = sum(
                item.total_price
                for item in OrderItem.objects.filter(
                    product__store__vendor=request.user
                )
            )
        except DatabaseError as e:  # pragma: no cover - defensive logging
            logger.warning("Could not fetch order data: %s", e)

    except DatabaseError as e:  # noqa: DBCATCH - database-specific fallback
        logger.exception("Database error in vendor dashboard: %s", e)
        stores = Store.objects.none()
        recent_orders = []
        total_sales = 0
        total_products = 0
    except Exception as e:  # pylint: disable=broad-except
        logger.exception("Unexpected error in vendor dashboard: %s", e)
        stores = Store.objects.none()
        recent_orders = []
        total_sales = 0
        total_products = 0

    context = {
        "stores": stores,
        "recent_orders": recent_orders,
        "total_sales": total_sales,
        "total_products": total_products,
    }
    return render(request, "shop/vendor/dashboard.html", context)


@vendor_required
def store_list(request):
    """Vendor's store list - vendors only"""
    stores = Store.objects.filter(vendor=request.user)
    context = {"stores": stores}
    return render(request, "shop/vendor/store_list.html", context)


@vendor_required
def store_create(request):
    """Create new store - vendors only"""
    if request.method == "POST":
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            store = form.save(commit=False)
            store.vendor = request.user
            store.save()
            messages.success(request, "Store created successfully!")
            return redirect("shop:store_detail", pk=store.pk)
    else:
        form = StoreForm()
    context = {"form": form}
    return render(request, "shop/vendor/store_form.html", context)


def store_detail(request, pk):
    """Store detail view"""
    store = get_object_or_404(Store, pk=pk, is_active=True)
    products = store.products.filter(is_active=True).order_by("-created_at")
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "store": store,
        "page_obj": page_obj,
    }
    return render(request, "shop/store_detail.html", context)


def about(request):
    """Simple About page"""
    return render(request, "shop/about.html")


def contact(request):
    """Simple Contact page"""
    return render(request, "shop/contact.html")


def cart_detail(request):
    """Display session-based shopping cart - works for anonymous users"""
    # Use module-level Decimal and SessionCart
    session_cart = SessionCart(request)
    cart_items = list(session_cart)

    total = session_cart.get_total_price()
    tax = total * Decimal("0.08")  # 8% tax
    grand_total = total + tax

    return render(
        request,
        "shop/cart.html",
        {
            "cart": session_cart,
            "cart_items": cart_items,
            "total": total,
            "tax": tax,
            "grand_total": grand_total,
        },
    )


def update_session_cart(request, product_id):
    """Update product quantity in session cart"""
    if request.method == "POST":
        session_cart = SessionCart(request)
        product = get_object_or_404(Product, id=product_id)

        try:
            quantity = int(request.POST.get("quantity", 1))
            if quantity > 0:
                if quantity <= product.stock:
                    session_cart.add(
                        product=product,
                        quantity=quantity,
                        override_quantity=True,
                    )
                    messages.success(
                        request,
                        f"Updated {product.name} quantity to {quantity}",
                    )
                else:
                    messages.error(
                        request,
                        (
                            f"Only {product.stock} units available for "
                            f"{product.name}"
                        ),
                    )
            else:
                messages.error(request, "Quantity must be greater than 0")
        except (ValueError, TypeError):
            messages.error(request, "Invalid quantity")

    return redirect("shop:cart_detail")


def remove_from_session_cart(request, product_id):
    """Remove product from session cart"""
    session_cart = SessionCart(request)
    product = get_object_or_404(Product, id=product_id)

    session_cart.remove(product)
    messages.success(request, f"Removed {product.name} from cart")

    return redirect("shop:cart_detail")


def cart_debug(request):
    """Debug view to see cart contents and structure"""
    # Use module-level Decimal and SessionCart
    session_cart = SessionCart(request)
    cart_items = list(session_cart)

    total = session_cart.get_total_price()
    tax = total * Decimal("0.08")
    grand_total = total + tax

    # Add extra debug info
    debug_info = {
        "session_key": request.session.session_key,
        "session_cart_raw": request.session.get("cart", {}),
        "cart_length": len(session_cart),
        "cart_items_type": type(cart_items),
        "cart_items_count": len(cart_items),
    }

    return render(
        request,
        "shop/cart_debug.html",
        {
            "cart": session_cart,
            "cart_items": cart_items,
            "total": total,
            "tax": tax,
            "grand_total": grand_total,
            "debug_info": debug_info,
        },
    )


def add_test_items(request):
    """Add test items to cart for debugging"""
    session_cart = SessionCart(request)

    # Get first 3 products
    products = Product.objects.all()[:3]

    for i, product in enumerate(products, 1):
        session_cart.add(product=product, quantity=i)
        messages.success(request, f"Added {i}x {product.name} to cart")

    return redirect("shop:cart_debug")


def cart_test(request):
    """Test page for cart functionality"""
    return render(request, "shop/cart_test.html")


def cart_dropdown_test(request):
    """Test page for cart dropdown functionality"""
    return render(request, "shop/cart_dropdown_test.html")


def cart_api(request):
    """API endpoint to get cart data as JSON for dropdown"""
    # Use module-level Decimal, JsonResponse, and SessionCart
    cart_items = list(SessionCart(request))

    # Convert cart items to JSON-serializable format
    items_data = []
    for item in cart_items:
        # Build full image URL
        image_url = None
        if item["product"].image:
            image_url = request.build_absolute_uri(item["product"].image.url)

        items_data.append(
            {
                "product": {
                    "id": item["product"].id,
                    "name": item["product"].name,
                    "price": str(item["product"].price),
                    "image": image_url,
                    "store": item["product"].store.name,
                },
                "quantity": item["quantity"],
                "price": str(item["price"]),
                "total_price": str(item["total_price"]),
            }
        )

    total = SessionCart(request).get_total_price()
    tax = total * Decimal("0.08")
    grand_total = total + tax

    return JsonResponse(
        {
            "items": items_data,
            "total": str(total),
            "tax": str(tax),
            "grand_total": str(grand_total),
            "items_count": len(cart_items),
        }
    )
