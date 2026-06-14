"""
==============================================================
NayePankh Foundation - Event Models
==============================================================
Models for events, volunteer assignments, attendance tracking,
interest expressions, and in-app notifications.
==============================================================
"""

from django.db import models
from django.conf import settings


class Event(models.Model):
    """
    Represents an event organized by the NayePankh Foundation.

    Events can be upcoming, open for interest, assigned, or completed.
    Volunteers can express interest; admins then assign from interested pool.
    """

    # --- Status Choices ---
    STATUS_CHOICES = (
        ('upcoming', 'Upcoming'),
        ('open_for_interest', 'Open for Interest'),
        ('assigned', 'Assigned'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    # --- Event Details ---
    title = models.CharField(
        max_length=200,
        help_text='Name of the event'
    )
    description = models.TextField(
        help_text='Detailed description of the event'
    )
    date = models.DateField(
        help_text='Date of the event'
    )
    start_time = models.TimeField(
        help_text='Event start time'
    )
    end_time = models.TimeField(
        help_text='Event end time'
    )
    location = models.CharField(
        max_length=300,
        help_text='Event venue/location'
    )
    max_volunteers = models.PositiveIntegerField(
        default=50,
        help_text='Maximum number of volunteers needed'
    )

    # --- Status ---
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='upcoming',
        help_text='Current status of the event'
    )

    # --- Image ---
    image = models.ImageField(
        upload_to='events/',
        blank=True,
        null=True,
        help_text='Event banner/image'
    )

    # --- Created By ---
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_events',
        help_text='Admin who created the event'
    )

    # --- Timestamps ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} ({self.date})"

    @property
    def assigned_count(self):
        """Number of volunteers assigned to this event."""
        return self.assignments.count()

    @property
    def is_full(self):
        """Check if the event has reached maximum volunteers."""
        return self.assigned_count >= self.max_volunteers

    @property
    def attendance_count(self):
        """Number of volunteers who attended this event."""
        return self.attendances.filter(status='present').count()

    @property
    def interested_count(self):
        """Number of volunteers who expressed active interest in this event."""
        return self.interests.filter(is_cancelled=False).count()

    def get_interested_volunteers(self):
        """Return queryset of active (non-cancelled) EventInterest records."""
        return self.interests.filter(is_cancelled=False).select_related('volunteer__user')  # uses Event.interests reverse relation

    @property
    def is_open_for_interest(self):
        """Whether volunteers can currently express interest."""
        return self.status in ('upcoming', 'open_for_interest')


class VolunteerAssignment(models.Model):
    """
    Represents the assignment of a volunteer to an event.
    This is a many-to-many relationship with extra data (status, dates).
    """

    STATUS_CHOICES = (
        ('assigned', 'Assigned'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    # --- Relationships ---
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='assignments',
        help_text='The event this assignment is for'
    )
    volunteer = models.ForeignKey(
        'volunteers.VolunteerProfile',
        on_delete=models.CASCADE,
        related_name='assignments',
        help_text='The volunteer assigned to this event'
    )

    # --- Assignment Details ---
    assigned_date = models.DateTimeField(
        auto_now_add=True,
        help_text='When the volunteer was assigned'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='assigned',
    )

    class Meta:
        verbose_name = 'Volunteer Assignment'
        verbose_name_plural = 'Volunteer Assignments'
        # Prevent duplicate assignments
        unique_together = ('event', 'volunteer')
        ordering = ['-assigned_date']

    def __str__(self):
        return f"{self.volunteer.full_name} → {self.event.title}"


class EventInterest(models.Model):
    """
    Tracks a volunteer's expressed interest in an event.

    A volunteer can express interest only once per event (unique_together).
    They may cancel before the admin assigns them.
    Admins use this list to pick who to formally assign.
    """

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='interests',
        help_text='The event the volunteer is interested in'
    )
    volunteer = models.ForeignKey(
        'volunteers.VolunteerProfile',
        on_delete=models.CASCADE,
        related_name='event_interests',
        help_text='The volunteer who expressed interest'
    )
    submitted_at = models.DateTimeField(
        auto_now_add=True,
        help_text='When the volunteer expressed interest'
    )
    is_cancelled = models.BooleanField(
        default=False,
        help_text='True if the volunteer cancelled their interest'
    )
    cancelled_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text='When the volunteer cancelled their interest'
    )

    class Meta:
        verbose_name = 'Event Interest'
        verbose_name_plural = 'Event Interests'
        unique_together = ('event', 'volunteer')
        ordering = ['-submitted_at']

    def __str__(self):
        status = 'Cancelled' if self.is_cancelled else 'Interested'
        return f"{self.volunteer.full_name} → {self.event.title} [{status}]"

    @property
    def is_active(self):
        """Interest is active (not cancelled)."""
        return not self.is_cancelled


class Attendance(models.Model):
    """
    Tracks volunteer attendance for events.
    Records check-in/check-out times and attendance status.
    """

    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    )

    # --- Relationships ---
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='attendances',
        help_text='The event this attendance record is for'
    )
    volunteer = models.ForeignKey(
        'volunteers.VolunteerProfile',
        on_delete=models.CASCADE,
        related_name='attendances',
        help_text='The volunteer this attendance record belongs to'
    )

    # --- Attendance Details ---
    check_in = models.DateTimeField(
        blank=True,
        null=True,
        help_text='When the volunteer checked in'
    )
    check_out = models.DateTimeField(
        blank=True,
        null=True,
        help_text='When the volunteer checked out'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='absent',
    )

    # --- Timestamps ---
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Attendance Record'
        verbose_name_plural = 'Attendance Records'
        unique_together = ('event', 'volunteer')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.volunteer.full_name} - {self.event.title} ({self.get_status_display()})"


class Notification(models.Model):
    """
    In-app notification for volunteers.

    Created when a volunteer is assigned to an event, when their
    application status changes, or for any admin broadcast.
    Displayed on the volunteer dashboard with an unread badge.
    """

    TYPE_CHOICES = (
        ('assignment', 'Event Assignment'),
        ('interest_cancelled', 'Interest Cancelled by Admin'),
        ('general', 'General Announcement'),
    )

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text='The user receiving this notification'
    )
    notification_type = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES,
        default='general',
    )
    title = models.CharField(
        max_length=200,
        help_text='Short notification title'
    )
    message = models.TextField(
        help_text='Full notification message'
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications',
        help_text='Related event (if applicable)'
    )
    is_read = models.BooleanField(
        default=False,
        help_text='Whether the recipient has read this notification'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_notification_type_display()}] → {self.recipient.get_full_name()} | {self.title}"
