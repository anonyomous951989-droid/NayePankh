"""
NayePankh Foundation - Core URL Patterns
"""

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('contact/', views.contact_submit, name='contact'),
]
