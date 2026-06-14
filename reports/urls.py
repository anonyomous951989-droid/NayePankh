"""
NayePankh Foundation - Reports URL Patterns
"""

from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports_home, name='home'),
    path('volunteers/', views.volunteer_report, name='volunteer_report'),
    path('events/', views.event_report, name='event_report'),
    path('attendance/', views.attendance_report, name='attendance_report'),
    path('monthly/', views.monthly_statistics, name='monthly_stats'),
    path('export/<str:report_type>/', views.export_report_excel, name='export_report'),
]
