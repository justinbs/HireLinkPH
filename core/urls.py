from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("profiles/", include(("profiles.urls", "profiles"), namespace="profiles")),
    path("jobs/", include(("jobs.urls", "jobs"), namespace="jobs")),
]
