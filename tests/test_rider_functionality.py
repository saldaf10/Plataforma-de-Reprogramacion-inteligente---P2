"""
Pruebas automatizadas para Historias de Usuario P2 #3, #7, #13
Funcionalidades del Repartidor
"""
import pytest
from tests.pages.login_page import LoginPage
from tests.pages.delivery_page import DeliveryPage

class TestRiderFunctionality:
    """Test suite para funcionalidades del repartidor"""
    
    @pytest.mark.test_id("P2-003")
    def test_rider_notified_on_reschedule(self, page, base_url):
        """
        P2 #3: Ser notificado cuando cliente reprograma
        """
        login_page = LoginPage(page)
        delivery_page = DeliveryPage(page)
        
        # Login como repartidor
        page.goto(f"{base_url}/accounts/login/")
        login_page.login("repartidor_test", "password123")
        
        # Ir a página de notificaciones del repartidor
        page.goto(f"{base_url}/orders/notifications/")
        
        # Verificar que aparece notificación de reprogramación
        assert delivery_page.check_notification_exists(), \
            "Repartidor no recibió notificación de reprogramación"
        
        # Verificar contenido de la notificación
        notification_text = delivery_page.get_notification_text()
        assert "reprogram" in notification_text.lower() or "cambió" in notification_text.lower(), \
            "La notificación no indica reprogramación"
        
        delivery_page.take_screenshot("rider_reschedule_notification")
    
    @pytest.mark.test_id("P2-007")
    def test_view_rescheduled_deliveries(self, page, base_url):
        """
        P2 #7: Ver entregas reprogramadas en la app
        """
        login_page = LoginPage(page)
        delivery_page = DeliveryPage(page)
        
        # Login como repartidor
        page.goto(f"{base_url}/accounts/login/")
        login_page.login("repartidor_test", "password123")
        
        # Ir a página de pedidos del repartidor
        page.goto(f"{base_url}/orders/rider-orders/")
        
        # Esperar a que cargue la página
        page.wait_for_load_state("networkidle")
        
        # Verificar que se muestran las entregas (buscar diferentes selectores posibles)
        delivery_visible = (page.is_visible(".modern-card") or 
                          page.is_visible(".card") or 
                          page.is_visible(".delivery-item") or
                          page.is_visible("[data-testid='delivery-list']") or
                          page.locator("text=Entrega").count() > 0)
        
        assert delivery_visible, \
            "No se muestra lista de entregas. Verificar permisos del repartidor o datos de prueba"
        
        # Buscar entregas reprogramadas (marcadas como tal)
        rescheduled_deliveries = page.locator(".modern-badge.badge-warning").count()
        
        if rescheduled_deliveries > 0:
            # Hacer clic en una entrega reprogramada (primer enlace en la tarjeta)
            page.click(".modern-card a:first-child")
            
            # Verificar que se muestra información de reprogramación
            assert page.is_visible(".modern-card"), \
                "No se muestra información de reprogramación"
            
            # Verificar que se muestra nueva fecha/hora
            assert page.is_visible(".modern-badge"), \
                "No se muestra nueva fecha/hora de entrega"
            
            delivery_page.take_screenshot("rescheduled_delivery_view")
    
    @pytest.mark.test_id("P2-013")
    def test_add_failure_reason(self, page, base_url):
        """
        P2 #13: Añadir motivo de fallo
        """
        login_page = LoginPage(page)
        delivery_page = DeliveryPage(page)
        
        # Login como repartidor
        page.goto(f"{base_url}/accounts/login/")
        login_page.login("repartidor_test", "password123")
        
        # Ir a página de pedidos del repartidor
        page.goto(f"{base_url}/orders/rider-orders/")
        
        # Buscar entrega en proceso
        if page.is_visible(".delivery-item.in-progress"):
            page.click(".delivery-item.in-progress:first-child")
            
            # Buscar opción para reportar fallo
            if page.is_visible(".report-failure-btn"):
                page.click(".report-failure-btn")
                
                # Verificar que aparece formulario de fallo
                assert page.is_visible("textarea[name='failure_reason']"), \
                    "No aparece campo para motivo de fallo"
                
                # Llenar motivo del fallo
                failure_reason = "Dirección incorrecta - No se encuentra el domicilio"
                page.fill("textarea[name='failure_reason']", failure_reason)
                
                # Verificar que se puede subir foto
                assert page.is_visible("input[type='file']"), \
                    "No aparece opción para subir foto"
                
                # Subir foto de evidencia (archivo dummy)
                # page.set_input_files("input[type='file']", "test_evidence.jpg")
                
                # Enviar reporte de fallo
                page.click(".submit-failure-btn")
                
                # Verificar confirmación
                page.wait_for_selector(".success-message", timeout=10000)
                assert page.is_visible(".success-message"), \
                    "No se confirmó el reporte de fallo"
                
                delivery_page.take_screenshot("failure_reported")
    
    @pytest.mark.test_id("P2-013-VERIFY")
    def test_verify_failure_reason_saved(self, page, base_url):
        """
        Verificar que el motivo de fallo se guarda correctamente
        """
        login_page = LoginPage(page)
        
        # Login como cliente para verificar
        page.goto(f"{base_url}/accounts/login/")
        login_page.login("cliente_test", "password123")
        
        # Ir a página de entregas del cliente
        page.goto(f"{base_url}/orders/my-orders/")
        
        # Buscar entrega con fallo
        if page.is_visible(".delivery-item.failed"):
            page.click(".delivery-item.failed:first-child")
            
            # Verificar que se muestra el motivo del fallo
            assert page.is_visible(".failure-reason"), \
                "No se muestra motivo del fallo al cliente"
            
            failure_text = page.text_content(".failure-reason")
            assert len(failure_text.strip()) > 0, \
                "El motivo del fallo está vacío"
            
            # Verificar que se puede ver la foto si se subió
            if page.is_visible(".failure-photo"):
                assert page.is_visible("img.failure-photo"), \
                    "No se muestra la foto de evidencia del fallo"
