from django.contrib import admin
from .models import Task, Comment, Attachment


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "priority",
        "due_date",
        "creator",
        "assignee",
        "team",
    )
    list_filter = ("status", "priority", "team")
    search_fields = ("title", "description")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("task", "user", "created_at")
    list_filter = ("task", "user")
    search_fields = ("content",)


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("task", "file", "uploaded_by", "uploaded_at")


admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Attachment, AttachmentAdmin)
