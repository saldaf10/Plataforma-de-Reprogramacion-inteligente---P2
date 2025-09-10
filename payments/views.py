from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from orders.models import Order, Delivery
from django.contrib.auth.models import User


@login_required
def simulate_payment(request):
    order_id = request.session.get("last_order_id")
    if not order_id:
        return redirect("catalog:product_list")
    if request.method == "POST":
        outcome = request.POST.get("outcome", "success")
        if outcome == "success":
            return redirect("payments:success")
        return redirect("payments:failed")
    return render(request, "payments/simulate.html", {})


@login_required
def payment_success(request):
    order_id = request.session.get("last_order_id")
    if not order_id:
        return redirect("catalog:product_list")
    order = Order.objects.get(id=order_id, user=request.user)
    order.paid = True
    order.save()
    # Crear Delivery si no existe
    delivery, _ = Delivery.objects.get_or_create(order=order)
    # Auto-asignación: rider con menos entregas activas (no entregada)
    riders = (
        User.objects.filter(profile__role="repartidor")
        .annotate(active_count=Count("deliveries", filter=~Q(deliveries__status="entregada")))
        .order_by("active_count", "id")
    )
    if riders.exists():
        delivery.rider = riders.first()
        delivery.status = "asignada"
        delivery.save()
    # Vaciar carrito
    request.session["cart"] = {}
    request.session.modified = True
    return redirect("orders:summary", order_id=order.id)


@login_required
def payment_failed(request):
    return render(request, "payments/failed.html", {})
from django.shortcuts import render

# Create your views here.
