from django.shortcuts import redirect


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
            return redirect("orders:my_orders")
    return redirect("catalog:product_list")

