"""
Template context processors for authentication and permissions
"""

# The following disables are intentional: this module performs
# runtime imports after django.setup() and accesses Django model
# managers dynamically. Silence editor/static-analysis noise here
# without changing runtime behavior.
# pylint: disable=no-member,import-outside-toplevel,broad-except

from main.shop_permissions import (
    user_can_access_admin,
    user_has_role,
    user_is_admin,
    user_is_buyer,
    user_is_vendor,
)


def auth_context(request):
    """
    Add authentication and permission context to all templates
    """
    context = {
        "user_is_authenticated": request.user.is_authenticated,
        "user_is_anonymous": request.user.is_anonymous,
    }

    if request.user.is_authenticated:
        context.update(
            {
                "user_is_vendor": user_is_vendor(request.user),
                "user_is_buyer": user_is_buyer(request.user),
                "user_is_admin": user_is_admin(request.user),
                "user_can_access_admin": user_can_access_admin(request.user),
                "user_is_staff": request.user.is_staff,
                "user_is_superuser": request.user.is_superuser,
            }
        )

        # Add user role if profile exists
        if hasattr(request.user, "profile") and request.user.profile:
            context["user_role"] = request.user.profile.role
        else:
            context["user_role"] = None

        # Add user's full name
        context["user_full_name"] = (
            request.user.get_full_name() or request.user.username
        )

        # Add user's stores count if vendor
        if user_is_vendor(request.user):
            try:
                # Import moved inside the request-time branch to avoid
                # import-time side-effects in some editor/static-analysis
                # environments. Keep runtime behavior identical.
                # pylint: disable=import-outside-toplevel
                from .shop_models import Store

                # pylint: enable=import-outside-toplevel

                context["user_stores_count"] = Store.objects.filter(
                    vendor=request.user
                ).count()  # pylint: disable=no-member
            except Exception:  # pylint: disable=broad-except
                context["user_stores_count"] = 0

        # Add user's orders count if buyer
        if user_is_buyer(request.user):
            try:
                # pylint: disable=import-outside-toplevel
                from .shop_models import Order

                # pylint: enable=import-outside-toplevel

                context["user_orders_count"] = Order.objects.filter(
                    buyer=request.user
                ).count()  # pylint: disable=no-member
            except Exception:  # pylint: disable=broad-except
                context["user_orders_count"] = 0

    # Add cart items count (session-based) - available for all users
    try:
        from .cart import Cart  # pylint: disable=import-outside-toplevel

        cart = Cart(request)
        context["cart_items_count"] = len(cart)
        context["cart_total"] = cart.get_total_price()
        context["cart_has_items"] = len(cart) > 0
        # Debug info (remove in production)
        context["session_key"] = request.session.session_key
        context["cart_session_data"] = request.session.get("cart", {})
    except Exception as e:  # pylint: disable=broad-except
        context["cart_items_count"] = 0
        context["cart_total"] = 0
        context["cart_has_items"] = False
        # Debug error (remove in production)
        context["cart_error"] = str(e)

    return context


def permissions_context(request):
    """
    Add permission-checking functions to template context
    """
    return {
        "user_has_role": lambda role: user_has_role(request.user, role),
        "user_is_vendor": lambda: user_is_vendor(request.user),
        "user_is_buyer": lambda: user_is_buyer(request.user),
        "user_is_admin": lambda: user_is_admin(request.user),
        "user_can_access_admin": lambda: user_can_access_admin(request.user),
    }


def navigation_context(request):
    """
    Add navigation context based on user permissions
    """
    nav_items = []

    if request.user.is_authenticated:
        # Common authenticated user navigation
        nav_items.extend(
            [
                {"name": "Home", "url": "shop:home", "icon": "fas fa-home"},
                {
                    "name": "Products",
                    "url": "shop:product_list",
                    "icon": "fas fa-box",
                },
            ]
        )

        # Buyer-specific navigation
        if user_is_buyer(request.user):
            nav_items.extend(
                [
                    {
                        "name": "Dashboard",
                        "url": "shop:customer_dashboard",
                        "icon": "fas fa-tachometer-alt",
                    },
                    {
                        "name": "Cart",
                        "url": "shop:cart_detail",
                        "icon": "fas fa-shopping-cart",
                    },
                    {
                        "name": "Orders",
                        "url": "shop:order_history",
                        "icon": "fas fa-list",
                    },
                ]
            )

        # Vendor-specific navigation
        if user_is_vendor(request.user):
            nav_items.extend(
                [
                    {
                        "name": "Vendor Dashboard",
                        "url": "shop:vendor_dashboard",
                        "icon": "fas fa-store",
                    },
                    {
                        "name": "My Stores",
                        "url": "shop:store_list",
                        "icon": "fas fa-building",
                    },
                    {
                        "name": "My Products",
                        "url": "shop:vendor_products",
                        "icon": "fas fa-boxes",
                    },
                ]
            )

        # Admin-specific navigation
        if user_can_access_admin(request.user):
            nav_items.extend(
                [
                    {
                        "name": "Admin Panel",
                        "url": "admin:index",
                        "icon": "fas fa-cog",
                    },
                    {
                        "name": "Categories",
                        "url": "shop:category_list",
                        "icon": "fas fa-tags",
                    },
                ]
            )

        # Common user navigation
        nav_items.extend(
            [
                {
                    "name": "Profile",
                    "url": "shop:profile",
                    "icon": "fas fa-user",
                },
                {
                    "name": "Logout",
                    "url": "shop:logout",
                    "icon": "fas fa-sign-out-alt",
                },
            ]
        )

    else:
        # Anonymous user navigation
        nav_items.extend(
            [
                {"name": "Home", "url": "shop:home", "icon": "fas fa-home"},
                {
                    "name": "Products",
                    "url": "shop:product_list",
                    "icon": "fas fa-box",
                },
                {
                    "name": "Login",
                    "url": "shop:login",
                    "icon": "fas fa-sign-in-alt",
                },
                {
                    "name": "Register",
                    "url": "shop:register",
                    "icon": "fas fa-user-plus",
                },
            ]
        )

    return {
        "nav_items": nav_items,
        "user_dashboard_url": _get_user_dashboard_url(request.user),
    }


def _get_user_dashboard_url(user):
    """Get appropriate dashboard URL based on user role"""
    if not user.is_authenticated:
        return None

    if user_is_vendor(user):
        return "shop:vendor_dashboard"
    elif user_is_buyer(user):
        return "shop:customer_dashboard"
    elif user_can_access_admin(user):
        return "admin:index"
    else:
        return "shop:home"


def breadcrumb_context(request):
    """
    Generate breadcrumb navigation based on current URL
    """
    breadcrumbs = [{"name": "Home", "url": "shop:home"}]

    # Map URLs to breadcrumb paths
    url_breadcrumbs = {
        "shop:product_list": [{"name": "Products", "url": None}],
        "shop:customer_dashboard": [
            {"name": "Customer Dashboard", "url": None},
        ],
        "shop:vendor_dashboard": [{"name": "Vendor Dashboard", "url": None}],
        "shop:store_list": [
            {"name": "Vendor Dashboard", "url": "shop:vendor_dashboard"},
            {"name": "My Stores", "url": None},
        ],
        "shop:vendor_products": [
            {"name": "Vendor Dashboard", "url": "shop:vendor_dashboard"},
            {"name": "My Products", "url": None},
        ],
        "shop:cart_detail": [{"name": "Shopping Cart", "url": None}],
        "shop:checkout": [
            {"name": "Shopping Cart", "url": "shop:cart_detail"},
            {"name": "Checkout", "url": None},
        ],
        "shop:order_history": [{"name": "Order History", "url": None}],
        "shop:category_list": [
            {"name": "Admin", "url": "admin:index"},
            {"name": "Categories", "url": None},
        ],
    }

    # Get current URL name
    current_url = None
    try:
        if hasattr(request, "resolver_match") and request.resolver_match:
            current_url = request.resolver_match.url_name
            if request.resolver_match.namespace:
                namespace = request.resolver_match.namespace
                current_url = f"{namespace}:{current_url}"
    except Exception:
        pass

    # Add breadcrumbs for current URL
    if current_url in url_breadcrumbs:
        breadcrumbs.extend(url_breadcrumbs[current_url])

    return {"breadcrumbs": breadcrumbs}
