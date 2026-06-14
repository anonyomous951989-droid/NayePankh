"""
==============================================================
NayePankh Foundation - API Serializers
==============================================================
Serializers convert Django model instances to JSON and vice versa.
They also handle validation for API input data.
==============================================================
"""

from rest_framework import serializers
from accounts.models import User
from volunteers.models import VolunteerProfile
from events.models import Event, VolunteerAssignment, Attendance


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model (read-only, for nesting)."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']


class VolunteerProfileSerializer(serializers.ModelSerializer):
    """Serializer for volunteer profiles."""
    user = UserSerializer(read_only=True)
    full_name = serializers.CharField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = VolunteerProfile
        fields = [
            'id', 'user', 'full_name', 'phone', 'date_of_birth', 'gender',
            'city', 'state', 'education', 'skills', 'interests',
            'availability', 'status', 'status_display', 'volunteer_id',
            'created_at', 'updated_at',
        ]


class EventSerializer(serializers.ModelSerializer):
    """Serializer for events."""
    assigned_count = serializers.IntegerField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'date', 'start_time', 'end_time',
            'location', 'max_volunteers', 'status', 'status_display',
            'assigned_count', 'created_at',
        ]


class AttendanceSerializer(serializers.ModelSerializer):
    """Serializer for attendance records."""
    volunteer_name = serializers.CharField(source='volunteer.full_name', read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)

    class Meta:
        model = Attendance
        fields = [
            'id', 'event', 'event_title', 'volunteer', 'volunteer_name',
            'check_in', 'check_out', 'status',
        ]


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics (not tied to a model)."""
    total_volunteers = serializers.IntegerField()
    approved_volunteers = serializers.IntegerField()
    pending_applications = serializers.IntegerField()
    active_events = serializers.IntegerField()
    total_events = serializers.IntegerField()
