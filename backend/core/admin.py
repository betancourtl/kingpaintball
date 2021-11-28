from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext
from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    # Fieldsets for admin/core/user/<id>/change/
    fieldsets = (
        (
            None,
            {'fields': ('email', 'password',)}
        ),
        (
            gettext('Personal Info'),
            {'fields': ('name',)}
        ),
        (
            gettext('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser',)}
        ),
        (
            gettext('Important dates'),
            {'fields': ('last_login',)}
        ),
    )
    # Fieldsets for /admin/core/user/
    add_fieldsets = (
        (
            None,
            {'classes': ('wide',), 'fields': ('email', 'password1', 'password2',)}
        ),
    )


admin.site.register(models.User, UserAdmin)
