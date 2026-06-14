"""
==============================================================
NayePankh Foundation - Core Models
==============================================================
Models for the core functionality like contact messages.
==============================================================
"""

from django.db import models


class ContactMessage(models.Model):
    """
    Stores messages submitted through the contact form on the landing page.
    """
    name = models.CharField(max_length=100, help_text='Sender name')
    email = models.EmailField(help_text='Sender email address')
    subject = models.CharField(max_length=200, help_text='Message subject')
    message = models.TextField(help_text='Message content')
    is_read = models.BooleanField(default=False, help_text='Whether the message has been read')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject} ({self.created_at.strftime('%Y-%m-%d')})"
