from django.urls import path
from . import views

urlpatterns = [
    path("me/", views.profile_edit_view, name="edit"),
    path("skills/", views.profile_skills_view, name="skills"),
    path("skills/<int:pk>/delete/", views.profile_skill_delete_view, name="skill_delete"),
]
