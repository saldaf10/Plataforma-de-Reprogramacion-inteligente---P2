from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance: User, created: bool, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, role="cliente")


@receiver(post_save, sender=User)
def save_user_profile(sender, instance: User, **kwargs):
    # Ensure profile exists
    UserProfile.objects.get_or_create(user=instance, defaults={"role": "cliente"})

