"""
==============================================================
NayePankh Foundation - API Views
==============================================================
REST API endpoints for volunteer data, events, and statistics.
Uses Django REST Framework's generic views and viewsets.
==============================================================
"""

from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from volunteers.models import VolunteerProfile
from events.models import Event, Attendance
from .serializers import (
    VolunteerProfileSerializer,
    EventSerializer,
    AttendanceSerializer,
    DashboardStatsSerializer,
)


class VolunteerListAPI(generics.ListAPIView):
    """
    GET /api/volunteers/
    List all volunteer profiles with search and filter support.
    """
    queryset = VolunteerProfile.objects.select_related('user').all()
    serializer_class = VolunteerProfileSerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ['status', 'city', 'gender', 'availability']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'skills']
    ordering_fields = ['created_at', 'city']


class VolunteerDetailAPI(generics.RetrieveAPIView):
    """
    GET /api/volunteers/<id>/
    Retrieve a specific volunteer's profile.
    """
    queryset = VolunteerProfile.objects.select_related('user').all()
    serializer_class = VolunteerProfileSerializer
    permission_classes = [permissions.IsAdminUser]


class EventListAPI(generics.ListAPIView):
    """
    GET /api/events/
    List all events with filtering.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ['status']
    search_fields = ['title', 'location']
    ordering_fields = ['date', 'created_at']


class EventDetailAPI(generics.RetrieveAPIView):
    """
    GET /api/events/<id>/
    Retrieve a specific event's details.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def dashboard_stats_api(request):
    """
    GET /api/stats/
    Return dashboard statistics as JSON.
    """
    data = {
        'total_volunteers': VolunteerProfile.objects.count(),
        'approved_volunteers': VolunteerProfile.objects.filter(status='approved').count(),
        'pending_applications': VolunteerProfile.objects.filter(status='pending').count(),
        'active_events': Event.objects.filter(status__in=['upcoming', 'ongoing']).count(),
        'total_events': Event.objects.count(),
    }
    serializer = DashboardStatsSerializer(data)
    return Response(serializer.data)
