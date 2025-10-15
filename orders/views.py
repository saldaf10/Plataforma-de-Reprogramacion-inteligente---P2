from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, Q
from django.contrib import messages
from catalog.models import Product
from .models import Order, OrderItem, Delivery, DeliveryEvent, DeliveryComment, DeliveryNotification
from .notification_service import DeliveryNotificationService


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
        return redirect("orders:panel")
    elif hasattr(user, "profile") and user.profile.role == "repartidor":
        # Mostrar entregas asignadas al rider
        deliveries = Delivery.objects.select_related("order").filter(rider=user).order_by("-created_at")
        return render(request, "orders/rider_orders.html", {"deliveries": deliveries})
    elif hasattr(user, "profile") and user.profile.role == "manager":
        return redirect("orders:panel")
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
        action = request.POST.get("action")
        
        # Verificar si el pedido está en estado final
        # EXCEPCIÓN: Permitir reprogramar pedidos fallidos (clientes)
        if delivery.is_final_state:
            # Si es cliente intentando reprogramar un pedido fallido, permitir
            if action == "reschedule" and delivery.status == "fallida" and (user_role == "cliente" or not user_role):
                pass  # Permitir continuar
            else:
                messages.error(request, "Este pedido no puede ser modificado porque está en estado final (entregado o fallido).")
                return redirect("orders:delivery_detail", order_id=order.id)
        
        # Actualizaciones dependiendo del rol
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
                
                # Si el pedido se marca como fallido, enviar notificación automática al cliente
                if action == "fallida":
                    failure_reason = delivery.failure_reason or delivery.notes or ""
                    DeliveryNotificationService.send_failed_notification(delivery, failure_reason)
                    messages.success(request, f"Entrega marcada como fallida. El cliente ha sido notificado automáticamente.")
                else:
                    messages.success(request, f"Estado actualizado a '{delivery.get_status_display()}'.")
            # Manejar notificaciones del repartidor
            elif action == "send_notification":
                # Validar que el pedido esté en un estado válido para notificaciones
                if not delivery.is_modifiable or delivery.status not in ['en_ruta', 'reprogramada']:
                    messages.error(request, "Las notificaciones solo se pueden enviar para pedidos activos en ruta o reprogramados.")
                else:
                    notification_type = request.POST.get("notification_type")
                    estimated_minutes = request.POST.get("estimated_minutes", "")
                    
                    if notification_type == "approaching":
                        minutes = int(estimated_minutes) if estimated_minutes.isdigit() else 30
                        DeliveryNotificationService.send_approaching_notification(delivery, minutes)
                        messages.success(request, f"Notificación enviada: El cliente será notificado que llegas en aproximadamente {minutes} minutos.")
                    elif notification_type == "leaving":
                        DeliveryNotificationService.send_leaving_notification(delivery)
                        messages.success(request, "Notificación enviada: El cliente fue notificado que ya saliste con su pedido.")
                    elif notification_type == "arriving_soon":
                        DeliveryNotificationService.send_arriving_soon_notification(delivery)
                        messages.success(request, "Notificación enviada: El cliente fue notificado que llegarás en 3 minutos.")
                    elif notification_type == "arrived":
                        DeliveryNotificationService.send_arrived_notification(delivery)
                        messages.success(request, "Notificación enviada: El cliente fue notificado que ya llegaste.")
                    elif notification_type == "delivered":
                        DeliveryNotificationService.send_delivered_notification(delivery)
                        messages.success(request, "Notificación enviada: El cliente fue notificado que su pedido fue entregado.")
        elif user_role == "cliente" or not user_role:
            # El cliente puede reprogramar su entrega si está en estado válido
            if action == "reschedule":
                # Solo permitir reprogramar si el estado lo permite (incluyendo fallidas)
                if delivery.status in ['pendiente', 'asignada', 'reprogramada', 'fallida']:
                    scheduled_date = request.POST.get("scheduled_date")
                    scheduled_window = request.POST.get("scheduled_window")
                    
                    if scheduled_date:
                        from datetime import datetime
                        try:
                            # Validar fecha
                            date_obj = datetime.strptime(scheduled_date, "%Y-%m-%d").date()
                            today = datetime.now().date()
                            
                            if date_obj < today:
                                messages.error(request, "No puedes seleccionar una fecha pasada.")
                            else:
                                old_date = delivery.scheduled_date
                                old_window = delivery.scheduled_window
                                
                                delivery.scheduled_date = date_obj
                                delivery.scheduled_window = scheduled_window if scheduled_window else None
                                delivery.status = "reprogramada"
                                delivery.save()
                                
                                # Crear evento
                                DeliveryEvent.objects.create(
                                    delivery=delivery,
                                    user=request.user,
                                    status_before=delivery.status,
                                    status_after="reprogramada",
                                    notes=f"Cliente reprogramó de {old_date} {old_window or ''} a {date_obj} {scheduled_window or ''}"
                                )
                                
                                # Enviar notificación al repartidor si está asignado
                                if delivery.rider:
                                    notification_message = f"📅 El cliente {request.user.username} ha reprogramado el pedido #{order.id} para el {date_obj}"
                                    if scheduled_window:
                                        notification_message += f" entre las {scheduled_window}"
                                    notification_message += ". Por favor, revisa los detalles actualizados."
                                    
                                    DeliveryNotification.objects.create(
                                        delivery=delivery,
                                        notification_type="rescheduled",
                                        recipient=delivery.rider,
                                        message=notification_message
                                    )
                                
                                messages.success(request, f"Tu entrega ha sido reprogramada para el {date_obj} {scheduled_window or ''}. Recibirás una confirmación pronto.")
                        except ValueError:
                            messages.error(request, "Fecha inválida. Por favor usa el formato correcto.")
                    else:
                        messages.error(request, "Debes seleccionar una fecha.")
                else:
                    messages.error(request, f"No puedes reprogramar un pedido en estado '{delivery.get_status_display()}'. Solo se pueden reprogramar pedidos pendientes, asignados, reprogramados o fallidos.")

        return redirect("orders:delivery_detail", order_id=order.id)

    # Render por rol
    from datetime import datetime
    context = {
        "order": order, 
        "delivery": delivery,
        "is_modifiable": delivery.is_modifiable,
        "is_final_state": delivery.is_final_state,
        "today": datetime.now().date()
    }
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
        context["can_send_notifications"] = DeliveryNotificationService.can_send_notifications(delivery)
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
            Q(full_name__icontains=q)
            | Q(address__icontains=q)
            | Q(city__icontains=q)
            | Q(email__icontains=q)
            | Q(id__icontains=q)
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


@login_required
def notifications(request):
    """Vista para mostrar las notificaciones del usuario"""
    notifications = DeliveryNotificationService.get_user_notifications(request.user, limit=20)
    
    # Marcar notificaciones como leídas si se especifica
    if request.method == "POST":
        notification_id = request.POST.get("notification_id")
        if notification_id:
            try:
                notification = DeliveryNotification.objects.get(
                    id=notification_id, 
                    recipient=request.user
                )
                DeliveryNotificationService.mark_as_read(notification)
                messages.success(request, "Notificación marcada como leída.")
            except DeliveryNotification.DoesNotExist:
                messages.error(request, "Notificación no encontrada.")
        
        return redirect("orders:notifications")
    
    return render(request, "orders/notifications.html", {
        "notifications": notifications
    })
