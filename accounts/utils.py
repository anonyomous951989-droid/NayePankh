"""
==============================================================
NayePankh Foundation - Email Utility Functions
==============================================================
Helper functions for sending emails (verification, notifications).
Uses Django's built-in email system with Gmail SMTP.
==============================================================
"""

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_verification_email(user, request):
    """
    Send an email verification link to a newly registered user.

    Args:
        user: The User instance who just signed up
        request: The HTTP request object (used to build the verification URL)
    """
    # Build the verification URL
    verification_url = f"{request.scheme}://{request.get_host()}/accounts/verify/{user.verification_token}/"

    subject = 'Verify Your Email - NayePankh Foundation'
    html_message = render_to_string('accounts/email/verification_email.html', {
        'user': user,
        'verification_url': verification_url,
    })
    plain_message = strip_tags(html_message)

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending verification email: {e}")
        return False


def send_approval_email(user):
    """
    Send notification email when a volunteer's application is approved.

    Args:
        user: The User instance whose application was approved
    """
    subject = 'Application Approved! - NayePankh Foundation'
    html_message = render_to_string('accounts/email/approval_email.html', {
        'user': user,
    })
    plain_message = strip_tags(html_message)

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending approval email: {e}")
        return False


def send_rejection_email(user, reason=''):
    """
    Send notification email when a volunteer's application is rejected.

    Args:
        user: The User instance whose application was rejected
        reason: Optional reason for rejection
    """
    subject = 'Application Update - NayePankh Foundation'
    html_message = render_to_string('accounts/email/rejection_email.html', {
        'user': user,
        'reason': reason,
    })
    plain_message = strip_tags(html_message)

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending rejection email: {e}")
        return False


def send_registration_confirmation_email(user):
    """
    Send a confirmation email after successful volunteer registration.

    Args:
        user: The User instance who just completed registration
    """
    subject = 'Registration Received - NayePankh Foundation'
    html_message = render_to_string('accounts/email/registration_confirmation.html', {
        'user': user,
    })
    plain_message = strip_tags(html_message)

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending registration confirmation: {e}")
        return False


def send_assignment_notification_email(user, event):
    """
    Send an email to a volunteer notifying them they've been assigned to an event.

    Args:
        user:  The User instance who was assigned
        event: The Event instance they were assigned to
    """
    subject = f'You\'ve Been Assigned to "{event.title}" — NayePankh Foundation'
    html_message = render_to_string('accounts/email/assignment_email.html', {
        'user': user,
        'event': event,
    })
    plain_message = strip_tags(html_message)

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending assignment email to {user.email}: {e}")
        return False
