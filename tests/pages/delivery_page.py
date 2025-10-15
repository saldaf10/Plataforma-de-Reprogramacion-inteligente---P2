"""
Página de entregas para las pruebas automatizadas
"""
from .base_page import BasePage

class DeliveryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Selectores para elementos de entrega
        self.delivery_status = ".delivery-status"
        self.reschedule_button = ".reschedule-btn"
        self.new_date_input = "input[name='new_date']"
        self.time_slot_select = "select[name='time_slot']"
        self.confirm_reschedule = ".confirm-reschedule"
        self.delivery_history = ".delivery-history"
        self.failure_reason = "textarea[name='failure_reason']"
        self.upload_photo = "input[type='file']"
        self.notification_area = ".notifications"
    
    def reschedule_delivery(self, new_date: str, time_slot: str):
        """Reprogramar una entrega"""
        self.click_element(self.reschedule_button)
        self.wait_for_element(self.new_date_input)
        self.fill_input(self.new_date_input, new_date)
        self.page.select_option(self.time_slot_select, time_slot)
        self.click_element(self.confirm_reschedule)
        self.wait_for_load_state("networkidle")
    
    def get_delivery_status(self) -> str:
        """Obtener el estado actual de la entrega"""
        return self.get_text(self.delivery_status)
    
    def report_delivery_failure(self, reason: str, photo_path: str = None):
        """Reportar fallo en la entrega"""
        self.fill_input(self.failure_reason, reason)
        if photo_path:
            self.page.set_input_files(self.upload_photo, photo_path)
        self.click_element(".report-failure-btn")
        self.wait_for_load_state("networkidle")
    
    def check_notification_exists(self) -> bool:
        """Verificar si existe una notificación"""
        # Buscar notificaciones en diferentes formatos
        return (self.is_element_visible(".card") or 
                self.is_element_visible(".badge") or 
                self.is_element_visible(".modern-badge") or
                self.is_element_visible(self.notification_area))
    
    def get_notification_text(self) -> str:
        """Obtener texto de la notificación"""
        if self.check_notification_exists():
            # Buscar texto en diferentes elementos de notificación
            if self.is_element_visible(".card"):
                return self.get_text(".card")
            elif self.is_element_visible(".badge"):
                return self.get_text(".badge")
            elif self.is_element_visible(".modern-badge"):
                return self.get_text(".modern-badge")
            else:
                return self.get_text(self.notification_area)
        return ""
