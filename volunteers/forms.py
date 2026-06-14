"""
==============================================================
NayePankh Foundation - Volunteer Forms
==============================================================
Forms for volunteer registration and profile editing.
These forms include file upload handling and custom validation.
==============================================================
"""

from django import forms
from .models import VolunteerProfile


class VolunteerRegistrationForm(forms.ModelForm):
    """
    Form for volunteer registration with all profile fields.
    Uses ModelForm to automatically generate fields from the model.
    """

    class Meta:
        model = VolunteerProfile
        fields = [
            'phone', 'date_of_birth', 'gender', 'address',
            'city', 'state', 'education', 'skills', 'interests',
            'availability', 'resume', 'photo',
        ]
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., +91 9876543210',
                'id': 'reg-phone',
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'reg-dob',
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select',
                'id': 'reg-gender',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your full address',
                'id': 'reg-address',
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., New Delhi',
                'id': 'reg-city',
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Delhi',
                'id': 'reg-state',
            }),
            'education': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., B.Tech in Computer Science',
                'id': 'reg-education',
            }),
            'skills': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'e.g., Teaching, Public Speaking, First Aid',
                'id': 'reg-skills',
            }),
            'interests': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'e.g., Education, Healthcare, Environment',
                'id': 'reg-interests',
            }),
            'availability': forms.Select(attrs={
                'class': 'form-select',
                'id': 'reg-availability',
            }),
            'resume': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx',
                'id': 'reg-resume',
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'id': 'reg-photo',
            }),
        }

    def clean_phone(self):
        """Validate phone number format."""
        phone = self.cleaned_data.get('phone')
        # Remove spaces and dashes for validation
        cleaned = phone.replace(' ', '').replace('-', '').replace('+', '')
        if not cleaned.isdigit():
            raise forms.ValidationError('Phone number should contain only digits.')
        if len(cleaned) < 10 or len(cleaned) > 13:
            raise forms.ValidationError('Phone number should be 10-13 digits.')
        return phone

    def clean_resume(self):
        """Validate resume file type and size."""
        resume = self.cleaned_data.get('resume')
        if resume:
            # Check file size (max 5 MB)
            if resume.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Resume file must be less than 5 MB.')
            # Check file type
            allowed_types = ['application/pdf', 'application/msword',
                             'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
            if resume.content_type not in allowed_types:
                raise forms.ValidationError('Only PDF, DOC, and DOCX files are allowed.')
        return resume

    def clean_photo(self):
        """Validate photo file type and size."""
        photo = self.cleaned_data.get('photo')
        if photo:
            # Check file size (max 2 MB)
            if photo.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Photo must be less than 2 MB.')
        return photo


class VolunteerEditForm(forms.ModelForm):
    """
    Form for editing an existing volunteer profile.
    Only allows editing certain fields (not status or volunteer_id).
    """

    class Meta:
        model = VolunteerProfile
        fields = [
            'phone', 'address', 'city', 'state',
            'education', 'skills', 'interests',
            'availability', 'resume', 'photo',
        ]
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'edit-phone',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'id': 'edit-address',
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'edit-city',
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'edit-state',
            }),
            'education': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'edit-education',
            }),
            'skills': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'id': 'edit-skills',
            }),
            'interests': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'id': 'edit-interests',
            }),
            'availability': forms.Select(attrs={
                'class': 'form-select',
                'id': 'edit-availability',
            }),
            'resume': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx',
                'id': 'edit-resume',
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'id': 'edit-photo',
            }),
        }
