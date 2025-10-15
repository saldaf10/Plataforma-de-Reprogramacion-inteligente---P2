"""
Página base con métodos comunes para todas las páginas
"""
from playwright.sync_api import Page, expect

class BasePage:
    def __init__(self, page: Page):
        self.page = page
    
    def navigate_to(self, url: str):
        """Navegar a una URL específica"""
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
    
    def wait_for_element(self, selector: str, timeout: int = 10000):
        """Esperar a que un elemento aparezca"""
        self.page.wait_for_selector(selector, timeout=timeout)
    
    def click_element(self, selector: str):
        """Hacer clic en un elemento"""
        self.page.click(selector)
    
    def fill_input(self, selector: str, text: str):
        """Llenar un campo de entrada"""
        self.page.fill(selector, text)
    
    def get_text(self, selector: str) -> str:
        """Obtener texto de un elemento"""
        return self.page.text_content(selector)
    
    def is_element_visible(self, selector: str) -> bool:
        """Verificar si un elemento es visible"""
        return self.page.is_visible(selector)
    
    def take_screenshot(self, name: str):
        """Tomar captura de pantalla"""
        self.page.screenshot(path=f"screenshots/{name}.png")
    
    def wait_for_notification(self):
        """Esperar a que aparezca una notificación"""
        self.page.wait_for_selector(".notification, .alert, .toast", timeout=5000)
