"""URL configuration for the ecommerce shop app     # Cart operations (session-based)
     path('cart/', views.cart_detail, name='cart_detail'),
     path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

     # New session-based cart URLs
     path('cart/remove/<int:product_id>/',
          views_extra.cart_remove, name='cart_remove'),
     path('cart/update/', views_extra.cart_update, name='cart_update'),
     path('cart/checkout/', views_extra.cart_checkout, name='cart_checkout'),

     # Legacy cart operations (keeping for backward compatibility)
     path(
          'cart/update/<int:item_id>/',
          views.update_cart_item,
          name='update_cart_item',
     ),
     path(
          'cart/remove/<int:item_id>/',
          views.remove_from_cart,
          name='remove_from_cart',
     ),
     path('checkout/', views.checkout, name='checkout'),s module defines all URL patterns for the shop including  # noqa: E501
product views, cart functionality, user authentication, and admin features.
"""

from django.contrib.auth import views as auth_views  # type: ignore
from django.urls import path  # type: ignore
from django.views.generic import RedirectView  # type: ignore

from . import views, views_extra

APP_NAME = "shop"
# Django requires lowercase 'app_name' variable - pylint: disable=invalid-name
app_name = APP_NAME
urlpatterns = [
    # Public views
    path("", views.home, name="home"),
    path("products/", views.product_list, name="product_list"),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
    path("search/", views_extra.search_products, name="search_products"),
    path("stores/<int:pk>/", views.store_detail, name="store_detail"),
    # Authentication
    path("register/", views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    # Support legacy redirects that point to /accounts/login/ (some
    # decorators or external links use this path). Redirect to the
    # canonical shop:login route and preserve the querystring (next=...)
    path(
        "accounts/login/",
        RedirectView.as_view(pattern_name="shop:login", permanent=False, query_string=True),
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", views.profile, name="profile"),
    # Customer Dashboard
    path("customer/", views.customer_dashboard, name="customer_dashboard"),
    # Password Reset
    path(
        "password-reset/",
        views_extra.password_reset_request,
        name="password_reset_request",
    ),
    path(
        "password-reset/<uuid:token>/",
        views_extra.password_reset_confirm,
        name="password_reset_confirm",
    ),
    # Cart and Checkout (Session-based)
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/debug/", views.cart_debug, name="cart_debug"),
    path("cart/test/", views.add_test_items, name="add_test_items"),
    path("cart/test-page/", views.cart_test, name="cart_test"),
    path("cart/api/", views.cart_api, name="cart_api"),
    path(
        "cart/dropdown-test/",
        views.cart_dropdown_test,
        name="cart_dropdown_test",
    ),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path(
        "cart/update/<int:product_id>/",
        views.update_session_cart,
        name="update_session_cart",
    ),
    path(
        "cart/remove/<int:product_id>/",
        views.remove_from_session_cart,
        name="remove_from_session_cart",
    ),
    path("checkout/", views.checkout, name="checkout"),
    # Legacy cart operations (keeping for backward compatibility)
    path(
        "cart/update-old/<int:item_id>/",
        views.update_cart_item,
        name="update_cart_item",
    ),
    path(
        "cart/remove-old/<int:item_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    # Orders
    path("orders/", views.order_history, name="order_history"),
    path("orders/<str:order_id>/", views.order_detail, name="order_detail"),
    # Reviews
    path(
        "products/<int:product_id>/review/",
        views.add_review,
        name="add_review",
    ),
    # Vendor Dashboard
    path("vendor/", views.vendor_dashboard, name="vendor_dashboard"),
    path(
        "vendor/products/",
        views_extra.vendor_products,
        name="vendor_products",
    ),
    # Store Management
    path("vendor/stores/", views.store_list, name="store_list"),
    path("vendor/stores/create/", views.store_create, name="store_create"),
    path(
        "vendor/stores/<int:pk>/update/",
        views_extra.store_update,
        name="store_update",
    ),
    path(
        "vendor/stores/<int:pk>/delete/",
        views_extra.store_delete,
        name="store_delete",
    ),
    # Product Management
    path(
        "vendor/stores/<int:store_id>/products/create/",
        views_extra.product_create,
        name="product_create",
    ),
    path(
        "vendor/products/<int:pk>/update/",
        views_extra.product_update,
        name="product_update",
    ),
    path(
        "vendor/products/<int:pk>/delete/",
        views_extra.product_delete,
        name="product_delete",
    ),
    # Static-ish pages
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    # Category Management (Admin only)
    path(
        "admin/categories/",
        views_extra.category_list,
        name="category_list",
    ),
    path(
        "admin/categories/create/",
        views_extra.category_create,
        name="category_create",
    ),
    path(
        "admin/categories/<int:pk>/update/",
        views_extra.category_update,
        name="category_update",
    ),
    path(
        "admin/categories/<int:pk>/delete/",
        views_extra.category_delete,
        name="category_delete",
    ),
]
