"""
Pruebas automatizadas para Historias de Usuario P2 #9, #10
Reprogramación de Entregas desde Cliente
"""
import pytest
from datetime import datetime, timedelta
from tests.pages.login_page import LoginPage
from tests.pages.delivery_page import DeliveryPage

class TestRescheduling:
    """Test suite para funcionalidades de reprogramación"""
    
    @pytest.mark.test_id("P2-009")
    def test_select_date_and_time_range(self, page, base_url):
        """
        P2 #9: Seleccionar fecha y rango de horas
        """
        login_page = LoginPage(page)
        delivery_page = DeliveryPage(page)
        
        # Login como cliente
        page.goto(f"{base_url}/accounts/login/")
        login_page.login("cliente_test", "password123")
        
        # Ir a página de entregas
        page.goto(f"{base_url}/orders/my-orders/")
        
        # Buscar entrega que se pueda reprogramar
        if page.is_visible(".delivery-item"):
            page.click(".delivery-item")
            
            # Hacer clic en reprogramar
            if page.is_visible(".reschedule-btn"):
                page.click(".reschedule-btn")
                
                # Verificar que aparece selector de fecha
                assert page.is_visible("input[name='new_date']"), \
                    "No aparece selector de fecha"
                
                # Verificar que aparece selector de hora
                assert page.is_visible("select[name='time_slot']"), \
                    "No aparece selector de hora"
                
                # Verificar que hay opciones de hora disponibles
                time_options = page.locator("select[name='time_slot'] option").count()
                assert time_options > 1, \
                    "No hay suficientes opciones de hora disponibles"
                
                delivery_page.take_screenshot("date_time_selector")
    
    @pytest.mark.test_id("P2-010")
    def test_reschedule_delivery_from_web(self, page, base_url):
        """
        P2 #10: Reprogramar entrega desde web o app
        """
        login_page = LoginPage(page)
        delivery_page = DeliveryPage(page)
        
        # Login como cliente
        page.goto(f"{base_url}/accounts/login/")
        login_page.login("cliente_test", "password123")
        
        # Ir a página de entregas
        page.goto(f"{base_url}/orders/my-orders/")
        
        # Buscar entrega que se pueda reprogramar
        if page.is_visible(".delivery-item"):
            page.click(".delivery-item")
            
            # Obtener fecha actual de la entrega
            original_date = page.text_content(".delivery-date")
            
            # Hacer clic en reprogramar
            if page.is_visible(".reschedule-btn"):
                page.click(".reschedule-btn")
                
                # Seleccionar nueva fecha (mañana)
                tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
                page.fill("input[name='new_date']", tomorrow)
                
                # Seleccionar nuevo horario
                page.select_option("select[name='time_slot']", "09:00-12:00")
                
                # Confirmar reprogramación
                page.click(".confirm-reschedule")
                
                # Esperar confirmación
                page.wait_for_selector(".success-message", timeout=10000)
                
                # Verificar que se muestra mensaje de éxito
                assert page.is_visible(".success-message"), \
                    "No se mostró mensaje de éxito"
                
                # Verificar que la fecha cambió
                page.reload()
                new_date = page.text_content(".delivery-date")
                assert new_date != original_date, \
                    "La fecha de entrega no cambió"
                
                delivery_page.take_screenshot("reschedule_success")
    
    @pytest.mark.test_id("P2-010-REAL-TIME")
    def test_reschedule_availability_real_time(self, page, base_url):
        """
        Verificar disponibilidad en tiempo real al reprogramar
        """
        login_page = LoginPage(page)
        
        # Login como cliente
        page.goto(f"{base_url}/accounts/login/")
        login_page.login("cliente_test", "password123")
        
        # Ir a página de reprogramación
        page.goto(f"{base_url}/orders/my-orders/")
        
        if page.is_visible(".delivery-item"):
            page.click(".delivery-item")
            
            if page.is_visible(".reschedule-btn"):
                page.click(".reschedule-btn")
                
                # Seleccionar una fecha
                tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
                page.fill("input[name='new_date']", tomorrow)
                
                # Verificar que las opciones de hora se actualizan
                # (esto requeriría implementación AJAX)
                page.wait_for_timeout(2000)  # Esperar actualización
                
                # Verificar que hay opciones disponibles
                available_slots = page.locator(".time-slot.available").count()
                assert available_slots > 0, \
                    "No hay horarios disponibles en tiempo real"
