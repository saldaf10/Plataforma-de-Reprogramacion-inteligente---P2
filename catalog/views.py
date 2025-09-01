from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Product, Category


def product_list(request):
    # Restringir a solo clientes/anonimos
    if request.user.is_authenticated and hasattr(request.user, "profile") and request.user.profile.role in {"manager", "repartidor"}:
        return redirect("orders:my_orders")
    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category")
    min_price = request.GET.get("min")
    max_price = request.GET.get("max")

    products = Product.objects.select_related("category").all()

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    if category_slug:
        products = products.filter(category__slug=category_slug)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    categories = Category.objects.all()

    return render(
        request,
        "catalog/product_list.html",
        {"products": products, "categories": categories, "query": query},
    )


def product_detail(request, slug: str):
    if request.user.is_authenticated and hasattr(request.user, "profile") and request.user.profile.role in {"manager", "repartidor"}:
        return redirect("orders:my_orders")
    product = get_object_or_404(Product, slug=slug)
    similar = (
        Product.objects.filter(category=product.category)
        .exclude(id=product.id)
        .order_by("-created_at")[:4]
    )
    return render(request, "catalog/product_detail.html", {"product": product, "similar": similar})
