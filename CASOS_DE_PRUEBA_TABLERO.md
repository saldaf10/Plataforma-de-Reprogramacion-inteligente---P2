# Casos de Prueba - Plataforma de Reprogramación Inteligente (PRI)
## Documento de Pruebas - Equipo de Desarrollo

**Proyecto:** Plataforma de Reprogramación Inteligente (PRI)  
**Versión:** 1.0  
**Equipo:** Grupo de Desarrollo P2  

---

## Resumen Ejecutivo

Este documento presenta los casos de prueba diseñados por nuestro equipo para validar las funcionalidades implementadas en la Plataforma de Reprogramación Inteligente. Los casos están basados en las historias de usuario completadas en nuestro tablero de proyecto.

## Funcionalidades Implementadas

Nuestro equipo ha completado las siguientes funcionalidades principales:

### 🔐 **Autenticación y Roles**
- Login según rol (cliente, repartidor, coordinador)
- Control de acceso por funcionalidades

### 🛍️ **Catálogo y Búsqueda**
- Visualización de productos en la web
- Sistema de búsqueda y filtrado de productos

### 🚚 **Sistema de Entregas**
- Reprogramación de entregas por cliente
- Validación de fechas dentro del SLA
- Selección de fecha y rango de horas
- Gestión de evidencias de fallos
- Comentarios sobre motivos de fallo
- Alertas de entregas reprogramadas para coordinadores

---

## Metodología de Pruebas

Nuestro equipo ha adoptado una metodología de pruebas basada en casos de prueba estructurados que cubren:

- **Casos positivos**: Flujos exitosos de usuario
- **Casos negativos**: Validaciones y manejo de errores
- **Casos de integración**: Interacción entre módulos
- **Casos de seguridad**: Control de acceso por roles

## Casos de Prueba por Funcionalidad

### **TC-AUTH-001: Login según Rol**
| Campo | Valor |
|-------|-------|
| **ID** | TC-AUTH-001 |
| **Título** | Login exitoso según rol de usuario |
| **Descripción** | Verificar que el usuario puede iniciar sesión y acceder solo a sus funcionalidades según su rol |
| **Precondiciones** | Usuario registrado con rol específico |
| **Pasos** | 1. Ir a página de login<br>2. Ingresar credenciales válidas<br>3. Hacer clic en "Iniciar Sesión" |
| **Resultado Esperado** | Usuario logueado y redirigido según su rol (cliente/repartidor/coordinador) |
| **Prioridad** | Alta |

### **TC-AUTH-002: Control de Acceso por Rol**
| Campo | Valor |
|-------|-------|
| **ID** | TC-AUTH-002 |
| **Título** | Verificar acceso restringido por rol |
| **Descripción** | Confirmar que cada rol solo accede a sus funcionalidades específicas |
| **Precondiciones** | Usuario logueado con rol específico |
| **Pasos** | 1. Intentar acceder a funcionalidades de otros roles<br>2. Verificar redirección o bloqueo |
| **Resultado Esperado** | Acceso denegado o redirección a página autorizada |
| **Prioridad** | Alta |

### **TC-CAT-001: Visualización de Productos**
| Campo | Valor |
|-------|-------|
| **ID** | TC-CAT-001 |
| **Título** | Visualizar catálogo de productos |
| **Descripción** | Verificar que el comprador puede ver todos los productos disponibles en la web |
| **Precondiciones** | Productos registrados en el sistema |
| **Pasos** | 1. Ir a página de catálogo<br>2. Verificar lista de productos<br>3. Verificar información de cada producto |
| **Resultado Esperado** | Lista completa de productos con información detallada |
| **Prioridad** | Alta |

### **TC-CAT-002: Búsqueda de Productos**
| Campo | Valor |
|-------|-------|
| **ID** | TC-CAT-002 |
| **Título** | Buscar productos con sistema de filtrado |
| **Descripción** | Verificar que el comprador puede buscar productos usando el sistema de búsqueda y filtros |
| **Precondiciones** | Productos registrados en el sistema |
| **Pasos** | 1. Ir a página de catálogo<br>2. Usar campo de búsqueda<br>3. Aplicar filtros disponibles<br>4. Verificar resultados |
| **Resultado Esperado** | Productos filtrados según criterios de búsqueda |
| **Prioridad** | Alta |

### **TC-DEL-001: Reprogramación de Entrega**
| Campo | Valor |
|-------|-------|
| **ID** | TC-DEL-001 |
| **Título** | Reprogramar entrega desde web/app |
| **Descripción** | Verificar que el cliente puede reprogramar su entrega definiendo cuándo quiere recibir el paquete |
| **Precondiciones** | Cliente con pedido pendiente de entrega |
| **Pasos** | 1. Acceder a "Mis Pedidos"<br>2. Seleccionar pedido pendiente<br>3. Hacer clic en "Reprogramar"<br>4. Seleccionar nueva fecha y hora |
| **Resultado Esperado** | Entrega reprogramada exitosamente |
| **Prioridad** | Alta |

### **TC-DEL-002: Validación de SLA**
| Campo | Valor |
|-------|-------|
| **ID** | TC-DEL-002 |
| **Título** | Validar fecha dentro del SLA permitido |
| **Descripción** | Verificar que el sistema valida que la nueva fecha seleccionada esté dentro del SLA permitido |
| **Precondiciones** | Cliente intentando reprogramar entrega |
| **Pasos** | 1. Intentar reprogramar con fecha fuera del SLA<br>2. Verificar mensaje de error<br>3. Intentar con fecha válida |
| **Resultado Esperado** | Error para fechas fuera del SLA, éxito para fechas válidas |
| **Prioridad** | Alta |

### **TC-DEL-003: Selección de Fecha y Hora**
| Campo | Valor |
|-------|-------|
| **ID** | TC-DEL-003 |
| **Título** | Seleccionar fecha y rango de horas |
| **Descripción** | Verificar que el cliente puede seleccionar fecha y rango de horas para la nueva entrega |
| **Precondiciones** | Cliente reprogramando entrega |
| **Pasos** | 1. Acceder a reprogramación<br>2. Seleccionar fecha del calendario<br>3. Seleccionar rango de horas<br>4. Confirmar selección |
| **Resultado Esperado** | Fecha y hora seleccionadas correctamente |
| **Prioridad** | Media |

### **TC-DEL-004: Consulta de Evidencia de Fallo**
| Campo | Valor |
|-------|-------|
| **ID** | TC-DEL-004 |
| **Título** | Consultar evidencia del fallo |
| **Descripción** | Verificar que el cliente puede consultar la evidencia del fallo para saber por qué no recibió su pedido |
| **Precondiciones** | Entrega fallida con evidencia registrada |
| **Pasos** | 1. Acceder a pedido fallido<br>2. Ver sección de evidencia<br>3. Revisar fotos y comentarios |
| **Resultado Esperado** | Evidencia visible con fotos y comentarios del repartidor |
| **Prioridad** | Media |

### **TC-DEL-005: Visualización de Evidencias para Coordinador**
| Campo | Valor |
|-------|-------|
| **ID** | TC-DEL-005 |
| **Título** | Ver evidencias de intentos fallidos |
| **Descripción** | Verificar que el coordinador puede ver las evidencias asociadas a cada intento fallido |
| **Precondiciones** | Coordinador logueado, entregas fallidas con evidencia |
| **Pasos** | 1. Acceder al panel de coordinador<br>2. Filtrar entregas fallidas<br>3. Revisar evidencias de cada intento |
| **Resultado Esperado** | Lista de entregas fallidas con evidencias detalladas |
| **Prioridad** | Media |

### **TC-DEL-006: Comentarios de Fallo por Repartidor**
| Campo | Valor |
|-------|-------|
| **ID** | TC-DEL-006 |
| **Título** | Añadir comentario sobre motivo del fallo |
| **Descripción** | Verificar que el repartidor puede añadir comentarios sobre el motivo del fallo |
| **Precondiciones** | Repartidor logueado, entrega fallida |
| **Pasos** | 1. Acceder a entrega fallida<br>2. Hacer clic en "Reportar Fallo"<br>3. Seleccionar motivo<br>4. Añadir comentario adicional<br>5. Subir foto si es necesario |
| **Resultado Esperado** | Comentario y evidencia registrados |
| **Prioridad** | Media |

### **TC-DEL-007: Alertas de Reprogramación**
| Campo | Valor |
|-------|-------|
| **ID** | TC-DEL-007 |
| **Título** | Recibir alertas de entregas reprogramadas |
| **Descripción** | Verificar que el coordinador recibe alertas de entregas reprogramadas para reordenar rutas |
| **Precondiciones** | Coordinador logueado, entrega reprogramada |
| **Pasos** | 1. Cliente reprograma entrega<br>2. Verificar notificación en panel de coordinador<br>3. Revisar nueva asignación de rutas |
| **Resultado Esperado** | Alerta visible y rutas actualizadas |
| **Prioridad** | Alta |

---

## Resumen de Casos de Prueba

| Módulo | Casos de Prueba | Estado | Responsable |
|--------|----------------|--------|-------------|
| **Autenticación** | TC-AUTH-001 a TC-AUTH-002 | ✅ Completado | Equipo Backend |
| **Catálogo** | TC-CAT-001 a TC-CAT-002 | ✅ Completado | Equipo Frontend |
| **Entregas** | TC-DEL-001 a TC-DEL-007 | ✅ Completado | Equipo Full-Stack |

**Total: 9 casos de prueba** diseñados por nuestro equipo basados en las historias de usuario completadas.

### Distribución de Responsabilidades
- **Equipo Backend**: Autenticación y lógica de negocio
- **Equipo Frontend**: Interfaz de usuario y experiencia
- **Equipo Full-Stack**: Integración y funcionalidades complejas

---

## Configuración del Entorno de Pruebas

Nuestro equipo ha preparado la siguiente configuración para ejecutar las pruebas:

### Instalación y Configuración
```bash
# 1. Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Migrar base de datos
python manage.py migrate

# 4. Crear datos de prueba
python manage.py seed_store

# 5. Crear superusuario
python manage.py createsuperuser
```

### Usuarios de Prueba Preparados por el Equipo
```python
# Script desarrollado por nuestro equipo para crear usuarios de prueba
python manage.py shell
>>> from django.contrib.auth.models import User
>>> from accounts.models import UserProfile

# Cliente de prueba
cliente = User.objects.create_user('cliente_test', 'cliente@test.com', 'pass123')
UserProfile.objects.create(user=cliente, role='cliente')

# Repartidor de prueba
repartidor = User.objects.create_user('repartidor_test', 'repartidor@test.com', 'pass123')
UserProfile.objects.create(user=repartidor, role='repartidor')

# Coordinador/Manager de prueba
coord = User.objects.create_user('coord_test', 'coord@test.com', 'pass123')
UserProfile.objects.create(user=coord, role='manager')
```

---

## Prioridades de Ejecución

1. **Alta Prioridad**: TC-AUTH-001, TC-AUTH-002, TC-CAT-001, TC-CAT-002, TC-DEL-001, TC-DEL-002, TC-DEL-007
2. **Media Prioridad**: TC-DEL-003, TC-DEL-004, TC-DEL-005, TC-DEL-006

---

## Checklist de Ejecución

- [ ] Configurar entorno de pruebas
- [ ] Crear usuarios de prueba
- [ ] Ejecutar casos de autenticación
- [ ] Ejecutar casos de catálogo
- [ ] Ejecutar casos de entregas
- [ ] Documentar resultados
- [ ] Reportar bugs encontrados

---

## Notas Importantes

- Todos los casos están basados en funcionalidades **completadas** según el tablero
- Se incluyen validaciones de SLA y controles de acceso por rol
- Los casos cubren el flujo completo desde login hasta gestión de entregas
- Se consideran tanto casos exitosos como de error/validación
