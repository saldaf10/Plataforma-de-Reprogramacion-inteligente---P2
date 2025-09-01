from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("simulate/", views.simulate_payment, name="simulate"),
    path("success/", views.payment_success, name="success"),
    path("failed/", views.payment_failed, name="failed"),
]

