from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "password",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    list_filter = ("is_active",)
    filter_horizontal = ("groups",)
