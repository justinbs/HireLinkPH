from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm
from .models import User

def register_view(request, default_role=None):
    initial = {}
    # allow ?role=seeker|employer or url kwarg
    role_param = request.GET.get("role") or default_role
    if role_param in {"seeker", "employer", "admin"}:
        initial["role"] = role_param

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user: User = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.role = form.cleaned_data["role"]
            user.save()
            messages.success(request, "Account created. You can now sign in.")
            return redirect("accounts:login")
    else:
        form = RegistrationForm(initial=initial)

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            login(request, user)
            return redirect("accounts:dashboard")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been signed out.")
    return redirect("home")

@login_required
def dashboard_view(request):
    # Redirects to the correct dashboard by role
    role = getattr(request.user, "role", "seeker")
    template_map = {
        "seeker": "dashboards/seeker.html",
        "employer": "dashboards/employer.html",
        "admin": "dashboards/admin.html",
    }
    return render(request, template_map.get(role, "dashboards/seeker.html"))
