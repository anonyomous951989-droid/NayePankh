"""
==============================================================
NayePankh Foundation - Event Views
==============================================================
Views for event CRUD, volunteer interest expression,
admin assignment from interested pool, and attendance tracking.
==============================================================
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Event, VolunteerAssignment, Attendance, EventInterest, Notification
from .forms import EventForm
from volunteers.models import VolunteerProfile


# ==============================================================
# PUBLIC / SHARED VIEWS
# ==============================================================

def event_list(request):
    """
    Display a paginated list of events.
    Supports search by title and location, and filter by status.
    """
    events = Event.objects.all()

    # --- Search ---
    search_query = request.GET.get('search', '')
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # --- Filter by status ---
    status_filter = request.GET.get('status', '')
    if status_filter:
        events = events.filter(status=status_filter)

    # --- Pagination (6 events per page) ---
    paginator = Paginator(events, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # For authenticated volunteers: determine which events they already expressed interest in
    user_interests = set()
    if request.user.is_authenticated and hasattr(request.user, 'volunteer_profile'):
        try:
            profile = request.user.volunteer_profile
            user_interests = set(
                EventInterest.objects.filter(
                    volunteer=profile, is_cancelled=False
                ).values_list('event_id', flat=True)
            )
        except Exception:
            pass

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'user_interests': user_interests,
        'status_choices': Event.STATUS_CHOICES,
    }
    return render(request, 'events/event_list.html', context)


def event_detail(request, pk):
    """Display detailed information about a specific event."""
    event = get_object_or_404(Event, pk=pk)
    assignments = event.assignments.select_related('volunteer__user')
    attendances = event.attendances.select_related('volunteer__user')

    # Check if the logged-in volunteer has already expressed interest
    user_interest = None
    volunteer_profile = None
    if request.user.is_authenticated and hasattr(request.user, 'volunteer_profile'):
        try:
            volunteer_profile = request.user.volunteer_profile
            user_interest = EventInterest.objects.filter(
                event=event, volunteer=volunteer_profile
            ).first()
        except Exception:
            pass

    context = {
        'event': event,
        'assignments': assignments,
        'attendances': attendances,
        'user_interest': user_interest,
        'volunteer_profile': volunteer_profile,
        'interested_count': event.interested_count,
    }
    return render(request, 'events/event_detail.html', context)


# ==============================================================
# ADMIN-ONLY CRUD VIEWS
# ==============================================================

@login_required
def create_event(request):
    """Create a new event (admin only)."""
    if not request.user.is_staff and not request.user.is_admin_user:
        messages.error(request, 'You do not have permission to create events.')
        return redirect('events:list')

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, f'Event "{event.title}" created successfully!')
            return redirect('events:detail', pk=event.pk)
    else:
        form = EventForm()

    return render(request, 'events/event_form.html', {
        'form': form,
        'title': 'Create Event',
    })


@login_required
def update_event(request, pk):
    """Update an existing event (admin only)."""
    if not request.user.is_staff and not request.user.is_admin_user:
        messages.error(request, 'You do not have permission to update events.')
        return redirect('events:list')

    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, f'Event "{event.title}" updated successfully!')
            return redirect('events:detail', pk=event.pk)
    else:
        form = EventForm(instance=event)

    return render(request, 'events/event_form.html', {
        'form': form,
        'title': 'Update Event',
        'event': event,
    })


@login_required
def delete_event(request, pk):
    """Delete an event (admin only)."""
    if not request.user.is_staff and not request.user.is_admin_user:
        messages.error(request, 'You do not have permission to delete events.')
        return redirect('events:list')

    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        title = event.title
        event.delete()
        messages.success(request, f'Event "{title}" deleted successfully!')
        return redirect('events:list')

    return render(request, 'events/event_confirm_delete.html', {'event': event})


# ==============================================================
# VOLUNTEER INTEREST VIEWS
# ==============================================================

@login_required
@require_POST
def express_interest(request, pk):
    """
    Volunteer expresses interest in an event.
    - Requires approved volunteer profile.
    - One interest per volunteer per event (enforced by unique_together).
    - If previously cancelled, reactivates the interest.
    Returns JSON for AJAX or redirects for standard POST.
    """
    event = get_object_or_404(Event, pk=pk)

    # Must be an approved volunteer
    if not hasattr(request.user, 'volunteer_profile'):
        messages.error(request, 'You need to complete your volunteer registration first.')
        return redirect('volunteers:register')

    volunteer_profile = request.user.volunteer_profile
    if volunteer_profile.status != 'approved':
        messages.warning(request, 'Only approved volunteers can express interest in events.')
        return redirect('events:detail', pk=pk)

    # Check event accepts interest
    if not event.is_open_for_interest:
        messages.warning(request, 'This event is not currently open for volunteer interest.')
        return redirect('events:detail', pk=pk)

    # Create or reactivate interest
    interest, created = EventInterest.objects.get_or_create(
        event=event,
        volunteer=volunteer_profile,
        defaults={'is_cancelled': False}
    )

    if not created:
        if interest.is_cancelled:
            # Reactivate cancelled interest
            interest.is_cancelled = False
            interest.cancelled_at = None
            interest.save()
            msg = f'Your interest in "{event.title}" has been resubmitted!'
            messages.success(request, msg)
        else:
            messages.info(request, 'You have already expressed interest in this event.')
    else:
        messages.success(request, f'Your interest in "{event.title}" has been saved! The admin will review and assign volunteers soon.')

    # AJAX support
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok', 'message': 'Interest submitted'})

    return redirect('events:detail', pk=pk)


@login_required
@require_POST
def cancel_interest(request, pk):
    """
    Volunteer cancels their expressed interest before assignment.
    Only allowed if the volunteer has not yet been formally assigned.
    """
    event = get_object_or_404(Event, pk=pk)

    if not hasattr(request.user, 'volunteer_profile'):
        messages.error(request, 'Volunteer profile not found.')
        return redirect('events:detail', pk=pk)

    volunteer_profile = request.user.volunteer_profile

    # Check they haven't already been assigned
    already_assigned = VolunteerAssignment.objects.filter(
        event=event, volunteer=volunteer_profile
    ).exists()
    if already_assigned:
        messages.warning(request, 'You have already been assigned to this event and cannot cancel interest.')
        return redirect('events:detail', pk=pk)

    interest = get_object_or_404(EventInterest, event=event, volunteer=volunteer_profile)

    if interest.is_cancelled:
        messages.info(request, 'Your interest was already cancelled.')
    else:
        interest.is_cancelled = True
        interest.cancelled_at = timezone.now()
        interest.save()
        messages.success(request, f'Your interest in "{event.title}" has been cancelled.')

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok', 'message': 'Interest cancelled'})

    return redirect('events:detail', pk=pk)


# ==============================================================
# ADMIN INTEREST & ASSIGNMENT VIEWS
# ==============================================================

@login_required
def event_interest_list(request, pk):
    """
    Admin view: list all volunteers who expressed interest in an event.
    Shows Name, Email, Phone, Skills, Interest Date, and whether assigned.
    """
    if not request.user.is_staff and not request.user.is_admin_user:
        messages.error(request, 'Access denied.')
        return redirect('events:list')

    event = get_object_or_404(Event, pk=pk)
    interests = event.get_interested_volunteers()

    # Tag interests as already assigned or not
    assigned_vol_ids = set(
        event.assignments.values_list('volunteer_id', flat=True)
    )
    interests_with_status = []
    for interest in interests:
        interests_with_status.append({
            'interest': interest,
            'volunteer': interest.volunteer,
            'is_assigned': interest.volunteer.id in assigned_vol_ids,
        })

    context = {
        'event': event,
        'interests_with_status': interests_with_status,
        'total_interested': event.interested_count,
        'total_assigned': event.assigned_count,
    }
    return render(request, 'events/event_interest_list.html', context)


@login_required
def assign_volunteers(request, pk):
    """
    Admin view: assign selected interested volunteers to the event.

    GET  → shows the list of interested (non-assigned) volunteers
    POST → creates VolunteerAssignment records for selected volunteers,
           sends in-app Notification + email to each assigned volunteer,
           updates event status to 'assigned' if any were assigned.
    """
    if not request.user.is_staff and not request.user.is_admin_user:
        messages.error(request, 'You do not have permission to assign volunteers.')
        return redirect('events:list')

    event = get_object_or_404(Event, pk=pk)

    # Volunteers already assigned (to exclude from available list)
    assigned_ids = set(event.assignments.values_list('volunteer_id', flat=True))

    # Interested volunteers who haven't been assigned yet
    interested_not_assigned = event.interests.filter(
        is_cancelled=False
    ).exclude(
        volunteer_id__in=assigned_ids
    ).select_related('volunteer__user')

    if request.method == 'POST':
        volunteer_ids = request.POST.getlist('volunteers')
        assigned_count = 0
        errors = []

        for vol_id in volunteer_ids:
            try:
                volunteer = VolunteerProfile.objects.get(id=vol_id, status='approved')
                assignment, created = VolunteerAssignment.objects.get_or_create(
                    event=event,
                    volunteer=volunteer,
                )
                if created:
                    assigned_count += 1

                    # --- In-app Notification ---
                    Notification.objects.create(
                        recipient=volunteer.user,
                        notification_type='assignment',
                        title=f'You have been assigned to "{event.title}"!',
                        message=(
                            f'Congratulations! You have been officially assigned to the event '
                            f'"{event.title}" scheduled on {event.date.strftime("%B %d, %Y")} '
                            f'at {event.location}. Please be ready on time!'
                        ),
                        event=event,
                    )

                    # --- Email Notification ---
                    try:
                        from accounts.utils import send_assignment_notification_email
                        send_assignment_notification_email(volunteer.user, event)
                    except Exception as email_err:
                        print(f"[Email Error] Could not send assignment email to {volunteer.user.email}: {email_err}")

            except VolunteerProfile.DoesNotExist:
                errors.append(vol_id)
            except Exception as e:
                errors.append(str(e))

        # Update event status to 'assigned' once volunteers are assigned
        if assigned_count > 0 and event.status in ('upcoming', 'open_for_interest'):
            event.status = 'assigned'
            event.save()

        messages.success(request, f'{assigned_count} volunteer(s) assigned to "{event.title}".')
        if errors:
            messages.warning(request, f'Could not assign {len(errors)} volunteer(s).')
        return redirect('events:detail', pk=event.pk)

    context = {
        'event': event,
        'interested_not_assigned': interested_not_assigned,
        'current_assignments': event.assignments.select_related('volunteer__user'),
        'total_interested': event.interested_count,
    }
    return render(request, 'events/assign_volunteers.html', context)


# ==============================================================
# ATTENDANCE
# ==============================================================

@login_required
def mark_attendance(request, pk):
    """Mark attendance for an event (admin only)."""
    if not request.user.is_staff and not request.user.is_admin_user:
        messages.error(request, 'You do not have permission to mark attendance.')
        return redirect('events:list')

    event = get_object_or_404(Event, pk=pk)
    assignments = event.assignments.select_related('volunteer__user')

    if request.method == 'POST':
        for assignment in assignments:
            status = request.POST.get(f'status_{assignment.volunteer.id}', 'absent')
            attendance, created = Attendance.objects.get_or_create(
                event=event,
                volunteer=assignment.volunteer,
                defaults={'status': status}
            )
            if not created:
                attendance.status = status
                attendance.save()

            # Set check-in time if present
            if status == 'present' and not attendance.check_in:
                attendance.check_in = timezone.now()
                attendance.save()

        messages.success(request, f'Attendance marked for "{event.title}".')
        return redirect('events:detail', pk=event.pk)

    # Get existing attendance records
    existing_attendance = {}
    for att in event.attendances.all():
        existing_attendance[att.volunteer.id] = att.status

    context = {
        'event': event,
        'assignments': assignments,
        'existing_attendance': existing_attendance,
    }
    return render(request, 'events/attendance.html', context)
