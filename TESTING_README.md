# 🧪 Framework de Testing Automatizado - Sprint 2

## 📋 Descripción del Proyecto

Este framework de testing automatizado fue desarrollado para validar las **historias de usuario completadas del Sprint 2** de la **Plataforma de Reprogramación Inteligente (PRI)**.

### 🎯 Objetivo del Sprint 2
Implementar y validar funcionalidades críticas de reprogramación de entregas y sistema de notificaciones para mejorar la experiencia del usuario final.

### 📊 Historias de Usuario Validadas

#### 🟣 **Notificaciones y Confirmaciones del Cliente**
- **P2 #1** - Recibir notificación cuando falla la entrega
- **P2 #2** - Confirmar recepción de notificaciones  
- **P2 #11** - Consultar evidencia del fallo

#### 🔄 **Reprogramación de Entregas**
- **P2 #9** - Seleccionar fecha y rango de horas
- **P2 #10** - Reprogramar entrega desde web o app

#### 🛵 **Funcionalidades del Repartidor**
- **P2 #3** - Ser notificado cuando cliente reprograma
- **P2 #7** - Ver entregas reprogramadas en la app
- **P2 #13** - Añadir motivo de fallo

## 🛠️ Cómo se Implementó el Framework

### 📅 Proceso de Desarrollo
1. **Análisis de Requerimientos** - Revisión de las historias de usuario del Sprint 2
2. **Diseño del Framework** - Arquitectura basada en Page Object Model
3. **Creación de Datos de Prueba** - Script automatizado para generar escenarios reales
4. **Implementación de Pruebas** - Casos de prueba específicos para cada historia de usuario
5. **Validación y Corrección** - Ajuste de selectores CSS basado en el HTML real

### 🏗️ Arquitectura del Framework
- **Playwright** - Motor de automatización web moderno
- **Page Object Model** - Patrón de diseño para mantenibilidad
- **pytest** - Framework de testing con reportes HTML
- **Datos de Prueba Automatizados** - Generación de usuarios, órdenes y notificaciones

### 📁 Archivos Creados
```
tests/
├── conftest.py                    # Configuración global
├── config/test_config.py         # Configuración de entornos
├── pages/                        # Page Object Model
│   ├── base_page.py
│   ├── login_page.py
│   └── delivery_page.py
├── test_notifications.py         # P2 #1, #2, #11
├── test_rescheduling.py          # P2 #9, #10
└── test_rider_functionality.py   # P2 #3, #7, #13

generate_test_data.py             # Script de datos de prueba
run_tests.py                      # Script de ejecución
pytest.ini                       # Configuración de pytest
```

## 🚀 Instalación y Configuración

### 1. Instalar dependencias

```bash
# Instalar dependencias de testing
pip install -r requirements-testing.txt

# Instalar navegadores de Playwright
playwright install chromium
```

### 2. Configurar usuarios de prueba

Antes de ejecutar las pruebas, asegúrate de tener estos usuarios creados en tu base de datos:

```python
# Usuarios necesarios para las pruebas
cliente_test / password123
repartidor_test / password123  
manager_test / password123
```

### 3. Ejecutar el servidor Django

```bash
python manage.py runserver
```

## 🎯 Ejecutar Pruebas

### Opción 1: Script automatizado (Recomendado)

```bash
# Ejecutar todas las pruebas
python run_tests.py

# Ejecutar pruebas específicas
python run_tests.py notifications    # Solo notificaciones
python run_tests.py rescheduling     # Solo reprogramación
python run_tests.py rider           # Solo funcionalidades del repartidor
python run_tests.py smoke           # Pruebas críticas
```

### Opción 2: Comando directo de pytest

```bash
# Todas las pruebas
pytest tests/ -v

# Pruebas específicas
pytest tests/test_notifications.py -v
pytest tests/test_rescheduling.py -v
pytest tests/test_rider_functionality.py -v

# Con reporte HTML
pytest tests/ -v --html=reports/report.html --self-contained-html
```

## 📊 Resultados Finales de Testing - Sprint 2

### 🎯 Cobertura de Historias de Usuario

| Sprint | ID | Historia | Archivo de Prueba | Estado | Detalles |
|--------|----|----------|-------------------|--------|----------|
| **Sprint 2** | **P2-001** | Recibir notificación cuando falla la entrega | `test_notifications.py` | ⚠️ | Datos de notificación |
| **Sprint 2** | **P2-002** | Confirmar recepción de notificaciones | `test_notifications.py` | ✅ | **FUNCIONA** |
| **Sprint 2** | **P2-003** | Repartidor notificado cuando cliente reprograma | `test_rider_functionality.py` | ✅ | **FUNCIONA** |
| **Sprint 2** | **P2-007** | Ver entregas reprogramadas en la app | `test_rider_functionality.py` | ⚠️ | Permisos repartidor |
| **Sprint 2** | **P2-009** | Seleccionar fecha y rango de horas | `test_rescheduling.py` | ✅ | **FUNCIONA** |
| **Sprint 2** | **P2-010** | Reprogramar entrega desde web o app | `test_rescheduling.py` | ✅ | **FUNCIONA** |
| **Sprint 2** | **P2-011** | Consultar evidencia del fallo | `test_notifications.py` | ✅ | **FUNCIONA** |
| **Sprint 2** | **P2-013** | Añadir motivo de fallo | `test_rider_functionality.py` | ✅ | **FUNCIONA** |

### 📈 Métricas Finales del Sprint 2
- **Total Historias de Usuario**: 8
- **Historias Validadas**: 6 (75%)
- **Pruebas Automatizadas**: 8/10 pasaron (80%)
- **Funcionalidades Críticas**: ✅ Notificaciones, ✅ Reprogramación, ✅ Gestión de Fallos
- **Roles Cubiertos**: Cliente, Repartidor, Manager

### 🏆 Logros del Sprint 2
- ✅ **Framework de testing completamente funcional**
- ✅ **Datos de prueba generados automáticamente**
- ✅ **6 funcionalidades críticas validadas**
- ✅ **Documentación completa implementada**
- ✅ **Reportes HTML generados automáticamente**
- ✅ **Capturas de pantalla para evidencia**

## 📁 Estructura del Framework

```
tests/
├── __init__.py
├── conftest.py                 # Configuración global
├── config/
│   └── test_config.py         # Configuración de entornos
├── pages/                     # Page Object Model
│   ├── base_page.py
│   ├── login_page.py
│   └── delivery_page.py
├── test_notifications.py      # P2 #1, #2, #11
├── test_rescheduling.py       # P2 #9, #10
└── test_rider_functionality.py # P2 #3, #7, #13

reports/                       # Reportes generados
├── report.html
├── allure-results/
└── allure-report/

screenshots/                   # Capturas de evidencia
logs/                         # Logs detallados
```

## 🔧 Configuración Avanzada

### Variables de Entorno

```bash
# Configurar URL base
export TEST_BASE_URL=http://localhost:8000

# Modo headless
export HEADLESS=true

# Velocidad de ejecución
export SLOW_MO=500

# Resolución de pantalla
export VIEWPORT_WIDTH=1920
export VIEWPORT_HEIGHT=1080
```

### Configuración de Navegador

El framework usa **Playwright** con las siguientes características:

- 🌐 **Navegador**: Chromium (configurable)
- 📱 **Responsive**: Múltiples resoluciones
- ⚡ **Paralelo**: Ejecución en paralelo
- 📸 **Screenshots**: Capturas automáticas en fallos
- 🎥 **Video**: Grabación de pruebas (opcional)

## 📈 Reportes

### Reporte HTML

Después de cada ejecución se genera un reporte HTML completo en `reports/report.html` que incluye:

- ✅ Estado de cada prueba
- 📊 Estadísticas generales
- 📸 Screenshots de fallos
- ⏱️ Tiempos de ejecución
- 📝 Logs detallados

### Reporte Allure (Opcional)

Para reportes más avanzados con Allure:

```bash
# Instalar Allure
npm install -g allure-commandline

# Generar reporte
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

## 🐛 Debugging y Troubleshooting

### Problemas Comunes

1. **Usuario no encontrado**: Verificar que los usuarios de prueba existan
2. **Elemento no encontrado**: Revisar selectores CSS en las páginas
3. **Timeout**: Aumentar timeouts en `conftest.py`
4. **Servidor no responde**: Verificar que Django esté ejecutándose

### Modo Debug

Para ejecutar en modo debug con navegador visible:

```bash
export HEADLESS=false
export SLOW_MO=2000
python run_tests.py
```

## 🔄 Integración CI/CD

### GitHub Actions

```yaml
name: Automated Testing
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install -r requirements-testing.txt
          playwright install chromium
      - name: Run tests
        run: python run_tests.py
```

## 📝 Contribuir

Para agregar nuevas pruebas:

1. Crear nuevo archivo en `tests/`
2. Usar Page Object Model en `tests/pages/`
3. Seguir convenciones de naming
4. Agregar documentación
5. Incluir screenshots de evidencia

---

**Desarrollado para validar la funcionalidad de reprogramación inteligente de entregas** 🚀
