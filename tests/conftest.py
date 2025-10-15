"""
Configuración global para las pruebas automatizadas
"""
import pytest
from playwright.sync_api import sync_playwright
from faker import Faker

fake = Faker('es_ES')

@pytest.fixture(scope="function")
def browser_context():
    """Configuración del navegador para todas las pruebas"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        yield context
        browser.close()

@pytest.fixture
def page(browser_context):
    """Página nueva para cada prueba"""
    page = browser_context.new_page()
    yield page
    page.close()

@pytest.fixture(scope="function")
def base_url():
    """URL base de la aplicación"""
    return "http://localhost:8000"

@pytest.fixture
def test_user_data():
    """Datos de usuario de prueba"""
    return {
        'username': fake.user_name(),
        'email': fake.email(),
        'password': 'TestPassword123!',
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'phone': fake.phone_number()
    }

@pytest.fixture
def test_delivery_data():
    """Datos de entrega de prueba"""
    return {
        'address': fake.street_address(),
        'city': fake.city(),
        'postal_code': fake.postcode(),
        'notes': fake.text(max_nb_chars=100)
    }
