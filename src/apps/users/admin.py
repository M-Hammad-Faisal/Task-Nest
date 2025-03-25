from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Team


class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_verified", "is_staff")
    list_filter = ("role", "is_verified", "is_staff")
    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields", {"fields": ("role", "is_verified")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Custom Fields", {"fields": ("role", "is_verified")}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Team, admin.ModelAdmin)