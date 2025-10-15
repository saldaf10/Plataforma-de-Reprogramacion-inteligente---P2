#!/usr/bin/env python3
"""
Script para crear usuarios de prueba para las pruebas automatizadas
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile

def create_test_users():
    """Crear usuarios de prueba para las pruebas automatizadas"""
    
    # Datos de usuarios de prueba
    test_users = [
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
    
    for user_data in test_users:
        username = user_data['username']
        
        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            print(f"✅ Usuario {username} ya existe")
            user = User.objects.get(username=username)
        else:
            # Crear nuevo usuario
            user = User.objects.create_user(
                username=username,
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            print(f"✅ Usuario {username} creado exitosamente")
        
        # Crear o actualizar perfil de usuario
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={'role': user_data['role']}
        )
        
        if not created:
            profile.role = user_data['role']
            profile.save()
        
        created_users.append(user)
    
    print(f"\n🎉 {len(created_users)} usuarios de prueba configurados correctamente")
    return created_users

if __name__ == "__main__":
    try:
        users = create_test_users()
        print("\n📋 Usuarios disponibles para testing:")
        for user in users:
            try:
                role = user.userprofile.role
            except:
                role = "Sin rol asignado"
            print(f"  - {user.username} ({user.email}) - Rol: {role}")
        
        print("\n🚀 Listo para ejecutar las pruebas automatizadas!")
        
    except Exception as e:
        print(f"❌ Error creando usuarios de prueba: {e}")
        sys.exit(1)
