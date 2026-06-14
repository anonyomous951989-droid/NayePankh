"""
==============================================================
NayePankh Foundation - Volunteer Models
==============================================================
Defines the VolunteerProfile model which stores all information
about a volunteer's registration, skills, and status.
==============================================================
"""

import uuid
from django.db import models
from django.conf import settings


class VolunteerProfile(models.Model):
    """
    Stores detailed profile information for each volunteer.

    Linked to the User model via a OneToOneField, meaning each user
    can have exactly one volunteer profile.

    For beginners: This model stores all the extra information that
    doesn't belong in the User model (like phone, address, skills, etc.)
    """

    # --- Status Choices ---
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    # --- Gender Choices ---
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer Not to Say'),
    )

    # --- Availability Choices ---
    AVAILABILITY_CHOICES = (
        ('weekdays', 'Weekdays'),
        ('weekends', 'Weekends'),
        ('both', 'Both Weekdays & Weekends'),
        ('flexible', 'Flexible'),
    )

    # --- Link to User model ---
    # OneToOneField means each User has exactly one VolunteerProfile
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # Delete profile if user is deleted
        related_name='volunteer_profile',
        help_text='The user account linked to this volunteer profile'
    )

    # --- Personal Information ---
    phone = models.CharField(
        max_length=15,
        help_text='Contact phone number'
    )
    date_of_birth = models.DateField(
        help_text='Date of birth (YYYY-MM-DD)'
    )
    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        help_text='Gender identity'
    )

    # --- Address ---
    address = models.TextField(
        help_text='Full street address'
    )
    city = models.CharField(
        max_length=100,
        help_text='City of residence'
    )
    state = models.CharField(
        max_length=100,
        help_text='State/Province'
    )

    # --- Education & Skills ---
    education = models.CharField(
        max_length=200,
        help_text='Highest educational qualification'
    )
    skills = models.TextField(
        help_text='List your skills (e.g., Teaching, First Aid, Social Media)'
    )
    interests = models.TextField(
        help_text='Areas of interest (e.g., Education, Healthcare, Environment)'
    )

    # --- Availability ---
    availability = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default='flexible',
        help_text='When are you available to volunteer?'
    )

    # --- File Uploads ---
    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True,
        help_text='Upload your resume (PDF, DOC, DOCX)'
    )
    photo = models.ImageField(
        upload_to='photos/',
        blank=True,
        null=True,
        help_text='Upload a profile photo'
    )

    # --- Application Status ---
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text='Current application status'
    )
    rejection_reason = models.TextField(
        blank=True,
        null=True,
        help_text='Reason for rejection (if applicable)'
    )

    # --- Volunteer ID ---
    volunteer_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        help_text='Unique volunteer ID (auto-generated upon approval)'
    )

    # --- Timestamps ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Volunteer Profile'
        verbose_name_plural = 'Volunteer Profiles'
        ordering = ['-created_at']

    def __str__(self):
        """String representation: shows the user's full name and status."""
        return f"{self.user.get_full_name()} - {self.get_status_display()}"

    def generate_volunteer_id(self):
        """
        Generate a unique volunteer ID when application is approved.
        Format: NP-XXXX (e.g., NP-0001, NP-0042)
        """
        if not self.volunteer_id:
            # Get the count of approved volunteers + 1
            count = VolunteerProfile.objects.filter(
                volunteer_id__isnull=False
            ).count() + 1
            self.volunteer_id = f"NP-{count:04d}"
            self.save()
        return self.volunteer_id

    @property
    def full_name(self):
        """Get the volunteer's full name from the linked user."""
        return self.user.get_full_name()

    @property
    def email(self):
        """Get the volunteer's email from the linked user."""
        return self.user.email
