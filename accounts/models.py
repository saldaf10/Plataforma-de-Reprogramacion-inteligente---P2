from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ("manager", "Manager"),
        ("cliente", "Cliente"),
        ("repartidor", "Repartidor"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="cliente")

    def __str__(self) -> str:
        return f"{self.user.username} ({self.role})"
from django.db import models

# Create your models here.
