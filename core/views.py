"""
==============================================================
NayePankh Foundation - Core Views
==============================================================
Views for the landing page, contact form, and error handlers.
==============================================================
"""

from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ContactForm
from events.models import Event
from volunteers.models import VolunteerProfile


def landing_page(request):
    """
    Render the main landing page with:
    - Hero section with NGO introduction
    - About Us section
    - Mission and Vision
    - Volunteer benefits
    - Upcoming events
    - Contact form
    - Statistics
    """
    # Get stats for the landing page
    stats = {
        'total_volunteers': VolunteerProfile.objects.filter(status='approved').count(),
        'total_events': Event.objects.count(),
        'upcoming_events': Event.objects.filter(status='upcoming').count(),
        'cities': VolunteerProfile.objects.filter(status='approved').values('city').distinct().count(),
    }

    # Get upcoming events (limit to 3)
    upcoming_events = Event.objects.filter(status='upcoming').order_by('date')[:3]

    # Contact form
    contact_form = ContactForm()

    context = {
        'stats': stats,
        'upcoming_events': upcoming_events,
        'contact_form': contact_form,
    }
    return render(request, 'core/landing.html', context)


def contact_submit(request):
    """Handle contact form submission."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('core:landing')
        else:
            messages.error(request, 'Please correct the errors below.')

    return redirect('core:landing')


def error_404_view(request, exception):
    """Custom 404 error page."""
    return render(request, '404.html', status=404)


def error_500_view(request):
    """Custom 500 error page."""
    return render(request, '500.html', status=500)
