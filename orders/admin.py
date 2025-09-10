from django.contrib import admin
from .models import Order, OrderItem, Delivery


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ("id", "user", "paid", "total_amount", "created_at")
    list_filter = ("paid", "created_at")


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "status", "rider", "scheduled_date", "scheduled_window")
    list_filter = ("status", "scheduled_date")
from django.contrib import admin

# Register your models here.
