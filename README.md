# PRI Shop + Reprogramación Inteligente (Django)

Proyecto Django que implementa un ecommerce básico (zapatos, lociones, proteínas) y un módulo operativo de reprogramación de entregas con roles: cliente, repartidor y manager/superuser.

## Características

- Catálogo con búsqueda y filtros (categoría, precio) en `/shop/`.
- Carrito por sesión y checkout con simulación de pago.
- Órdenes con generación automática de entrega (Delivery).
- Auto-asignación al repartidor con menos entregas activas.
- Roles y navegación por permisos:
  - Cliente: Mis pedidos y detalle con barra de progreso.
  - Repartidor: Historial de pedidos asignados; detalle con estado, comentarios y foto.
  - Manager/Superuser: Panel con KPIs y lista; detalle con asignación de repartidor/ventana horaria, historial y comentarios.
- Historial de eventos de entrega (cambios de estado) con usuario, notas y foto.
- Comentarios con foto asociados a la entrega (manager/repartidor/cliente).
- Imágenes dummy para productos generadas por seed.

## Estructura de apps

- `catalog`: categorías y productos.
- `cart`: carrito basado en sesión.
- `orders`: órdenes, items, entregas y vistas por rol.
- `payments`: simulación de pago y post-proceso.
- `accounts`: autenticación, perfiles y gestión de roles (superuser).

## Requisitos

- Python 3.12+
- pip, venv

## Instalación y ejecución

1. Clonar repo y entrar a `server/`:
   ```bash
   cd "./server"
   ```
2. Crear y activar entorno virtual:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Migrar base de datos y seed de datos:
   ```bash
   python manage.py migrate
   python manage.py seed_store
   ```
5. Crear superusuario:
   ```bash
   python manage.py createsuperuser
   ```
6. Ejecutar servidor:
   ```bash
   python manage.py runserver
   ```

## Uso por rol

- Anónimo/Cliente:
  - Navega `/shop/`, agrega al carrito y compra.
  - En `Pedidos` ve estado y un bloque “Próximo pedido” con barra de progreso.
- Repartidor:
  - Menú “Historial de pedidos” muestra asignados con dirección, hora estimada (creación +24h) y estado.
  - En detalle puede actualizar estado, subir comentario y foto (evidencia).
- Manager/Superuser:
  - Menú “Panel” (`/orders/panel/`): KPIs y lista con filtros.
  - En detalle gestiona asignación, ventana horaria, ve historial de eventos y comentarios, y puede añadir comentarios con foto.
  - “Gestionar roles” para cambiar rol de usuarios.

## Variables y rutas relevantes

- Media estática: `MEDIA_ROOT=media/`. Asegúrate de que exista.
- Rutas principales:
  - `/` → Redirección según rol.
  - `/shop/` → Catálogo.
  - `/cart/` → Carrito.
  - `/orders/checkout/` → Checkout.
  - `/orders/my-orders/` → Vista pedidos (contexto según rol).
  - `/orders/delivery/<id>/` → Detalle de entrega.
  - `/orders/panel/` → Panel manager/superuser.
  - `/accounts/manage-roles/` → Gestionar roles (solo superuser).

## Notas

- Este proyecto usa SQLite por defecto.
- Subida de fotos se guarda en `media/deliveries/` y subcarpetas.
- Los badges de estado se colorean: asignada (gris), en_ruta (azul), entregada (verde), fallida (rojo).
