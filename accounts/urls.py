from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("register/seeker/", views.register_view, {"default_role": "seeker"}, name="register_seeker"),
    path("register/employer/", views.register_view, {"default_role": "employer"}, name="register_employer"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
]
