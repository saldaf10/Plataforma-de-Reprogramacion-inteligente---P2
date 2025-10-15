#!/usr/bin/env python3
"""
Script principal para ejecutar todas las pruebas automatizadas
"""
import subprocess
import sys
import os
from datetime import datetime

def create_directories():
    """Crear directorios necesarios para los reportes"""
    directories = ['reports', 'screenshots', 'logs']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def install_dependencies():
    """Instalar dependencias de testing"""
    print("🔧 Instalando dependencias de testing...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements-testing.txt'], 
                      check=True, capture_output=True, text=True)
        subprocess.run(['playwright', 'install', 'chromium'], check=True, capture_output=True, text=True)
        print("✅ Dependencias instaladas correctamente")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False
    return True

def run_tests(test_type="all"):
    """Ejecutar las pruebas según el tipo especificado"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Configurar comandos según el tipo de prueba
    if test_type == "notifications":
        cmd = ["pytest", "tests/test_notifications.py", "-v", "--tb=short"]
        report_name = f"notifications_report_{timestamp}.html"
    elif test_type == "rescheduling":
        cmd = ["pytest", "tests/test_rescheduling.py", "-v", "--tb=short"]
        report_name = f"rescheduling_report_{timestamp}.html"
    elif test_type == "rider":
        cmd = ["pytest", "tests/test_rider_functionality.py", "-v", "--tb=short"]
        report_name = f"rider_report_{timestamp}.html"
    elif test_type == "smoke":
        cmd = ["pytest", "-m", "smoke", "-v", "--tb=short"]
        report_name = f"smoke_report_{timestamp}.html"
    else:  # all
        cmd = ["pytest", "tests/", "-v", "--tb=short"]
        report_name = f"full_report_{timestamp}.html"
    
    # Agregar configuración de reportes
    cmd.extend([
        f"--html=reports/{report_name}",
        "--self-contained-html",
        "--alluredir=reports/allure-results"
    ])
    
    print(f"🚀 Ejecutando pruebas: {test_type}")
    print(f"📊 Reporte se generará en: reports/{report_name}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        print("📋 Resultado de las pruebas:")
        print(result.stdout)
        
        if result.stderr:
            print("⚠️  Errores/Warnings:")
            print(result.stderr)
        
        print(f"✅ Pruebas completadas. Reporte disponible en: reports/{report_name}")
        
        # Generar reporte Allure si está disponible
        try:
            subprocess.run(["allure", "generate", "reports/allure-results", "-o", "reports/allure-report", "--clean"], 
                          check=True, capture_output=True, text=True)
            print("📈 Reporte Allure generado en: reports/allure-report")
        except:
            print("ℹ️  Allure no disponible, solo reporte HTML generado")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error ejecutando pruebas: {e}")
        return False

def main():
    """Función principal"""
    print("🧪 Framework de Testing Automatizado - Plataforma de Reprogramación")
    print("=" * 70)
    
    # Crear directorios
    create_directories()
    
    # Verificar argumentos
    test_type = "all"
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
    
    valid_types = ["all", "notifications", "rescheduling", "rider", "smoke"]
    if test_type not in valid_types:
        print(f"❌ Tipo de prueba inválido. Opciones: {', '.join(valid_types)}")
        return
    
    # Instalar dependencias
    if not install_dependencies():
        return
    
    # Ejecutar pruebas
    success = run_tests(test_type)
    
    if success:
        print("\n🎉 Todas las pruebas completadas exitosamente!")
    else:
        print("\n⚠️  Algunas pruebas fallaron. Revisar reportes para más detalles.")
    
    print("\n📁 Archivos generados:")
    print("  - reports/: Reportes HTML y Allure")
    print("  - screenshots/: Capturas de pantalla de las pruebas")
    print("  - logs/: Logs detallados (si están configurados)")

if __name__ == "__main__":
    main()
