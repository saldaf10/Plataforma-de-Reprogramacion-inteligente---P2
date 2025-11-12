from django import template
from django.templatetags.static import static

register = template.Library()


# Mapeo de nombres de productos a archivos de imagen estáticos
PRODUCT_IMAGE_MAP = {
    # Por nombre exacto - Zapatos/Calzado
    "Tenis Urban Pro": "products/tenisurbanpro.png",
    "Botas Trekking X": "products/botastrekkingx.png",
    "Zapatos Deportivos Pro": "products/tenisurbanpro.png",
    
    # Lociones/Cuidado Personal
    "Aroma Nocturno": "products/aromanocturno.png",
    "Cítrico Fresh": "products/Citricofresh.png",
    "Loción Corporal Fresh": "products/Citricofresh.png",
    
    # Proteínas/Suplementos (múltiples variaciones del nombre)
    "Whey Protein 1kg": "products/Wheyprotein1kg.png",
    "Proteína Whey 1kg": "products/Wheyprotein1kg.png",  # ← AGREGADO
    "Caseína 1kg": "products/Caseina1kg.png",
}

# Mapeo por palabras clave (fallback)
PRODUCT_KEYWORD_MAP = {
    "tenis": "products/tenisurbanpro.png",
    "zapato": "products/tenisurbanpro.png",
    "bota": "products/botastrekkingx.png",
    "aroma": "products/aromanocturno.png",
    "loción": "products/Citricofresh.png",
    "locion": "products/Citricofresh.png",
    "cítrico": "products/Citricofresh.png",
    "citrico": "products/Citricofresh.png",
    "fresh": "products/Citricofresh.png",
    "whey": "products/Wheyprotein1kg.png",
    "proteína": "products/Wheyprotein1kg.png",
    "proteina": "products/Wheyprotein1kg.png",
    "caseína": "products/Caseina1kg.png",
    "caseina": "products/Caseina1kg.png",
}


@register.simple_tag
def product_image(product):
    """
    Retorna la URL de la imagen estática para un producto.
    Prioridad:
    1. Si el producto tiene image cargada en la BD, usar esa
    2. Buscar en el mapeo por nombre exacto
    3. Buscar por palabras clave en el nombre
    4. Retornar None (el template mostrará el placeholder)
    """
    # Si el producto tiene imagen en la BD, usarla
    if product.image:
        return product.image.url
    
    # Buscar por nombre exacto
    if product.name in PRODUCT_IMAGE_MAP:
        return static(PRODUCT_IMAGE_MAP[product.name])
    
    # Buscar por palabras clave
    product_name_lower = product.name.lower()
    for keyword, image_path in PRODUCT_KEYWORD_MAP.items():
        if keyword in product_name_lower:
            return static(image_path)
    
    # No se encontró imagen
    return None


@register.simple_tag
def product_has_image(product):
    """
    Verifica si un producto tiene imagen (BD o estática)
    """
    # Si tiene imagen en BD
    if product.image:
        return True
    
    # Si está en el mapeo por nombre
    if product.name in PRODUCT_IMAGE_MAP:
        return True
    
    # Si coincide con keywords
    product_name_lower = product.name.lower()
    for keyword in PRODUCT_KEYWORD_MAP.keys():
        if keyword in product_name_lower:
            return True
    
    return False

