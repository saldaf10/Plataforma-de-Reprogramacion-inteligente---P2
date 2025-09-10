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


