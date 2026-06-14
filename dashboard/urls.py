"""
NayePankh Foundation - Dashboard URL Patterns
"""

from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Main dashboard (routes based on role)
    path('', views.dashboard_home, name='home'),

    # Admin volunteer management
    path('volunteers/', views.admin_volunteers_list, name='admin_volunteers'),
    path('volunteers/<int:pk>/', views.admin_volunteer_detail, name='admin_volunteer_detail'),
    path('volunteers/<int:pk>/approve/', views.approve_volunteer, name='approve_volunteer'),
    path('volunteers/<int:pk>/reject/', views.reject_volunteer, name='reject_volunteer'),

    # Export
    path('export/excel/', views.export_volunteers_excel, name='export_excel'),
    path('export/pdf/', views.export_volunteers_pdf, name='export_pdf'),

    # Notifications
    path('notifications/', views.notifications_list, name='notifications'),
    path('notifications/<int:pk>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_read'),
]

