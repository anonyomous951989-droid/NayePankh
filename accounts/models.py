"""
==============================================================
NayePankh Foundation - Accounts Models
==============================================================
Custom User model that extends Django's built-in AbstractUser.
This gives us full control over the User model while keeping
all of Django's authentication features.
==============================================================
"""

import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model for the NayePankh Foundation.

    Extends Django's AbstractUser to add:
    - Role-based access (volunteer or admin)
    - Email verification support
    - UUID-based verification tokens

    For beginners: AbstractUser gives us username, email, password,
    first_name, last_name, is_active, is_staff, etc. out of the box.
    We're adding extra fields on top of those.
    """

    # --- Role Choices ---
    ROLE_CHOICES = (
        ('volunteer', 'Volunteer'),
        ('admin', 'Admin'),
    )

    # --- Custom Fields ---
    # The role determines what the user can access
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='volunteer',
        help_text='Determines user permissions and dashboard access'
    )

    # Email verification fields
    email_verified = models.BooleanField(
        default=False,
        help_text='Whether the user has verified their email address'
    )
    verification_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        help_text='Unique token sent via email for verification'
    )

    # Make email required and unique
    email = models.EmailField(unique=True, help_text='Required. Must be a valid email address.')

    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self):
        """String representation of the user."""
        return f"{self.get_full_name() or self.username} ({self.role})"

    @property
    def is_volunteer(self):
        """Check if the user is a volunteer."""
        return self.role == 'volunteer'

    @property
    def is_admin_user(self):
        """Check if the user is an admin (not Django's is_staff)."""
        return self.role == 'admin'
