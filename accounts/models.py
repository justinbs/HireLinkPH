from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # username, password, first_name, last_name come from AbstractUser
    ROLE_CHOICES = [
        ("seeker", "Seeker"),
        ("employer", "Employer"),
        ("admin", "Admin"),
    ]
    email = models.EmailField(max_length=100, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="seeker")
    contact_number = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=100, blank=True)

    user_created_at = models.DateTimeField(auto_now_add=True)
    user_updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return f"{self.username} ({self.role})"
