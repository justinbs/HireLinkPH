from django.urls import path
from . import views

urlpatterns = [
    path("employer/", views.employer_org_view, name="employer_org"),
    path("employer/jobs/", views.job_list_view, name="job_list"),
    path("employer/jobs/new/", views.job_create_view, name="job_create"),
    path("employer/jobs/<int:pk>/edit/", views.job_update_view, name="job_edit"),
    path("employer/jobs/<int:pk>/delete/", views.job_delete_view, name="job_delete"),
    path("employer/jobs/<int:pk>/skills/", views.job_skills_view, name="job_skills"),

    # public-ish views (simple for now)
    path("jobs/<int:pk>/", views.job_detail_view, name="job_detail"),
]
