"""
==============================================================
NayePankh Foundation - Event Forms
==============================================================
"""

from django import forms
from .models import Event, Attendance


class EventForm(forms.ModelForm):
    """Form for creating and editing events."""

    class Meta:
        model = Event
        fields = [
            'title', 'description', 'date', 'start_time', 'end_time',
            'location', 'max_volunteers', 'status', 'image',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Event Title',
                'id': 'event-title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the event...',
                'id': 'event-description',
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'event-date',
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'id': 'event-start-time',
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'id': 'event-end-time',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Event Location',
                'id': 'event-location',
            }),
            'max_volunteers': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'id': 'event-max-volunteers',
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
                'id': 'event-status',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'id': 'event-image',
            }),
        }

    def clean(self):
        """Validate that end time is after start time."""
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        if start_time and end_time and end_time <= start_time:
            raise forms.ValidationError('End time must be after start time.')
        return cleaned_data


class AttendanceForm(forms.ModelForm):
    """Form for marking attendance."""

    class Meta:
        model = Attendance
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select form-select-sm',
            }),
        }
