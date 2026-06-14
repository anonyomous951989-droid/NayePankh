"""
==============================================================
NayePankh Foundation - Accounts Forms
==============================================================
Forms for user signup, login, and password management.
Django forms handle HTML form rendering, validation, and data cleaning.
==============================================================
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from .models import User


class SignupForm(UserCreationForm):
    """
    Registration form for new users.
    Extends Django's UserCreationForm which handles password hashing
    and validation automatically.
    """
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name',
            'id': 'signup-first-name',
        })
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name',
            'id': 'signup-last-name',
        })
    )
    username = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'id': 'signup-username',
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address',
            'id': 'signup-email',
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create Password',
            'id': 'signup-password1',
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
            'id': 'signup-password2',
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean_email(self):
        """Ensure email is unique across all users."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email


class LoginForm(AuthenticationForm):
    """
    Login form with Bootstrap-styled widgets.
    Extends Django's AuthenticationForm which handles authentication.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username or Email',
            'id': 'login-username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-password',
        })
    )


class CustomPasswordResetForm(PasswordResetForm):
    """Password reset form with Bootstrap styling."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'id': 'reset-email',
        })
    )


class CustomSetPasswordForm(SetPasswordForm):
    """Set new password form with Bootstrap styling."""
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New Password',
            'id': 'new-password1',
        })
    )
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm New Password',
            'id': 'new-password2',
        })
    )
