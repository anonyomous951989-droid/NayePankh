"""
==============================================================
NayePankh Foundation - Root URL Configuration
==============================================================
This is the main URL routing file. It maps URL patterns to the
appropriate app's URL configurations.

For beginners: When a user visits a URL, Django checks this file
first to figure out which app should handle the request.
==============================================================
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # --- Django Admin Panel ---
    # Access at: /admin/
    path('admin/', admin.site.urls),

    # --- Core App (Landing Page, Contact) ---
    # Access at: / (root URL)
    path('', include('core.urls', namespace='core')),

    # --- Accounts App (Login, Signup, Password Reset) ---
    # Access at: /accounts/
    path('accounts/', include('accounts.urls', namespace='accounts')),

    # --- Volunteers App (Registration, Profile) ---
    # Access at: /volunteers/
    path('volunteers/', include('volunteers.urls', namespace='volunteers')),

    # --- Events App (Event Management) ---
    # Access at: /events/
    path('events/', include('events.urls', namespace='events')),

    # --- Dashboard App (Volunteer & Admin Dashboards) ---
    # Access at: /dashboard/
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),

    # --- Reports App (Reports & Data Export) ---
    # Access at: /reports/
    path('reports/', include('reports.urls', namespace='reports')),

    # --- REST API Endpoints ---
    # Access at: /api/
    path('api/', include('api.urls', namespace='api')),
]

# ==============================================================
# Serve media files during development
# ==============================================================
# In production, your web server (Nginx/Apache) should serve media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# ==============================================================
# Custom Error Handlers
# ==============================================================
handler404 = 'core.views.error_404_view'
handler500 = 'core.views.error_500_view'

# ==============================================================
# Admin Site Customization
# ==============================================================
admin.site.site_header = 'NayePankh Foundation Admin'
admin.site.site_title = 'NayePankh Foundation'
admin.site.index_title = 'Volunteer Management System'
