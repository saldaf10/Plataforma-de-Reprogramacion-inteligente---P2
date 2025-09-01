from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from catalog.models import Product


def _get_cart(session):
    cart = session.get("cart", {})
    return cart


def _save_cart(session, cart):
    session["cart"] = cart
    session.modified = True


def cart_detail(request):
    if request.user.is_authenticated and hasattr(request.user, "profile") and request.user.profile.role in {"manager", "repartidor"}:
        return redirect("orders:my_orders")
    cart = _get_cart(request.session)
    items = []
    total = 0
    for pid, item in cart.items():
        product = get_object_or_404(Product, id=pid)
        quantity = int(item.get("quantity", 1))
        line_total = product.price * quantity
        total += line_total
        items.append({"product": product, "quantity": quantity, "line_total": line_total})
    return render(request, "cart/detail.html", {"items": items, "total": total})


@require_POST
def cart_add(request, product_id: int):
    if request.user.is_authenticated and hasattr(request.user, "profile") and request.user.profile.role in {"manager", "repartidor"}:
        return redirect("orders:my_orders")
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get("quantity", 1))
    cart = _get_cart(request.session)
    key = str(product.id)
    if key in cart:
        cart[key]["quantity"] = int(cart[key]["quantity"]) + quantity
    else:
        cart[key] = {"quantity": quantity}
    _save_cart(request.session, cart)
    return redirect("cart:detail")


@require_POST
def cart_update(request, product_id: int):
    if request.user.is_authenticated and hasattr(request.user, "profile") and request.user.profile.role in {"manager", "repartidor"}:
        return redirect("orders:my_orders")
    quantity = int(request.POST.get("quantity", 1))
    cart = _get_cart(request.session)
    key = str(product_id)
    if key in cart:
        cart[key]["quantity"] = quantity
        _save_cart(request.session, cart)
    return redirect("cart:detail")


def cart_remove(request, product_id: int):
    if request.user.is_authenticated and hasattr(request.user, "profile") and request.user.profile.role in {"manager", "repartidor"}:
        return redirect("orders:my_orders")
    cart = _get_cart(request.session)
    key = str(product_id)
    if key in cart:
        del cart[key]
        _save_cart(request.session, cart)
    return redirect("cart:detail")
from django.shortcuts import render

# Create your views here.
