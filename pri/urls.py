from django.urls import path
from . import views

app_name = "pri"

urlpatterns = [
    path("", views.pri_home, name="home"),
    path("mock/index/", views.mock_index, name="mock_index"),
    path("mock/cliente/", views.mock_cliente, name="mock_cliente"),
    path("mock/repartidor/", views.mock_repartidor, name="mock_repartidor"),
    path("mock/dashboard/", views.mock_dashboard, name="mock_dashboard"),
    path("mock/confirmacion/", views.mock_confirmacion, name="mock_confirmacion"),
]

