from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Extra info", {"fields": ("role", "contact_number", "city", "user_created_at", "user_updated_at")}),
    )
    readonly_fields = ("user_created_at", "user_updated_at")
    list_display = ("username", "email", "first_name", "last_name", "role", "city")
    list_filter = ("role", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email", "first_name", "last_name", "city")
