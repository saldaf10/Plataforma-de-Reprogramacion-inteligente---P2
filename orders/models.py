from django.db import models
from django.contrib.auth import get_user_model
from catalog.models import Product


User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    paid = models.BooleanField(default=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f"Order #{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_line_total(self):
        return self.price * self.quantity


class Delivery(models.Model):
    STATUS_CHOICES = (
        ("pendiente", "Pendiente"),
        ("asignada", "Asignada"),
        ("en_ruta", "En ruta"),
        ("fallida", "Fallida"),
        ("reprogramada", "Reprogramada"),
        ("entregada", "Entregada"),
    )
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="delivery")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pendiente")
    rider = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="deliveries")
    scheduled_date = models.DateField(null=True, blank=True)
    scheduled_window = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    photo = models.ImageField(upload_to="deliveries/", null=True, blank=True)
    failure_reason = models.CharField(max_length=120, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Delivery #{self.pk} - Order {self.order_id} ({self.get_status_display()})"

    @property
    def estimated_datetime(self):
        from datetime import datetime, timedelta
        
        # Si hay fecha programada, usar esa como base para el estimado
        if self.scheduled_date:
            # Si hay ventana horaria programada, intentar parsear la hora inicial
            if self.scheduled_window:
                try:
                    # Formato esperado: "14:00-16:00" o "14:00"
                    time_parts = self.scheduled_window.split('-')[0].strip().split(':')
                    hour = int(time_parts[0])
                    minute = int(time_parts[1]) if len(time_parts) > 1 else 0
                    return datetime.combine(self.scheduled_date, datetime.min.time().replace(hour=hour, minute=minute))
                except (ValueError, IndexError):
                    # Si no se puede parsear, usar mediodía como hora por defecto
                    return datetime.combine(self.scheduled_date, datetime.min.time().replace(hour=12, minute=0))
            else:
                # Sin ventana horaria, usar mediodía
                return datetime.combine(self.scheduled_date, datetime.min.time().replace(hour=12, minute=0))
        
        # Si no hay fecha programada, usar el estimado original: 24 horas después de la creación
        return self.order.created_at + timedelta(days=1)
    
    @property
    def is_final_state(self):
        """Verifica si el pedido está en un estado final (no modificable)"""
        return self.status in ['entregada', 'fallida']
    
    @property
    def is_modifiable(self):
        """Verifica si el pedido puede ser modificado"""
        return not self.is_final_state


class DeliveryEvent(models.Model):
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name="events")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status_before = models.CharField(max_length=20, blank=True)
    status_after = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    photo = models.ImageField(upload_to="deliveries/events/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Event for Delivery {self.delivery_id} at {self.created_at}"


class DeliveryComment(models.Model):
    ROLE_CHOICES = (
        ("manager", "Manager"),
        ("repartidor", "Repartidor"),
        ("cliente", "Cliente"),
    )
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)
    message = models.TextField()
    photo = models.ImageField(upload_to="deliveries/comments/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Comment by {self.user_id or 'n/a'} on Delivery {self.delivery_id}"


class DeliveryNotification(models.Model):
    NOTIFICATION_TYPES = (
        ("approaching", "Aproximándose"),
        ("leaving", "Saliendo"),
        ("arriving_soon", "Llegando pronto (3 min)"),
        ("arrived", "Ha llegado"),
        ("delivered", "Entregado"),
        ("rescheduled", "Reprogramado"),
        ("failed", "Entrega Fallida"),
    )
    
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name="notifications")
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="delivery_notifications")
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ["-sent_at"]
    
    def __str__(self) -> str:
        return f"Notification {self.get_notification_type_display()} for {self.recipient.username}"
