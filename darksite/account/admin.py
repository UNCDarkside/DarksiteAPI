from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import ugettext_lazy as _

from account import models


@admin.register(models.User)
class UserAdmin(auth_admin.UserAdmin):
    add_fieldsets = (
        (None, {
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )
    date_hierarchy = 'created'
    fieldsets = (
        (None, {
            'fields': ('email', 'name', 'password'),
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
        }),
        (_('Time Information'), {
            'fields': ('created', 'updated', 'last_login'),
        }),
    )
    list_display = (
        'email',
        'name',
        'is_active',
        'is_staff',
        'is_superuser',
        'created',
        'last_login',
    )
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    ordering = None
    readonly_fields = ('created', 'last_login', 'updated')
    search_fields = ('email', 'name',)
