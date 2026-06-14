"""
NayePankh Foundation - Event URL Patterns
"""

from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # --- Event CRUD ---
    path('', views.event_list, name='list'),
    path('<int:pk>/', views.event_detail, name='detail'),
    path('create/', views.create_event, name='create'),
    path('<int:pk>/update/', views.update_event, name='update'),
    path('<int:pk>/delete/', views.delete_event, name='delete'),

    # --- Volunteer Interest ---
    path('<int:pk>/interest/', views.express_interest, name='express_interest'),
    path('<int:pk>/cancel-interest/', views.cancel_interest, name='cancel_interest'),
    path('<int:pk>/interested-volunteers/', views.event_interest_list, name='interest_list'),

    # --- Assignment & Attendance ---
    path('<int:pk>/assign/', views.assign_volunteers, name='assign'),
    path('<int:pk>/attendance/', views.mark_attendance, name='attendance'),
]
