from django import template


register = template.Library()


@register.filter
def status_badge(status: str) -> str:
    mapping = {
        "asignada": "bg-secondary",  # gris
        "en_ruta": "bg-primary",     # azul
        "entregada": "bg-success",   # verde
        "fallida": "bg-danger",      # rojo
    }
    return mapping.get(status, "bg-secondary")


@register.filter
def is_final_state(status):
    """Verifica si el estado es final (no modificable)"""
    return status in ['entregada', 'fallida']


@register.filter
def is_modifiable(status):
    """Verifica si el estado permite modificaciones"""
    return status not in ['entregada', 'fallida']


