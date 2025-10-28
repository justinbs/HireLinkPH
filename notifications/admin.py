from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "notification_read", "notification_created_at")
    list_filter = ("notification_read",)
    search_fields = ("user__username", "title", "body")
