"""
NayePankh Foundation - API URL Patterns
"""

from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('volunteers/', views.VolunteerListAPI.as_view(), name='volunteer_list'),
    path('volunteers/<int:pk>/', views.VolunteerDetailAPI.as_view(), name='volunteer_detail'),
    path('events/', views.EventListAPI.as_view(), name='event_list'),
    path('events/<int:pk>/', views.EventDetailAPI.as_view(), name='event_detail'),
    path('stats/', views.dashboard_stats_api, name='dashboard_stats'),
]
