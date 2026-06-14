"""
==============================================================
NayePankh Foundation - Volunteer URL Patterns
==============================================================
"""

from django.urls import path
from . import views

app_name = 'volunteers'

urlpatterns = [
    path('register/', views.register_volunteer, name='register'),
    path('profile/', views.view_profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('download-id/', views.download_volunteer_id, name='download_id'),
]
