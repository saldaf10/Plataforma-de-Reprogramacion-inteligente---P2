from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from catalog.models import Product
from .models import Order, OrderItem, Delivery, DeliveryEvent, DeliveryComment


@login_required
@transaction.atomic
def checkout(request):
    cart = request.session.get("cart", {})
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        address = request.POST.get("address")
        city = request.POST.get("city")
        postal_code = request.POST.get("postal_code")

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            address=address,
            city=city,
            postal_code=postal_code,
        )

        total = 0
        for pid, item in cart.items():
            product = get_object_or_404(Product, id=pid)
            qty = int(item.get("quantity", 1))
            OrderItem.objects.create(order=order, product=product, price=product.price, quantity=qty)
            total += product.price * qty
        order.total_amount = total
        order.save()

        # Redirigir a simulación de pago
        request.session["last_order_id"] = order.id
        return redirect("payments:simulate")

    # GET: mostrar resumen previo
    items = []
    total = 0
    for pid, item in cart.items():
        product = get_object_or_404(Product, id=pid)
        qty = int(item.get("quantity", 1))
        line_total = product.price * qty
        total += line_total
        items.append({"product": product, "quantity": qty, "line_total": line_total})
    return render(request, "orders/checkout.html", {"items": items, "total": total})


@login_required
def order_summary(request, order_id: int):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/summary.html", {"order": order})


@login_required
def my_orders(request):
    user = request.user
    if user.is_superuser:
        orders = Order.objects.all().order_by("-created_at")
    elif hasattr(user, "profile") and user.profile.role == "repartidor":
        # Mostrar entregas asignadas al rider
        deliveries = Delivery.objects.select_related("order").filter(rider=user).order_by("-created_at")
        return render(request, "orders/rider_orders.html", {"deliveries": deliveries})
    elif hasattr(user, "profile") and user.profile.role == "manager":
        orders = Order.objects.all().order_by("-created_at")
    else:
        orders = Order.objects.filter(user=user).order_by("-created_at")
        # Próximo pedido no entregado
        next_delivery = (
            Delivery.objects.select_related("order")
            .filter(order__user=user)
            .exclude(status="entregada")
            .order_by("order__created_at")
            .first()
        )
        return render(request, "orders/my_orders.html", {"orders": orders, "next_delivery": next_delivery})


@login_required
def delivery_detail(request, order_id: int):
    order = get_object_or_404(Order, id=order_id)
    delivery, _ = Delivery.objects.get_or_create(order=order)
    # Cliente solo su orden; superuser/manager cualquier orden; rider si está asignado
    # Determine role
    user_role = None
    if request.user.is_superuser:
        user_role = "manager"
    elif hasattr(request.user, "profile"):
        user_role = request.user.profile.role

    if user_role == "manager":
        pass
    elif user_role == "repartidor":
        pass
    else:
        # Cliente u otro: solo su orden
        if order.user_id != request.user.id:
            return redirect("orders:my_orders")

    if request.method == "POST":
        # Actualizaciones dependiendo del rol
        action = request.POST.get("action")
        if user_role == "manager":
            if action == "assign":
                before = delivery.status
                rider_id = request.POST.get("rider_id")
                delivery.scheduled_date = request.POST.get("scheduled_date") or delivery.scheduled_date
                delivery.scheduled_window = request.POST.get("scheduled_window") or delivery.scheduled_window
                if rider_id:
                    delivery.rider_id = int(rider_id)
                    delivery.status = "asignada"
                delivery.save()
                DeliveryEvent.objects.create(
                    delivery=delivery,
                    user=request.user,
                    status_before=before,
                    status_after=delivery.status,
                    notes=f"Asignado rider {delivery.rider.username if delivery.rider else ''}"
                )
            elif action == "manager_comment":
                msg = request.POST.get("message", "").strip()
                photo = request.FILES.get("photo")
                if msg or photo:
                    DeliveryComment.objects.create(
                        delivery=delivery,
                        user=request.user,
                        role="manager",
                        message=msg,
                        photo=photo,
                    )
        elif user_role == "repartidor":
            if action in {"en_ruta", "fallida", "entregada", "reprogramada"}:
                before = delivery.status
                delivery.status = action
                delivery.failure_reason = request.POST.get("failure_reason", "")
                delivery.notes = request.POST.get("notes", "")
                photo_file = request.FILES.get("photo")
                if photo_file:
                    delivery.photo = photo_file
                delivery.save()
                DeliveryEvent.objects.create(
                    delivery=delivery,
                    user=request.user,
                    status_before=before,
                    status_after=delivery.status,
                    notes=delivery.notes,
                    photo=delivery.photo if photo_file else None,
                )
        # Cliente no actualiza estado aquí

        return redirect("orders:delivery_detail", order_id=order.id)

    # Render por rol
    context = {"order": order, "delivery": delivery}
    if user_role == "manager":
        from django.contrib.auth.models import User
        riders = User.objects.filter(profile__role="repartidor")
        context["riders"] = riders
        context["events"] = delivery.events.all()
        context["comments"] = delivery.comments.all()
        return render(request, "orders/delivery_manager.html", context)
    if user_role == "repartidor":
        context["events"] = delivery.events.all()
        context["comments"] = delivery.comments.all()
        return render(request, "orders/delivery_rider.html", context)
    # Cliente
    context["events"] = delivery.events.all()
    context["comments"] = delivery.comments.all()
    return render(request, "orders/delivery_client.html", context)


@login_required
def manager_panel(request):
    user = request.user
    if not user.is_superuser and (not hasattr(user, "profile") or user.profile.role != "manager"):
        return redirect("orders:my_orders")

    status = request.GET.get("status", "")
    q = request.GET.get("q", "")

    orders_qs = Order.objects.select_related("user").prefetch_related("items", "delivery").all()
    if status:
        orders_qs = orders_qs.filter(delivery__status=status)
    if q:
        orders_qs = orders_qs.filter(
            models.Q(full_name__icontains=q)
            | models.Q(address__icontains=q)
            | models.Q(city__icontains=q)
            | models.Q(email__icontains=q)
            | models.Q(id__icontains=q)
        )

    total = orders_qs.count()
    delivered = orders_qs.filter(delivery__status="entregada").count()
    failed = orders_qs.filter(delivery__status="fallida").count()
    pending = orders_qs.exclude(delivery__status="entregada").exclude(delivery__status="fallida").count()

    deliveries_by_status = Delivery.objects.values("status").annotate(c=Count("id"))

    return render(
        request,
        "orders/manager_panel.html",
        {
            "orders": orders_qs.order_by("-created_at")[:200],
            "total": total,
            "delivered": delivered,
            "failed": failed,
            "pending": pending,
            "deliveries_by_status": deliveries_by_status,
            "status": status,
            "q": q,
        },
    )
from django.shortcuts import render

# Create your views here.
