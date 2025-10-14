"""
Updated cart views using session-based cart functionality.
"""

import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from .cart import Cart
from .models import Order, OrderItem, Product
from .permissions import buyer_required


def cart_add(request, product_id):
    """Add product to session cart - works for anonymous users."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))

        # Check stock availability
        if quantity > product.quantity:
            messages.error(
                request,
                f"Sorry, only {product.quantity} items available in stock.",
            )
            return redirect("shop:product_detail", pk=product_id)

        # Check if adding this quantity would exceed stock
        current_quantity = 0
        if str(product_id) in cart.cart:
            current_quantity = cart.cart[str(product_id)]["quantity"]

        if current_quantity + quantity > product.quantity:
            available = product.quantity - current_quantity
            messages.error(
                request,
                f"Sorry, only {available} more items can be added to cart.",
            )
            return redirect("shop:product_detail", pk=product_id)

        cart.add(product=product, quantity=quantity)
        messages.success(request, f"{product.name} added to cart!")

        # Return JSON response for AJAX requests
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(
                {
                    "success": True,
                    "message": f"{product.name} added to cart!",
                    "cart_count": len(cart),
                }
            )

    return redirect("shop:cart_detail")


def cart_remove(request, product_id):
    """Remove product from session cart."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f"{product.name} removed from cart.")
    return redirect("shop:cart_detail")


def cart_detail(request):
    """Display cart contents."""
    cart = Cart(request)

    # Calculate totals
    cart_items = []
    total_price = 0

    for item in cart:
        cart_items.append(item)
        total_price += item["total_price"]

    context = {
        "cart": cart,
        "cart_items": cart_items,
        "total_price": total_price,
    }
    return render(request, "shop/cart/detail.html", context)


@csrf_exempt
def cart_update(request):
    """Update cart item quantities via AJAX."""
    if request.method == "POST":
        cart = Cart(request)
        data = json.loads(request.body)
        product_id = data.get("product_id")
        quantity = int(data.get("quantity", 0))

        if quantity > 0:
            product = get_object_or_404(Product, id=product_id)
            if quantity <= product.quantity:
                cart.add(product=product, quantity=quantity, override_quantity=True)
                return JsonResponse(
                    {
                        "success": True,
                        "cart_count": len(cart),
                        "total_price": str(cart.get_total_price()),
                    }
                )
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "error": f"Only {product.quantity} items available",
                    }
                )
        else:
            product = get_object_or_404(Product, id=product_id)
            cart.remove(product)
            return JsonResponse(
                {
                    "success": True,
                    "cart_count": len(cart),
                    "total_price": str(cart.get_total_price()),
                }
            )

    return JsonResponse({"success": False})


@login_required
@buyer_required
def cart_checkout(request):
    """Convert session cart to order for authenticated users."""
    cart = Cart(request)

    if len(cart) == 0:
        messages.error(request, "Your cart is empty.")
        return redirect("shop:cart_detail")

    if request.method == "POST":
        # Get shipping address
        shipping_address = request.POST.get("shipping_address", "")
        if not shipping_address:
            messages.error(request, "Please provide a shipping address.")
            return render(request, "shop/cart/checkout.html", {"cart": cart})

        # Create order
        total_amount = cart.get_total_price()
        order = Order.objects.create(
            buyer=request.user,
            total_amount=total_amount,
            shipping_address=shipping_address,
            status="pending",
        )

        # Create order items and update stock
        for item in cart:
            product = item["product"]
            quantity = item["quantity"]

            # Check stock again before creating order
            if quantity > product.quantity:
                messages.error(request, f"Sorry, {product.name} is out of stock.")
                order.delete()
                return redirect("shop:cart_detail")

            # Create order item
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price,
            )

            # Update product stock
            product.quantity -= quantity
            product.save()

        # Clear cart
        cart.clear()

        messages.success(request, f"Order {order.order_id} placed successfully!")
        return redirect("shop:order_history")

    context = {
        "cart": cart,
        "total_price": cart.get_total_price(),
    }
    return render(request, "shop/cart/checkout.html", context)
