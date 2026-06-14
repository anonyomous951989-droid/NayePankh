"""
==============================================================
NayePankh Foundation - Accounts Views
==============================================================
Views for user authentication: signup, login, logout, email
verification, and password reset.

For beginners: Views are Python functions (or classes) that handle
HTTP requests and return HTTP responses (usually HTML pages).
==============================================================
"""

import uuid
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from .forms import SignupForm, LoginForm
from .models import User
from .utils import send_verification_email


def signup_view(request):
    """
    Handle user registration.
    - GET: Display the signup form
    - POST: Process the form, create user, send verification email
    """
    # Redirect logged-in users to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Save the user but don't commit yet (we need to set extra fields)
            user = form.save(commit=False)
            user.is_active = True  # User can log in but email isn't verified yet
            user.role = 'volunteer'
            user.save()

            # Send verification email
            send_verification_email(user, request)

            messages.success(
                request,
                'Account created successfully! Please check your email to verify your account.'
            )
            return redirect('accounts:login')
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    """
    Handle user login.
    - GET: Display the login form
    - POST: Authenticate and log in the user
    """
    # Redirect logged-in users to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')

                # Redirect to the page they were trying to access, or dashboard
                next_url = request.GET.get('next', '')
                if next_url:
                    return redirect(next_url)
                return redirect('dashboard:home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """Log out the current user and redirect to landing page."""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('core:landing')


def verify_email_view(request, token):
    """
    Verify a user's email address using the token sent via email.
    The token is a UUID that was generated when the user signed up.
    """
    try:
        user = User.objects.get(verification_token=token)
        if not user.email_verified:
            user.email_verified = True
            # Generate a new token so the old one can't be reused
            user.verification_token = uuid.uuid4()
            user.save()
            messages.success(request, 'Email verified successfully! You can now log in.')
        else:
            messages.info(request, 'Your email is already verified.')
    except User.DoesNotExist:
        messages.error(request, 'Invalid verification link.')

    return redirect('accounts:login')


def password_reset_view(request):
    """
    Handle password reset request.
    - GET: Display the password reset form
    - POST: Send password reset email
    """
    if request.method == 'POST':
        email = request.POST.get('email', '')
        try:
            user = User.objects.get(email=email)
            # Generate a new verification token for password reset
            user.verification_token = uuid.uuid4()
            user.save()

            # Build reset URL
            reset_url = f"{request.scheme}://{request.get_host()}/accounts/password-reset-confirm/{user.verification_token}/"

            from django.core.mail import send_mail
            from django.conf import settings

            send_mail(
                subject='Password Reset - NayePankh Foundation',
                message=f'Click the link to reset your password: {reset_url}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            messages.success(request, 'Password reset link sent to your email.')
        except User.DoesNotExist:
            # Don't reveal whether the email exists (security best practice)
            messages.success(request, 'If an account with that email exists, a reset link has been sent.')

        return redirect('accounts:login')

    return render(request, 'accounts/password_reset.html')


def password_reset_confirm_view(request, token):
    """
    Handle setting a new password after clicking the reset link.
    - GET: Display the new password form
    - POST: Update the user's password
    """
    try:
        user = User.objects.get(verification_token=token)
    except User.DoesNotExist:
        messages.error(request, 'Invalid or expired reset link.')
        return redirect('accounts:login')

    if request.method == 'POST':
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if password1 and password1 == password2:
            if len(password1) >= 8:
                user.set_password(password1)
                # Regenerate token so the link can't be reused
                user.verification_token = uuid.uuid4()
                user.save()
                messages.success(request, 'Password reset successfully! You can now log in.')
                return redirect('accounts:login')
            else:
                messages.error(request, 'Password must be at least 8 characters long.')
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'accounts/password_reset_confirm.html', {'token': token})
