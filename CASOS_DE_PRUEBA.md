# Casos de Prueba - Plataforma de Reprogramación Inteligente (PRI)
## Proyecto Django - E-commerce con Sistema de Entregas

---

## Funcionalidades Implementadas

He desarrollado las siguientes funcionalidades principales en mi proyecto Django:

### 🔐 **Autenticación y Gestión de Usuarios**
- Registro de usuarios
- Login/Logout
- Gestión de roles (Cliente, Repartidor, Manager)
- Control de acceso por roles

### 🛍️ **E-commerce Básico**
- Catálogo de productos con búsqueda y filtros
- Carrito de compras basado en sesión
- Checkout y simulación de pagos
- Gestión de órdenes

### 🚚 **Sistema de Entregas**
- Generación automática de entregas
- Auto-asignación de repartidores
- Gestión de estados de entrega
- Comentarios y eventos de entrega
- Subida de fotos de evidencia

### 📊 **Panel de Gestión**
- Dashboard con KPIs
- Filtros y búsquedas
- Gestión de entregas por roles

---

## Casos de Prueba Implementados

A continuación presento los casos de prueba que he diseñado para validar el funcionamiento correcto de mi sistema:

| ID | Descripción | Precondiciones | Pasos a Seguir | Resultado Esperado | Prioridad |
|---|---|---|---|---|---|
| **AUTENTICACIÓN Y USUARIOS** |
| **TC-001** | **Registrar usuario nuevo** | Sistema funcionando | 1. Ir a `/accounts/signup/`<br>2. Completar username, email, password<br>3. Hacer clic en "Registrar" | Usuario creado, login automático, redirección a catálogo | Alta |
| **TC-002** | **Login con credenciales válidas** | Usuario registrado | 1. Ir a `/accounts/login/`<br>2. Ingresar username y password<br>3. Hacer clic en "Iniciar Sesión" | Login exitoso, redirección a catálogo | Alta |
| **TC-003** | **Login con credenciales inválidas** | Sistema funcionando | 1. Ir a `/accounts/login/`<br>2. Ingresar credenciales incorrectas<br>3. Intentar login | Mensaje "Credenciales inválidas" | Alta |
| **TC-004** | **Logout de usuario** | Usuario autenticado | 1. Estar logueado<br>2. Hacer clic en "Logout" | Sesión cerrada, redirección a catálogo | Media |
| **TC-005** | **Cambiar rol de usuario (Superuser)** | Superuser autenticado | 1. Ir a `/accounts/manage-roles/`<br>2. Seleccionar usuario<br>3. Cambiar rol<br>4. Confirmar | Rol actualizado, mensaje de confirmación | Media |
| **CATÁLOGO Y PRODUCTOS** |
| **TC-006** | **Ver catálogo de productos** | Productos en BD | 1. Ir a `/shop/` | Lista de productos con imagen, nombre, precio | Alta |
| **TC-007** | **Buscar productos por nombre** | Productos en catálogo | 1. Ir a `/shop/`<br>2. Ingresar término de búsqueda<br>3. Buscar | Productos que contengan el término | Alta |
| **TC-008** | **Filtrar productos por categoría** | Productos con categorías | 1. Ir a `/shop/`<br>2. Seleccionar categoría<br>3. Aplicar filtro | Solo productos de la categoría | Media |
| **TC-009** | **Filtrar productos por precio** | Productos con precios variados | 1. Ir a `/shop/`<br>2. Ingresar rango de precio<br>3. Aplicar filtro | Solo productos en el rango | Media |
| **TC-010** | **Ver detalle de producto** | Producto existente | 1. Hacer clic en un producto | Página de detalle con información completa | Alta |
| **CARRITO DE COMPRAS** |
| **TC-011** | **Agregar producto al carrito** | Producto disponible | 1. Ir a detalle de producto<br>2. Seleccionar cantidad<br>3. Hacer clic en "Agregar al carrito" | Producto agregado, redirección a carrito | Alta |
| **TC-012** | **Ver contenido del carrito** | Productos en carrito | 1. Ir a `/cart/` | Lista de productos con cantidades y totales | Alta |
| **TC-013** | **Actualizar cantidad en carrito** | Producto en carrito | 1. Ir al carrito<br>2. Cambiar cantidad<br>3. Actualizar | Cantidad actualizada, total recalculado | Media |
| **TC-014** | **Eliminar producto del carrito** | Producto en carrito | 1. Ir al carrito<br>2. Hacer clic en "Eliminar" | Producto removido del carrito | Media |
| **PROCESO DE COMPRA** |
| **TC-015** | **Proceso de checkout** | Productos en carrito, usuario autenticado | 1. Ir al carrito<br>2. Hacer clic en "Proceder al checkout"<br>3. Completar datos de envío<br>4. Confirmar | Orden creada, redirección a simulación de pago | Alta |
| **TC-016** | **Simulación de pago exitoso** | Orden creada | 1. Estar en página de simulación<br>2. Seleccionar "Pago exitoso"<br>3. Confirmar | Orden marcada como pagada, delivery creado | Alta |
| **TC-017** | **Simulación de pago fallido** | Orden creada | 1. Estar en página de simulación<br>2. Seleccionar "Pago fallido"<br>3. Confirmar | Página de pago fallido mostrada | Media |
| **TC-018** | **Ver resumen de orden** | Orden pagada | 1. Completar pago exitoso<br>2. Ser redirigido a resumen | Detalles de la orden y estado de entrega | Alta |
| **GESTIÓN DE ÓRDENES** |
| **TC-019** | **Ver mis órdenes (Cliente)** | Usuario Cliente con órdenes | 1. Login como Cliente<br>2. Ir a `/orders/my-orders/` | Lista de órdenes del usuario | Alta |
| **TC-020** | **Ver entregas asignadas (Repartidor)** | Usuario Repartidor con entregas | 1. Login como Repartidor<br>2. Ir a `/orders/my-orders/` | Lista de entregas asignadas | Alta |
| **TC-021** | **Acceder al panel de gestión (Manager)** | Usuario Manager autenticado | 1. Login como Manager<br>2. Ir a `/orders/panel/` | Panel con KPIs y lista de órdenes | Alta |
| **TC-022** | **Filtrar órdenes por estado** | Panel de Manager accesible | 1. Ir al panel<br>2. Seleccionar estado<br>3. Aplicar filtro | Solo órdenes con el estado seleccionado | Media |
| **TC-023** | **Buscar órdenes en panel** | Panel de Manager accesible | 1. Ir al panel<br>2. Ingresar término de búsqueda<br>3. Buscar | Órdenes que coincidan con el término | Media |
| **GESTIÓN DE ENTREGAS** |
| **TC-024** | **Asignar repartidor a entrega** | Manager en detalle de entrega | 1. Ir a detalle de entrega como Manager<br>2. Seleccionar repartidor<br>3. Establecer fecha y hora<br>4. Confirmar | Repartidor asignado, estado "asignada" | Alta |
| **TC-025** | **Actualizar estado de entrega (Repartidor)** | Repartidor asignado | 1. Ir a detalle de entrega como Repartidor<br>2. Cambiar estado<br>3. Agregar notas<br>4. Confirmar | Estado actualizado, evento creado | Alta |
| **TC-026** | **Marcar entrega como entregada** | Repartidor en entrega asignada | 1. Cambiar estado a "Entregada"<br>2. Subir foto de evidencia<br>3. Confirmar | Estado "entregada", foto guardada | Alta |
| **TC-027** | **Marcar entrega como fallida** | Repartidor en entrega asignada | 1. Cambiar estado a "Fallida"<br>2. Ingresar razón de falla<br>3. Confirmar | Estado "fallida", razón guardada | Alta |
| **TC-028** | **Reprogramar entrega** | Repartidor en entrega asignada | 1. Cambiar estado a "Reprogramada"<br>2. Agregar notas<br>3. Confirmar | Estado "reprogramada", notas guardadas | Media |
| **COMENTARIOS Y EVENTOS** |
| **TC-029** | **Agregar comentario de Manager** | Manager en detalle de entrega | 1. Ir a detalle de entrega como Manager<br>2. Escribir comentario<br>3. Opcionalmente subir foto<br>4. Enviar | Comentario guardado con rol "manager" | Media |
| **TC-030** | **Agregar comentario de Repartidor** | Repartidor en detalle de entrega | 1. Ir a detalle de entrega como Repartidor<br>2. Escribir comentario<br>3. Opcionalmente subir foto<br>4. Enviar | Comentario guardado con rol "repartidor" | Media |
| **TC-031** | **Ver historial de eventos** | Entrega con eventos | 1. Ir a detalle de entrega<br>2. Revisar sección de eventos | Lista cronológica de cambios de estado | Media |
| **TC-032** | **Ver comentarios de entrega** | Entrega con comentarios | 1. Ir a detalle de entrega<br>2. Revisar sección de comentarios | Lista de comentarios con autor y fecha | Media |
| **CONTROL DE ACCESO** |
| **TC-033** | **Acceso restringido por rol (Cliente)** | Usuario Cliente autenticado | 1. Login como Cliente<br>2. Intentar acceder a entrega de otro usuario | Redirección a mis órdenes | Alta |
| **TC-034** | **Acceso restringido por rol (Repartidor)** | Usuario Repartidor autenticado | 1. Login como Repartidor<br>2. Intentar acceder a entrega no asignada | Acceso denegado o redirección | Alta |
| **TC-035** | **Acceso a catálogo con rol Manager** | Usuario Manager autenticado | 1. Login como Manager<br>2. Intentar acceder a `/shop/` | Redirección a `/orders/my-orders/` | Media |
| **TC-036** | **Acceso a catálogo con rol Repartidor** | Usuario Repartidor autenticado | 1. Login como Repartidor<br>2. Intentar acceder a `/shop/` | Redirección a `/orders/my-orders/` | Media |
| **FUNCIONALIDADES ADICIONALES** |
| **TC-037** | **Auto-asignación de repartidor** | Orden pagada, repartidores disponibles | 1. Completar pago exitoso<br>2. Verificar creación de delivery | Repartidor con menos entregas asignado | Alta |
| **TC-038** | **Cálculo correcto de totales** | Productos en carrito | 1. Agregar productos con diferentes precios<br>2. Ir al checkout | Total calculado correctamente | Alta |
| **TC-039** | **Persistencia de carrito** | Productos en carrito | 1. Agregar productos al carrito<br>2. Cerrar y reabrir navegador<br>3. Ir al carrito | Productos mantienen cantidad | Media |
| **TC-040** | **Vaciamiento de carrito tras pago** | Carrito con productos, pago exitoso | 1. Completar pago exitoso<br>2. Verificar estado del carrito | Carrito vacío después del pago | Media |
| **TC-041** | **Subida de foto de evidencia** | Repartidor marcando entrega | 1. Cambiar estado a "Entregada"<br>2. Subir foto<br>3. Confirmar | Foto guardada en `/media/deliveries/` | Media |
| **TC-042** | **Subida de imagen en comentarios** | Entrega con funcionalidad de comentarios | 1. Agregar comentario con imagen<br>2. Subir archivo<br>3. Enviar | Imagen guardada en `/media/deliveries/comments/` | Media |

---

## Resumen de Casos de Prueba

He diseñado un total de **42 casos de prueba** que cubren todas las funcionalidades implementadas:

| Módulo | Casos de Prueba | Estado |
|--------|----------------|--------|
| **Autenticación** | TC-001 a TC-005 | Implementado |
| **Catálogo** | TC-006 a TC-010 | Implementado |
| **Carrito** | TC-011 a TC-014 | Implementado |
| **Compras** | TC-015 a TC-018 | Implementado |
| **Órdenes** | TC-019 a TC-023 | Implementado |
| **Entregas** | TC-024 a TC-028 | Implementado |
| **Comentarios** | TC-029 a TC-032 | Implementado |
| **Acceso** | TC-033 a TC-036 | Implementado |
| **Adicionales** | TC-037 a TC-042 | Implementado |

---

## Funcionalidades Pendientes

Para futuras versiones del proyecto, tengo planificado implementar:

- **Notificaciones SMS/WhatsApp** para informar sobre entregas
- **Notificaciones push** en tiempo real
- **Dashboard con gráficos avanzados** y métricas detalladas
- **Filtros geográficos** para reportes
- **Descarga de reportes** en Excel/PDF
- **Métricas de satisfacción** (NPS)

---

## Configuración para Ejecutar las Pruebas

Para poder ejecutar estos casos de prueba, necesitas configurar el entorno de la siguiente manera:

```bash
# 1. Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Migrar base de datos
python manage.py migrate

# 4. Crear datos de prueba
python manage.py seed_store

# 5. Crear superusuario
python manage.py createsuperuser
```

### Usuarios de Prueba
```python
# Crear usuarios con diferentes roles para las pruebas
python manage.py shell
>>> from django.contrib.auth.models import User
>>> from accounts.models import UserProfile

# Cliente
cliente = User.objects.create_user('cliente_test', 'cliente@test.com', 'pass123')
UserProfile.objects.create(user=cliente, role='cliente')

# Repartidor
repartidor = User.objects.create_user('repartidor_test', 'repartidor@test.com', 'pass123')
UserProfile.objects.create(user=repartidor, role='repartidor')

# Manager
manager = User.objects.create_user('manager_test', 'manager@test.com', 'pass123')
UserProfile.objects.create(user=manager, role='manager')
```

---

## Prioridades de Ejecución

He clasificado los casos de prueba por prioridad para facilitar la ejecución:

### Alta Prioridad (Crítico)
- TC-001, TC-002, TC-006, TC-011, TC-015, TC-016, TC-019, TC-024, TC-025, TC-026, TC-033, TC-037

### Media Prioridad (Importante)
- TC-003, TC-004, TC-007, TC-008, TC-012, TC-017, TC-020, TC-021, TC-027, TC-029, TC-034, TC-038

### Baja Prioridad (Complementario)
- TC-005, TC-009, TC-010, TC-013, TC-014, TC-018, TC-022, TC-023, TC-028, TC-030, TC-031, TC-032, TC-035, TC-036, TC-039, TC-040, TC-041, TC-042

---

## Checklist de Ejecución

### Preparación
- [ ] Entorno virtual activado
- [ ] Dependencias instaladas
- [ ] Base de datos migrada
- [ ] Datos de prueba creados
- [ ] Usuarios de prueba creados

### Ejecución
- [ ] Ejecutar casos de alta prioridad
- [ ] Documentar resultados (Pasó/Falló)
- [ ] Capturar evidencias (screenshots)
- [ ] Reportar bugs encontrados

### Validación
- [ ] Verificar que casos críticos pasan
- [ ] Confirmar funcionalidades básicas
- [ ] Validar control de acceso
- [ ] Comprobar gestión de entregas

---

## Notas Importantes

1. **Cobertura completa**: Estos casos cubren todas las funcionalidades implementadas en mi proyecto
2. **Basado en mi código**: Toda la funcionalidad documentada en mi README.md está cubierta
3. **Roles implementados**: Cliente, Repartidor, Manager/Superuser
4. **Estados de entrega**: Pendiente → Asignada → En ruta → Entregada/Fallida/Reprogramada
5. **Archivos de prueba**: Imágenes en `/media/products/` y `/media/deliveries/`

**Total: 42 casos de prueba diseñados para validar el funcionamiento correcto del sistema** ✅
