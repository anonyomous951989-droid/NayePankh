"""
NayePankh Foundation - Event Admin Configuration
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Event, VolunteerAssignment, Attendance, EventInterest, Notification


class EventInterestInline(admin.TabularInline):
    """Show interested volunteers inline within an Event admin page."""
    model = EventInterest
    extra = 0
    readonly_fields = ('volunteer', 'submitted_at', 'is_cancelled', 'cancelled_at')
    fields = ('volunteer', 'submitted_at', 'is_cancelled', 'cancelled_at')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'date', 'start_time', 'location', 'status',
        'max_volunteers', 'assigned_count', 'interested_count_display'
    )
    list_filter = ('status', 'date')
    search_fields = ('title', 'location', 'description')
    ordering = ('-date',)
    list_per_page = 20
    inlines = [EventInterestInline]

    @admin.display(description='Interested')
    def interested_count_display(self, obj):
        count = obj.interested_count
        if count > 0:
            return format_html(
                '<span style="color:#e94560;font-weight:bold;">{}</span>',
                count
            )
        return '0'


@admin.register(VolunteerAssignment)
class VolunteerAssignmentAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'event', 'status', 'assigned_date')
    list_filter = ('status', 'event')
    search_fields = ('volunteer__user__first_name', 'volunteer__user__last_name', 'event__title')


@admin.register(EventInterest)
class EventInterestAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'event', 'submitted_at', 'is_cancelled', 'cancelled_at')
    list_filter = ('is_cancelled', 'event')
    search_fields = (
        'volunteer__user__first_name', 'volunteer__user__last_name',
        'event__title'
    )
    readonly_fields = ('submitted_at', 'cancelled_at')
    ordering = ('-submitted_at',)
    list_per_page = 25


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'event', 'status', 'check_in', 'check_out')
    list_filter = ('status', 'event')
    search_fields = ('volunteer__user__first_name', 'volunteer__user__last_name', 'event__title')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'title', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('recipient__first_name', 'recipient__last_name', 'title', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    list_per_page = 25
