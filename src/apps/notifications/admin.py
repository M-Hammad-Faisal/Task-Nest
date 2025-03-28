from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "task", "message", "created_at", "is_read")
    list_filter = ("is_read", "created_at", "user")
    search_fields = ("message", "user__username", "task__title")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
