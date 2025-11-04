from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import DeliveryNotification, Delivery

User = get_user_model()


class DeliveryNotificationService:
    """Servicio para manejar las notificaciones de entrega"""
    
    @staticmethod
    def send_notification(delivery, notification_type, additional_message=""):
        """
        Envía una notificación al cliente sobre el estado de su entrega
        
        Args:
            delivery: Instancia de Delivery
            notification_type: Tipo de notificación (approaching, leaving, arriving_soon, arrived, delivered)
            additional_message: Mensaje adicional opcional
        """
        if not delivery.order.user:
            return None
            
        # Validar que el pedido esté en un estado válido para notificaciones
        if not delivery.is_modifiable or delivery.status not in ['en_ruta', 'reprogramada']:
            return None
            
        messages = {
            "approaching": f"🚚 Tu pedido #{delivery.order.id} está en camino. El repartidor {delivery.rider.username if delivery.rider else 'asignado'} se aproxima a tu ubicación.",
            "leaving": f"🚀 El repartidor {delivery.rider.username if delivery.rider else 'asignado'} ya salió con tu pedido #{delivery.order.id}. ¡Está en camino!",
            "arriving_soon": f"⏰ ¡Atención! Tu pedido #{delivery.order.id} llegará en aproximadamente 3 minutos. El repartidor {delivery.rider.username if delivery.rider else 'asignado'} está cerca.",
            "arrived": f"🏠 ¡Ya llegó! El repartidor {delivery.rider.username if delivery.rider else 'asignado'} está en tu dirección con el pedido #{delivery.order.id}. Por favor, prepárate para recibirlo.",
            "delivered": f"✅ ¡Pedido entregado! Tu pedido #{delivery.order.id} ha sido entregado exitosamente por {delivery.rider.username if delivery.rider else 'el repartidor'}. ¡Gracias por tu compra!",
        }
        
        base_message = messages.get(notification_type, "")
        if additional_message:
            base_message += f" {additional_message}"
            
        notification = DeliveryNotification.objects.create(
            delivery=delivery,
            notification_type=notification_type,
            recipient=delivery.order.user,
            message=base_message
        )
        
        return notification
    
    @staticmethod
    def send_approaching_notification(delivery, estimated_minutes=30):
        """Envía notificación cuando el repartidor se está aproximando"""
        message = f"Tiempo estimado de llegada: aproximadamente {estimated_minutes} minutos."
        return DeliveryNotificationService.send_notification(
            delivery, "approaching", message
        )
    
    @staticmethod
    def send_leaving_notification(delivery):
        """Envía notificación cuando el repartidor sale con el pedido"""
        return DeliveryNotificationService.send_notification(delivery, "leaving")
    
    @staticmethod
    def send_arriving_soon_notification(delivery):
        """Envía notificación cuando faltan 3 minutos para llegar"""
        return DeliveryNotificationService.send_notification(delivery, "arriving_soon")
    
    @staticmethod
    def send_arrived_notification(delivery):
        """Envía notificación cuando el repartidor ha llegado"""
        return DeliveryNotificationService.send_notification(delivery, "arrived")
    
    @staticmethod
    def send_delivered_notification(delivery):
        """Envía notificación cuando el pedido ha sido entregado"""
        return DeliveryNotificationService.send_notification(delivery, "delivered")
    
    @staticmethod
    def send_failed_notification(delivery, failure_reason=""):
        """
        Envía notificación automática cuando la entrega falla
        Esta notificación no requiere validación de estado modificable
        """
        if not delivery.order.user:
            return None
        
        # Construir mensaje de falla
        base_message = f"❌ Tu pedido #{delivery.order.id} no pudo ser entregado."
        
        if failure_reason:
            base_message += f" Motivo: {failure_reason}"
        else:
            base_message += " El repartidor intentó realizar la entrega pero no fue posible completarla."
        
        base_message += f" Puedes reprogramar tu entrega para una nueva fecha desde el detalle de tu pedido."
        
        # Crear notificación directamente sin pasar por send_notification
        # porque ese método valida is_modifiable
        notification = DeliveryNotification.objects.create(
            delivery=delivery,
            notification_type="failed",
            recipient=delivery.order.user,
            message=base_message
        )
        
        return notification
    
    @staticmethod
    def get_user_notifications(user, limit=10):
        """Obtiene las notificaciones más recientes de un usuario"""
        return DeliveryNotification.objects.filter(
            recipient=user
        ).select_related('delivery', 'delivery__order')[:limit]
    
    @staticmethod
    def mark_as_read(notification):
        """Marca una notificación como leída"""
        notification.read = True
        notification.save()
    
    @staticmethod
    def can_send_notifications(delivery):
        """
        Verifica si se pueden enviar notificaciones para una entrega
        
        Args:
            delivery: Instancia de Delivery
            
        Returns:
            bool: True si se pueden enviar notificaciones
        """
        return (
            delivery.order.user and 
            delivery.is_modifiable and  # Solo si es modificable
            delivery.status in ['en_ruta', 'reprogramada']
        )
    
    @staticmethod
    def get_coordinators():
        """Obtiene todos los usuarios con rol de coordinador/manager"""
        try:
            # Intentar obtener usuarios con perfil manager
            from accounts.models import UserProfile
            return User.objects.filter(
                Q(is_superuser=True) | 
                Q(profile__role="manager")
            ).distinct()
        except:
            # Fallback: solo superusuarios si no hay perfil
            return User.objects.filter(is_superuser=True)
    
    @staticmethod
    def notify_coordinators(delivery, notification_type, message):
        """
        Envía notificaciones a todos los coordinadores/managers
        
        Args:
            delivery: Instancia de Delivery
            notification_type: Tipo de notificación para coordinadores
            message: Mensaje de la notificación
        """
        from .models import DeliveryNotification
        coordinators = DeliveryNotificationService.get_coordinators()
        notifications = []
        
        for coordinator in coordinators:
            notification = DeliveryNotification.objects.create(
                delivery=delivery,
                notification_type=notification_type,
                recipient=coordinator,
                message=message
            )
            notifications.append(notification)
        
        return notifications
    
    @staticmethod
    def notify_coordinators_rescheduled(delivery, old_date=None, old_window=None, changed_by=None):
        """Notifica a coordinadores sobre una reprogramación"""
        from datetime import datetime
        
        date_str = delivery.scheduled_date.strftime("%d/%m/%Y") if delivery.scheduled_date else "No especificada"
        window_str = delivery.scheduled_window if delivery.scheduled_window else "No especificada"
        
        changed_by_str = ""
        if changed_by:
            changed_by_str = f" por {changed_by.username}"
        
        old_info = ""
        if old_date or old_window:
            old_date_str = old_date.strftime("%d/%m/%Y") if old_date else "No especificada"
            old_window_str = old_window if old_window else "No especificada"
            old_info = f" (anteriormente: {old_date_str} {old_window_str})"
        
        message = (
            f"📅 ALERTA DE REPROGRAMACIÓN - Pedido #{delivery.order.id}\n\n"
            f"La entrega del pedido #{delivery.order.id} ha sido reprogramada{changed_by_str}.\n\n"
            f"📌 Nueva programación:\n"
            f"   • Fecha: {date_str}\n"
            f"   • Franja horaria: {window_str}{old_info}\n"
            f"   • Cliente: {delivery.order.full_name}\n"
            f"   • Dirección: {delivery.order.address}, {delivery.order.city}\n"
            f"   • Repartidor asignado: {delivery.rider.username if delivery.rider else 'Sin asignar'}\n\n"
            f"⚠️ Revisa las rutas de entrega para optimizar la logística."
        )
        
        return DeliveryNotificationService.notify_coordinators(
            delivery, "coordinator_rescheduled", message
        )
    
    @staticmethod
    def notify_coordinators_status_changed(delivery, old_status, changed_by=None):
        """Notifica a coordinadores sobre un cambio de estado"""
        changed_by_str = ""
        if changed_by:
            changed_by_str = f" por {changed_by.username}"
        
        message = (
            f"🔄 CAMBIO DE ESTADO - Pedido #{delivery.order.id}\n\n"
            f"El estado de la entrega del pedido #{delivery.order.id} ha cambiado{changed_by_str}.\n\n"
            f"📊 Estado anterior: {dict(Delivery.STATUS_CHOICES).get(old_status, old_status)}\n"
            f"📊 Estado nuevo: {delivery.get_status_display()}\n\n"
            f"📌 Detalles:\n"
            f"   • Cliente: {delivery.order.full_name}\n"
            f"   • Dirección: {delivery.order.address}, {delivery.order.city}\n"
            f"   • Repartidor: {delivery.rider.username if delivery.rider else 'Sin asignar'}\n"
            f"   • Fecha programada: {delivery.scheduled_date.strftime('%d/%m/%Y') if delivery.scheduled_date else 'No especificada'}\n"
            f"   • Franja horaria: {delivery.scheduled_window if delivery.scheduled_window else 'No especificada'}\n\n"
            f"⚠️ Verifica el impacto en las rutas de entrega."
        )
        
        return DeliveryNotificationService.notify_coordinators(
            delivery, "coordinator_status_changed", message
        )
    
    @staticmethod
    def notify_coordinators_rider_assigned(delivery, old_rider=None, changed_by=None):
        """Notifica a coordinadores sobre asignación de repartidor"""
        changed_by_str = ""
        if changed_by:
            changed_by_str = f" por {changed_by.username}"
        
        old_rider_str = old_rider.username if old_rider else "Sin asignar"
        new_rider_str = delivery.rider.username if delivery.rider else "Sin asignar"
        
        message = (
            f"👤 ASIGNACIÓN DE REPARTIDOR - Pedido #{delivery.order.id}\n\n"
            f"El repartidor asignado para el pedido #{delivery.order.id} ha cambiado{changed_by_str}.\n\n"
            f"📌 Detalles:\n"
            f"   • Repartidor anterior: {old_rider_str}\n"
            f"   • Repartidor nuevo: {new_rider_str}\n\n"
            f"📦 Información de entrega:\n"
            f"   • Cliente: {delivery.order.full_name}\n"
            f"   • Dirección: {delivery.order.address}, {delivery.order.city}\n"
            f"   • Fecha programada: {delivery.scheduled_date.strftime('%d/%m/%Y') if delivery.scheduled_date else 'No especificada'}\n"
            f"   • Franja horaria: {delivery.scheduled_window if delivery.scheduled_window else 'No especificada'}\n"
            f"   • Estado: {delivery.get_status_display()}\n\n"
            f"⚠️ Actualiza las rutas de entrega según corresponda."
        )
        
        return DeliveryNotificationService.notify_coordinators(
            delivery, "coordinator_rider_assigned", message
        )
    
    @staticmethod
    def notify_coordinators_schedule_changed(delivery, old_date=None, old_window=None, changed_by=None):
        """Notifica a coordinadores sobre cambio de fecha/hora programada"""
        changed_by_str = ""
        if changed_by:
            changed_by_str = f" por {changed_by.username}"
        
        date_str = delivery.scheduled_date.strftime("%d/%m/%Y") if delivery.scheduled_date else "No especificada"
        window_str = delivery.scheduled_window if delivery.scheduled_window else "No especificada"
        
        old_info = ""
        if old_date or old_window:
            old_date_str = old_date.strftime("%d/%m/%Y") if old_date else "No especificada"
            old_window_str = old_window if old_window else "No especificada"
            old_info = f"\n   • Programación anterior: {old_date_str} {old_window_str}"
        
        message = (
            f"📅 CAMBIO DE PROGRAMACIÓN - Pedido #{delivery.order.id}\n\n"
            f"La fecha y/o franja horaria de la entrega del pedido #{delivery.order.id} ha sido modificada{changed_by_str}.\n\n"
            f"📌 Nueva programación:\n"
            f"   • Fecha: {date_str}\n"
            f"   • Franja horaria: {window_str}{old_info}\n\n"
            f"📦 Detalles de entrega:\n"
            f"   • Cliente: {delivery.order.full_name}\n"
            f"   • Dirección: {delivery.order.address}, {delivery.order.city}\n"
            f"   • Repartidor: {delivery.rider.username if delivery.rider else 'Sin asignar'}\n"
            f"   • Estado: {delivery.get_status_display()}\n\n"
            f"⚠️ Reorganiza las rutas de entrega para mantener la eficiencia logística."
        )
        
        return DeliveryNotificationService.notify_coordinators(
            delivery, "coordinator_schedule_changed", message
        )
    
    @staticmethod
    def notify_coordinators_delivery_failed(delivery, failure_reason="", changed_by=None):
        """Notifica a coordinadores sobre una entrega fallida"""
        changed_by_str = ""
        if changed_by:
            changed_by_str = f" por {changed_by.username}"
        
        reason_str = f"\n   • Motivo: {failure_reason}" if failure_reason else ""
        
        message = (
            f"❌ ENTREGA FALLIDA - Pedido #{delivery.order.id}\n\n"
            f"La entrega del pedido #{delivery.order.id} ha fallado{changed_by_str}.{reason_str}\n\n"
            f"📦 Detalles:\n"
            f"   • Cliente: {delivery.order.full_name}\n"
            f"   • Dirección: {delivery.order.address}, {delivery.order.city}\n"
            f"   • Repartidor: {delivery.rider.username if delivery.rider else 'Sin asignar'}\n"
            f"   • Fecha programada: {delivery.scheduled_date.strftime('%d/%m/%Y') if delivery.scheduled_date else 'No especificada'}\n"
            f"   • Estado: {delivery.get_status_display()}\n\n"
            f"⚠️ Acción requerida: Coordina la reprogramación o reasignación de la entrega."
        )
        
        return DeliveryNotificationService.notify_coordinators(
            delivery, "coordinator_delivery_failed", message
        )