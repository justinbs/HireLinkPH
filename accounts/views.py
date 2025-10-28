from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import RegistrationForm, LoginForm


def _after_login_redirect(user):
    """Return the best landing URL based on role."""
    if getattr(user, "role", "") == "seeker":
        # Seeker: go to recommendations (or your seeker dashboard)
        return reverse("matching:recommendations")
    if getattr(user, "role", "") == "employer":
        # Employer: go to job list
        return reverse("jobs:job_list")
    # Fallback/admin
    return "/admin/"


def login_view(request):
    if request.user.is_authenticated:
        return redirect(_after_login_redirect(request.user))

    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, "Welcome back!")
        return redirect(_after_login_redirect(user))

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been signed out.")
    return redirect("accounts:login")


def register_view(request, default_role=None):
    """
    Public registration for Seeker/Employer only.
    Optional `default_role` (or ?role=) can preselect role in the form.
    """
    initial = {}
    role_param = request.GET.get("role") or default_role
    if role_param in {"seeker", "employer"}:
        initial["role"] = role_param

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # Defense-in-depth: never allow public “admin” creation.
            role = form.cleaned_data.get("role")
            if role not in {"seeker", "employer"}:
                messages.error(request, "Invalid role.")
                return render(request, "accounts/register.html", {"form": form})

            user.role = role
            user.email = form.cleaned_data.get("email")
            user.save()

            messages.success(request, "Account created. You can now sign in.")
            return redirect("accounts:login")
        else:
            messages.error(request, "Registration failed. Please review the errors below.")
    else:
        form = RegistrationForm(initial=initial)

    return render(request, "accounts/register.html", {"form": form})


@login_required
def dashboard_view(request):
    """Optional: if you use /accounts/dashboard/, route by role."""
    return redirect(_after_login_redirect(request.user))
