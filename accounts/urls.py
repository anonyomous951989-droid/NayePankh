"""
==============================================================
NayePankh Foundation - Accounts URL Patterns
==============================================================
Maps URLs to views for authentication features.
==============================================================
"""

from django.urls import path
from . import views

# Namespace for URL reversing (e.g., 'accounts:login')
app_name = 'accounts'

urlpatterns = [
    # --- Authentication ---
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # --- Email Verification ---
    path('verify/<uuid:token>/', views.verify_email_view, name='verify_email'),

    # --- Password Reset ---
    path('password-reset/', views.password_reset_view, name='password_reset'),
    path('password-reset-confirm/<uuid:token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
]
