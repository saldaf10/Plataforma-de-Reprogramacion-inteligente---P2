"""
Configuración para diferentes entornos de testing
"""
import os

class TestConfig:
    """Configuración base para las pruebas"""
    
    # URLs de diferentes entornos
    BASE_URL = os.getenv('TEST_BASE_URL', 'http://localhost:8000')
    
    # Credenciales de usuarios de prueba
    TEST_USERS = {
        'cliente': {
            'username': 'cliente_test',
            'password': 'password123',
            'email': 'cliente@test.com'
        },
        'repartidor': {
            'username': 'repartidor_test', 
            'password': 'password123',
            'email': 'repartidor@test.com'
        },
        'manager': {
            'username': 'manager_test',
            'password': 'password123', 
            'email': 'manager@test.com'
        }
    }
    
    # Configuración de timeouts
    TIMEOUTS = {
        'short': 5000,
        'medium': 10000,
        'long': 30000
    }
    
    # Configuración del navegador
    BROWSER_CONFIG = {
        'headless': os.getenv('HEADLESS', 'false').lower() == 'true',
        'slow_mo': int(os.getenv('SLOW_MO', '1000')),
        'viewport': {
            'width': int(os.getenv('VIEWPORT_WIDTH', '1920')),
            'height': int(os.getenv('VIEWPORT_HEIGHT', '1080'))
        }
    }
    
    # Rutas de la aplicación
    URLS = {
        'login': '/accounts/login/',
        'signup': '/accounts/signup/',
        'profile': '/accounts/profile/',
        'shop': '/shop/',
        'cart': '/cart/',
        'checkout': '/orders/checkout/',
        'my_orders': '/orders/my-orders/',
        'rider_orders': '/orders/rider-orders/',
        'manager_panel': '/orders/panel/',
        'notifications': '/orders/notifications/',
        'delivery_detail': '/orders/delivery/'
    }
    
    # Datos de prueba
    TEST_DATA = {
        'products': [
            {
                'name': 'Zapatos Deportivos',
                'category': 'Calzado',
                'price': 89.99
            },
            {
                'name': 'Loción Corporal',
                'category': 'Cuidado Personal', 
                'price': 24.99
            },
            {
                'name': 'Proteína Whey',
                'category': 'Suplementos',
                'price': 45.99
            }
        ],
        'delivery_address': {
            'street': 'Calle Principal 123',
            'city': 'Bogotá',
            'postal_code': '110111',
            'notes': 'Casa blanca con portón verde'
        },
        'time_slots': [
            '08:00-12:00',
            '12:00-16:00', 
            '16:00-20:00'
        ]
    }
