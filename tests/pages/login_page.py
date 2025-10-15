"""
Página de login para las pruebas automatizadas
"""
from .base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_input = "input[name='username']"
        self.password_input = "input[name='password']"
        self.login_button = "button[type='submit']"
        self.error_message = ".error, .alert-danger"
    
    def login(self, username: str, password: str):
        """Realizar login con credenciales"""
        self.fill_input(self.username_input, username)
        self.fill_input(self.password_input, password)
        self.click_element(self.login_button)
        self.page.wait_for_load_state("networkidle")
    
    def is_login_successful(self) -> bool:
        """Verificar si el login fue exitoso"""
        # Verificar que no estemos en la página de login
        return not self.is_element_visible(self.login_button)
    
    def get_error_message(self) -> str:
        """Obtener mensaje de error si existe"""
        if self.is_element_visible(self.error_message):
            return self.get_text(self.error_message)
        return ""
