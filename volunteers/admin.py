"""
==============================================================
NayePankh Foundation - Volunteer Admin Configuration
==============================================================
Admin panel configuration for managing volunteer profiles.
Includes search, filters, bulk actions, and custom display.
==============================================================
"""

from django.contrib import admin
from .models import VolunteerProfile


@admin.register(VolunteerProfile)
class VolunteerProfileAdmin(admin.ModelAdmin):
    """Admin configuration for VolunteerProfile model."""

    # Columns displayed in the list view
    list_display = (
        'user', 'phone', 'city', 'state', 'education',
        'availability', 'status', 'volunteer_id', 'created_at',
    )

    # Filters in the right sidebar
    list_filter = ('status', 'gender', 'availability', 'state', 'created_at')

    # Searchable fields
    search_fields = (
        'user__first_name', 'user__last_name', 'user__email',
        'phone', 'city', 'state', 'skills', 'volunteer_id',
    )

    # Read-only fields
    readonly_fields = ('created_at', 'updated_at')

    # Default ordering
    ordering = ('-created_at',)

    # Number of items per page
    list_per_page = 25

    # Editable fields directly in list view
    list_editable = ('status',)

    # Fields grouped in sections when editing
    fieldsets = (
        ('User Link', {
            'fields': ('user',)
        }),
        ('Personal Information', {
            'fields': ('phone', 'date_of_birth', 'gender')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state')
        }),
        ('Education & Skills', {
            'fields': ('education', 'skills', 'interests')
        }),
        ('Availability & Uploads', {
            'fields': ('availability', 'resume', 'photo')
        }),
        ('Application Status', {
            'fields': ('status', 'rejection_reason', 'volunteer_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # Collapsible section
        }),
    )

    # Custom admin actions
    actions = ['approve_volunteers', 'reject_volunteers']

    def approve_volunteers(self, request, queryset):
        """Bulk approve selected volunteers."""
        for profile in queryset:
            profile.status = 'approved'
            profile.generate_volunteer_id()
            profile.save()
        self.message_user(request, f'{queryset.count()} volunteer(s) approved.')
    approve_volunteers.short_description = 'Approve selected volunteers'

    def reject_volunteers(self, request, queryset):
        """Bulk reject selected volunteers."""
        queryset.update(status='rejected')
        self.message_user(request, f'{queryset.count()} volunteer(s) rejected.')
    reject_volunteers.short_description = 'Reject selected volunteers'
