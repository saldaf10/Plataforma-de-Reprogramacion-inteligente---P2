from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("summary/<int:order_id>/", views.order_summary, name="summary"),
    path("my-orders/", views.my_orders, name="my_orders"),
    path("delivery/<int:order_id>/", views.delivery_detail, name="delivery_detail"),
    path("panel/", views.manager_panel, name="panel"),
]

