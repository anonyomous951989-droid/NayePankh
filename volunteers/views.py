"""
==============================================================
NayePankh Foundation - Volunteer Views
==============================================================
Views for volunteer registration, profile viewing/editing,
and volunteer ID card download.
==============================================================
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template

from .models import VolunteerProfile
from .forms import VolunteerRegistrationForm, VolunteerEditForm
from accounts.utils import send_registration_confirmation_email


@login_required
def register_volunteer(request):
    """
    Handle volunteer registration form.
    Only allows users who don't already have a profile.
    """
    # Check if user already has a volunteer profile
    if hasattr(request.user, 'volunteer_profile'):
        messages.info(request, 'You have already registered as a volunteer.')
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = VolunteerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the profile but link it to the current user
            profile = form.save(commit=False)
            profile.user = request.user
            profile.status = 'pending'  # All new registrations start as pending
            profile.save()

            # Send confirmation email
            send_registration_confirmation_email(request.user)

            messages.success(
                request,
                'Your volunteer registration has been submitted! '
                'You will receive an email once your application is reviewed.'
            )
            return redirect('dashboard:home')
    else:
        form = VolunteerRegistrationForm()

    return render(request, 'volunteers/register.html', {'form': form})


@login_required
def view_profile(request):
    """Display the volunteer's profile information."""
    profile = get_object_or_404(VolunteerProfile, user=request.user)
    return render(request, 'volunteers/profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    """Allow volunteers to update their profile information."""
    profile = get_object_or_404(VolunteerProfile, user=request.user)

    if request.method == 'POST':
        form = VolunteerEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('volunteers:profile')
    else:
        form = VolunteerEditForm(instance=profile)

    return render(request, 'volunteers/edit_profile.html', {
        'form': form,
        'profile': profile,
    })


@login_required
def download_volunteer_id(request):
    """
    Generate and download a volunteer ID card as PDF.
    Only available for approved volunteers.
    """
    profile = get_object_or_404(VolunteerProfile, user=request.user)
    print(profile.status)
    if profile.status != 'approved':
        messages.warning(request, 'Your volunteer ID will be available after your application is approved.')
        return redirect('dashboard:home')

    # Ensure volunteer has an ID
    if not profile.volunteer_id:
        profile.generate_volunteer_id()

    # Generate PDF using ReportLab
    try:
        from reportlab.lib.pagesizes import letter, landscape
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        from reportlab.pdfgen import canvas
        from reportlab.lib.utils import ImageReader
        import io
        import os
        from django.conf import settings

        # Create the PDF in memory
        buffer = io.BytesIO()

        # Use a card-sized canvas (3.375 x 2.125 inches, standard ID card)
        card_width = 3.375 * inch
        card_height = 2.125 * inch
        c = canvas.Canvas(buffer, pagesize=(card_width, card_height))

        # --- Card Background ---
        # Gradient effect using rectangles
        c.setFillColor(colors.HexColor('#1a1a2e'))
        c.rect(0, 0, card_width, card_height, fill=True)

        # Header bar
        c.setFillColor(colors.HexColor('#e94560'))
        c.rect(0, card_height - 0.5 * inch, card_width, 0.5 * inch, fill=True)

        # --- Header Text ---
        c.setFillColor(colors.white)
        c.setFont('Helvetica-Bold', 10)
        c.drawCentredString(card_width / 2, card_height - 0.35 * inch, 'NAYEPANKH FOUNDATION')

        # --- Volunteer Info ---
        c.setFillColor(colors.white)
        c.setFont('Helvetica-Bold', 9)
        y_pos = card_height - 0.75 * inch
        c.drawString(0.2 * inch, y_pos, f'Name: {profile.full_name}')

        c.setFont('Helvetica', 8)
        y_pos -= 0.2 * inch
        c.drawString(0.2 * inch, y_pos, f'ID: {profile.volunteer_id}')

        y_pos -= 0.2 * inch
        c.drawString(0.2 * inch, y_pos, f'Email: {profile.user.email}')

        y_pos -= 0.2 * inch
        c.drawString(0.2 * inch, y_pos, f'Phone: {profile.phone}')

        y_pos -= 0.2 * inch
        c.drawString(0.2 * inch, y_pos, f'City: {profile.city}, {profile.state}')

        # --- Footer ---
        c.setFillColor(colors.HexColor('#e94560'))
        c.rect(0, 0, card_width, 0.25 * inch, fill=True)
        c.setFillColor(colors.white)
        c.setFont('Helvetica', 6)
        c.drawCentredString(card_width / 2, 0.08 * inch, 'Official Volunteer Identification Card')

        c.save()

        # Get the PDF data
        buffer.seek(0)
        pdf_data = buffer.getvalue()
        buffer.close()

        # Return as downloadable file
        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="VolunteerID_{profile.volunteer_id}.pdf"'
        return response

    except ImportError:
        messages.error(request, 'PDF generation is not available. Please install reportlab.')
        return redirect('dashboard:home')
