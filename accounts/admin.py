"""
==============================================================
NayePankh Foundation - Accounts Admin Configuration
==============================================================
Registers the custom User model with Django's admin panel.
==============================================================
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin configuration for the User model.
    Extends the default UserAdmin to display our custom fields.
    """

    # Columns shown in the user list
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'email_verified', 'is_active', 'date_joined')

    # Filters in the right sidebar
    list_filter = ('role', 'email_verified', 'is_active', 'is_staff', 'date_joined')

    # Searchable fields
    search_fields = ('username', 'email', 'first_name', 'last_name')

    # Default ordering
    ordering = ('-date_joined',)

    # Fields displayed when editing a user
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'email_verified', 'verification_token'),
        }),
    )

    # Fields displayed when creating a new user via admin
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('email', 'first_name', 'last_name', 'role'),
        }),
    )

    # Read-only fields
    readonly_fields = ('verification_token', 'updated_at')
