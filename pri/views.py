from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.conf import settings
from pathlib import Path


def pri_home(request):
    # Si el usuario tiene rol, lo dirigimos a la vista mock correspondiente
    if request.user.is_authenticated and hasattr(request.user, "profile"):
        role = request.user.profile.role
        if role == "cliente":
            return redirect("pri:mock_cliente")
        if role == "repartidor":
            return redirect("pri:mock_repartidor")
        if role == "manager":
            return redirect("pri:mock_dashboard")
    # Fallback a la página puente
    return render(request, "pri/home.html")


def _serve_mock_file(filename: str):
    base = Path(settings.BASE_DIR).parent  # carpeta del proyecto con los HTML mock
    file_path = base / filename
    if not file_path.exists():
        raise Http404("Mock no encontrado")
    content = file_path.read_text(encoding="utf-8")
    return HttpResponse(content, content_type="text/html; charset=utf-8")


def mock_index(request):
    return _serve_mock_file("index.html")


def mock_cliente(request):
    return _serve_mock_file("cliente.html")


def mock_repartidor(request):
    return _serve_mock_file("repartidor.html")


def mock_dashboard(request):
    return _serve_mock_file("dashboard.html")


def mock_confirmacion(request):
    return _serve_mock_file("confirmacion.html")
from django.shortcuts import render

# Create your views here.
