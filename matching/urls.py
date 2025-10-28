from django.urls import path
from . import views

urlpatterns = [
    path("recommendations/", views.recommendations_view, name="recommendations"),
    path("candidates/<int:pk>/", views.candidates_for_job_view, name="candidates_for_job"),
]
