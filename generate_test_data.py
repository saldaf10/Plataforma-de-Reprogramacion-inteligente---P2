#!/usr/bin/env python3
"""
Script para generar datos de prueba completos para el framework de testing
"""
import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile
from catalog.models import Category, Product
from orders.models import Order, OrderItem, Delivery, DeliveryEvent, DeliveryComment, DeliveryNotification
# Cart es basado en sesión, no requiere modelos

def create_test_users():
    """Crear usuarios de prueba con roles específicos"""
    print("👥 Creando usuarios de prueba...")
    
    users_data = [
        {
            'username': 'cliente_test',
            'email': 'cliente@test.com',
            'password': 'password123',
            'first_name': 'Cliente',
            'last_name': 'Prueba',
            'role': 'cliente'
        },
        {
            'username': 'repartidor_test',
            'email': 'repartidor@test.com',
            'password': 'password123',
            'first_name': 'Repartidor',
            'last_name': 'Prueba',
            'role': 'repartidor'
        },
        {
            'username': 'manager_test',
            'email': 'manager@test.com',
            'password': 'password123',
            'first_name': 'Manager',
            'last_name': 'Prueba',
            'role': 'manager'
        }
    ]
    
    created_users = []
    
    for user_data in users_data:
        username = user_data['username']
        
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            print(f"  ✅ Usuario {username} ya existe")
        else:
            user = User.objects.create_user(
                username=username,
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            print(f"  ✅ Usuario {username} creado")
        
        # Crear o actualizar perfil
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={'role': user_data['role']}
        )
        if not created:
            profile.role = user_data['role']
            profile.save()
        
        created_users.append(user)
    
    return created_users

def create_test_categories():
    """Crear categorías de productos de prueba"""
    print("📦 Creando categorías de productos...")
    
    categories_data = [
        {'name': 'Calzado'},
        {'name': 'Cuidado Personal'},
        {'name': 'Suplementos'}
    ]
    
    created_categories = []
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name']
        )
        if created:
            print(f"  ✅ Categoría {cat_data['name']} creada")
        else:
            print(f"  ✅ Categoría {cat_data['name']} ya existe")
        created_categories.append(category)
    
    return created_categories

def create_test_products():
    """Crear productos de prueba"""
    print("🛍️ Creando productos de prueba...")
    
    categories = Category.objects.all()
    
    products_data = [
        {
            'name': 'Zapatos Deportivos Pro',
            'description': 'Zapatos deportivos de alta calidad para running',
            'price': Decimal('89.99'),
            'category': categories.filter(name='Calzado').first(),
            'stock': 10
        },
        {
            'name': 'Loción Corporal Fresh',
            'description': 'Loción hidratante con fragancia fresca',
            'price': Decimal('24.99'),
            'category': categories.filter(name='Cuidado Personal').first(),
            'stock': 25
        },
        {
            'name': 'Proteína Whey 1kg',
            'description': 'Proteína en polvo para deportistas',
            'price': Decimal('45.99'),
            'category': categories.filter(name='Suplementos').first(),
            'stock': 15
        }
    ]
    
    created_products = []
    
    for prod_data in products_data:
        product, created = Product.objects.get_or_create(
            name=prod_data['name'],
            defaults={
                'description': prod_data['description'],
                'price': prod_data['price'],
                'category': prod_data['category'],
                'stock': prod_data['stock']
            }
        )
        if created:
            print(f"  ✅ Producto {prod_data['name']} creado")
        else:
            print(f"  ✅ Producto {prod_data['name']} ya existe")
        created_products.append(product)
    
    return created_products

def create_test_orders():
    """Crear órdenes de prueba con diferentes estados"""
    print("📋 Creando órdenes de prueba...")
    
    cliente = User.objects.get(username='cliente_test')
    repartidor = User.objects.get(username='repartidor_test')
    products = Product.objects.all()
    
    orders_data = [
        {
            'user': cliente,
            'paid': True,
            'total': Decimal('114.98'),
            'delivery_status': 'entregada',
            'delivery_date': datetime.now() - timedelta(days=2),
            'address': 'Calle Principal 123, Bogotá',
            'notes': 'Entregar en horario de oficina',
            'full_name': 'Cliente Prueba',
            'email': 'cliente@test.com',
            'city': 'Bogotá',
            'postal_code': '110111'
        },
        {
            'user': cliente,
            'paid': True,
            'total': Decimal('89.99'),
            'delivery_status': 'en_ruta',
            'delivery_date': datetime.now() + timedelta(hours=2),
            'address': 'Carrera 45 #67-89, Medellín',
            'notes': 'Casa con portón verde',
            'full_name': 'Cliente Prueba',
            'email': 'cliente@test.com',
            'city': 'Medellín',
            'postal_code': '050001'
        },
        {
            'user': cliente,
            'paid': True,
            'total': Decimal('70.98'),
            'delivery_status': 'fallida',
            'delivery_date': datetime.now() - timedelta(hours=1),
            'address': 'Calle 100 #15-30, Cali',
            'notes': 'Dirección incorrecta',
            'full_name': 'Cliente Prueba',
            'email': 'cliente@test.com',
            'city': 'Cali',
            'postal_code': '760001'
        },
        {
            'user': cliente,
            'paid': False,
            'total': Decimal('135.97'),
            'delivery_status': 'asignada',
            'delivery_date': datetime.now() + timedelta(days=1),
            'address': 'Avenida 68 #25-40, Barranquilla',
            'notes': 'Reprogramada para mañana',
            'full_name': 'Cliente Prueba',
            'email': 'cliente@test.com',
            'city': 'Barranquilla',
            'postal_code': '080001'
        }
    ]
    
    created_orders = []
    
    for i, order_data in enumerate(orders_data):
        # Crear órdenes únicas basadas en la dirección
        order, created = Order.objects.get_or_create(
            user=order_data['user'],
            address=order_data['address'],
            defaults={
                'paid': order_data['paid'],
                'total_amount': order_data['total'],
                'full_name': order_data['full_name'],
                'email': order_data['email'],
                'city': order_data['city'],
                'postal_code': order_data['postal_code']
            }
        )
        
        if created:
            print(f"  ✅ Orden {order.id} creada ({'Pagada' if order_data['paid'] else 'Pendiente'})")
            
            # Crear items de la orden
            for i, product in enumerate(products[:2]):  # Agregar 2 productos
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=i + 1,
                    price=product.price
                )
            
            # Crear entrega - ASIGNAR TODAS AL REPARTIDOR para testing
            delivery = Delivery.objects.create(
                order=order,
                rider=repartidor,  # Asignar todas las entregas al repartidor para testing
                status=order_data['delivery_status'],
                notes=order_data['notes'],
                scheduled_date=order_data['delivery_date'].date() if hasattr(order_data['delivery_date'], 'date') else order_data['delivery_date']
            )
            
            # Crear eventos de entrega según el estado
            if order_data['delivery_status'] == 'entregada':
                DeliveryEvent.objects.create(
                    delivery=delivery,
                    status_before='en_ruta',
                    status_after='entregada',
                    notes='Entrega completada exitosamente',
                    user=repartidor
                )
            elif order_data['delivery_status'] == 'fallida':
                DeliveryEvent.objects.create(
                    delivery=delivery,
                    status_before='en_ruta',
                    status_after='fallida',
                    notes='Dirección no encontrada',
                    user=repartidor
                )
                # Crear comentario de fallo
                DeliveryComment.objects.create(
                    delivery=delivery,
                    message='Cliente no se encuentra en la dirección proporcionada',
                    role='repartidor',
                    user=repartidor
                )
                # Crear notificación de fallo
                DeliveryNotification.objects.create(
                    delivery=delivery,
                    notification_type='failed',
                    message='Tu entrega ha fallado. Razón: Dirección no encontrada',
                    recipient=cliente
                )
            elif order_data['delivery_status'] == 'en_ruta':
                DeliveryEvent.objects.create(
                    delivery=delivery,
                    status_before='asignada',
                    status_after='en_ruta',
                    notes='Repartidor en camino',
                    user=repartidor
                )
            
            created_orders.append(order)
        else:
            print(f"  ✅ Orden {order.id} ya existe")
            created_orders.append(order)
    
    return created_orders

def create_test_notifications():
    """Crear notificaciones de prueba"""
    print("🔔 Creando notificaciones de prueba...")
    
    cliente = User.objects.get(username='cliente_test')
    repartidor = User.objects.get(username='repartidor_test')
    deliveries = Delivery.objects.all()
    
    notifications_data = [
        {
            'delivery': deliveries.filter(status='fallida').first(),
            'notification_type': 'failed',
            'message': 'Tu entrega ha fallado. Razón: Dirección incorrecta',
            'recipient': cliente,
            'read': False
        },
        {
            'delivery': deliveries.filter(status='fallida').first(),
            'notification_type': 'failed',
            'message': 'Entrega fallida: Cliente no se encuentra en la dirección',
            'recipient': cliente,
            'read': False
        },
        {
            'delivery': deliveries.filter(status='en_ruta').first(),
            'notification_type': 'approaching',
            'message': 'Tu pedido está en camino. Tiempo estimado: 30 minutos',
            'recipient': cliente,
            'read': True
        },
        {
            'delivery': deliveries.filter(status='asignada').first(),
            'notification_type': 'rescheduled',
            'message': 'Tu entrega ha sido reprogramada para mañana',
            'recipient': repartidor,
            'read': False
        }
    ]
    
    created_notifications = []
    
    for notif_data in notifications_data:
        if notif_data['delivery']:  # Solo crear si existe la entrega
            notification, created = DeliveryNotification.objects.get_or_create(
                delivery=notif_data['delivery'],
                notification_type=notif_data['notification_type'],
                defaults={
                    'message': notif_data['message'],
                    'recipient': notif_data['recipient'],
                    'read': notif_data['read']
                }
            )
            if created:
                print(f"  ✅ Notificación {notif_data['notification_type']} creada")
            else:
                print(f"  ✅ Notificación {notif_data['notification_type']} ya existe")
            created_notifications.append(notification)
    
    return created_notifications

def create_test_rescheduled_delivery():
    """Crear entrega reprogramada para pruebas"""
    print("🔄 Creando entrega reprogramada...")
    
    cliente = User.objects.get(username='cliente_test')
    repartidor = User.objects.get(username='repartidor_test')
    
    # Crear orden reprogramada
    order, created = Order.objects.get_or_create(
        user=cliente,
        address='Calle 80 #12-34, Bogotá',
        defaults={
            'paid': True,
            'total_amount': Decimal('89.99'),
            'full_name': 'Cliente Prueba',
            'email': 'cliente@test.com',
            'city': 'Bogotá',
            'postal_code': '110111'
        }
    )
    
    if created:
        # Crear entrega con estado reprogramada
        delivery = Delivery.objects.create(
            order=order,
            rider=repartidor,
            status='reprogramada',
            notes='Entrega reprogramada por solicitud del cliente',
            scheduled_date=(datetime.now() + timedelta(days=1)).date()
        )
        
        # Crear evento de reprogramación
        DeliveryEvent.objects.create(
            delivery=delivery,
            status_before='asignada',
            status_after='reprogramada',
            notes='Entrega reprogramada por solicitud del cliente',
            user=cliente
        )
        
        # Crear notificación para el repartidor
        DeliveryNotification.objects.create(
            delivery=delivery,
            notification_type='rescheduled',
            message='Una entrega ha sido reprogramada. Nueva fecha: mañana',
            recipient=repartidor,
            read=False
        )
        
        print(f"  ✅ Entrega reprogramada {delivery.id} creada")
        return delivery
    else:
        print(f"  ✅ Orden reprogramada ya existe")
        return order.delivery

def main():
    """Función principal para generar todos los datos de prueba"""
    print("🚀 Generando datos de prueba completos para el framework de testing")
    print("=" * 70)
    
    try:
        # 1. Crear usuarios
        users = create_test_users()
        
        # 2. Crear categorías
        categories = create_test_categories()
        
        # 3. Crear productos
        products = create_test_products()
        
        # 4. Crear órdenes con diferentes estados
        orders = create_test_orders()
        
        # 5. Crear notificaciones
        notifications = create_test_notifications()
        
        # 6. Crear entrega reprogramada
        rescheduled_delivery = create_test_rescheduled_delivery()
        
        print("\n🎉 Datos de prueba generados exitosamente!")
        print("\n📊 Resumen de datos creados:")
        print(f"  👥 Usuarios: {len(users)}")
        print(f"  📦 Categorías: {len(categories)}")
        print(f"  🛍️ Productos: {len(products)}")
        print(f"  📋 Órdenes: {len(orders)}")
        print(f"  🔔 Notificaciones: {len(notifications)}")
        print(f"  🔄 Entregas reprogramadas: 1")
        
        print("\n✅ Datos disponibles para testing:")
        print("  - Entregas entregadas ✅")
        print("  - Entregas en ruta ✅")
        print("  - Entregas fallidas ✅")
        print("  - Entregas reprogramadas ✅")
        print("  - Notificaciones activas ✅")
        print("  - Usuarios con roles específicos ✅")
        
        print("\n🚀 ¡Listo para ejecutar las pruebas automatizadas!")
        
    except Exception as e:
        print(f"❌ Error generando datos de prueba: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
