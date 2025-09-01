from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import UserProfile


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if not username or not password:
            messages.error(request, "Usuario y contraseña son requeridos")
            return redirect("accounts:signup")
        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe")
            return redirect("accounts:signup")
        user = User.objects.create_user(username=username, email=email, password=password)
        # Role defaults to 'cliente' via signal
        login(request, user)
        return redirect("catalog:product_list")
    return render(request, "accounts/signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("catalog:product_list")
        messages.error(request, "Credenciales inválidas")
        return redirect("accounts:login")
    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("catalog:product_list")


@login_required
def profile_view(request):
    return render(request, "accounts/profile.html")


def is_superuser(user):
    return user.is_superuser


@login_required
@user_passes_test(is_superuser)
def manage_roles(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        role = request.POST.get("role")
        try:
            u = User.objects.get(id=user_id)
            if hasattr(u, "profile"):
                u.profile.role = role
                u.profile.save()
            else:
                UserProfile.objects.create(user=u, role=role)
            messages.success(request, f"Rol actualizado para {u.username} a {role}")
        except User.DoesNotExist:
            messages.error(request, "Usuario no encontrado")
        return redirect("accounts:manage_roles")

    users = User.objects.all().order_by("username")
    return render(request, "accounts/manage_roles.html", {"users": users, "roles": ["manager", "cliente", "repartidor"]})
