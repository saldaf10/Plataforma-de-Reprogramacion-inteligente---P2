from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Delivery
from .notification_service import DeliveryNotificationService


@receiver(pre_save, sender=Delivery)
def delivery_pre_save(sender, instance, **kwargs):
    """Captura el estado anterior antes de guardar"""
    if instance.pk:
        try:
            old_instance = Delivery.objects.get(pk=instance.pk)
            instance._old_status = old_instance.status
            instance._old_rider = old_instance.rider
            instance._old_scheduled_date = old_instance.scheduled_date
            instance._old_scheduled_window = old_instance.scheduled_window
        except Delivery.DoesNotExist:
            instance._old_status = None
            instance._old_rider = None
            instance._old_scheduled_date = None
            instance._old_scheduled_window = None
    else:
        instance._old_status = None
        instance._old_rider = None
        instance._old_scheduled_date = None
        instance._old_scheduled_window = None


@receiver(post_save, sender=Delivery)
def delivery_post_save(sender, instance, created, **kwargs):
    """
    Notifica a coordinadores sobre cambios importantes en entregas.
    Solo notifica si el cambio no fue iniciado desde las vistas (que ya notifican).
    Las vistas marcan _notification_sent para evitar duplicados.
    """
    
    # Si es una nueva entrega, no notificar (aún no hay cambios)
    if created:
        return
    
    # Si la notificación ya fue enviada desde la vista, no volver a notificar
    if getattr(instance, '_notification_sent', False):
        return
    
    # Verificar si hay cambios importantes
    old_status = getattr(instance, '_old_status', None)
    old_rider = getattr(instance, '_old_rider', None)
    old_date = getattr(instance, '_old_scheduled_date', None)
    old_window = getattr(instance, '_old_scheduled_window', None)
    
    # Detectar cambios de estado (solo si realmente cambió)
    if old_status and old_status != instance.status:
        # Solo notificar si es un cambio automático o desde otro origen
        DeliveryNotificationService.notify_coordinators_status_changed(
            instance, old_status=old_status, changed_by=None
        )
    
    # Detectar cambios de repartidor
    if old_rider != instance.rider:
        DeliveryNotificationService.notify_coordinators_rider_assigned(
            instance, old_rider=old_rider, changed_by=None
        )
    
    # Detectar cambios de fecha/hora programada
    if old_date != instance.scheduled_date or old_window != instance.scheduled_window:
        DeliveryNotificationService.notify_coordinators_schedule_changed(
            instance, old_date=old_date, old_window=old_window, changed_by=None
        )

