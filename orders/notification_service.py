from django.contrib.auth import get_user_model
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
