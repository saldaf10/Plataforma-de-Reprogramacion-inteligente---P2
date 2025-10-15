from django.shortcuts import redirect, render
from catalog.models import Product


def home_redirect(request):
    user = request.user
    if user.is_authenticated and user.is_superuser:
        return redirect("orders:panel")
    if user.is_authenticated and hasattr(user, "profile"):
        if user.profile.role == "manager":
            return redirect("orders:panel")
        if user.profile.role == "repartidor":
            return redirect("orders:my_orders")
        if user.profile.role == "cliente":
            return redirect("catalog:product_list")
    
    # Para usuarios no autenticados, mostrar landing page
    featured_products = Product.objects.all()[:6]
    return render(request, "home.html", {"featured_products": featured_products})

