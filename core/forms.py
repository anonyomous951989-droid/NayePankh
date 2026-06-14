"""
NayePankh Foundation - Core Forms
"""

from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Contact form with Bootstrap styling."""

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'id': 'contact-name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email',
                'id': 'contact-email',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject',
                'id': 'contact-subject',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Your Message',
                'id': 'contact-message',
            }),
        }
