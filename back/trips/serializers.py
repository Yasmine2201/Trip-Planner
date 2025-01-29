from rest_framework import serializers

from core.serializers import PublicUserSerializer
from trips.models import Trip, TripParticipation, TripInvitation


class TripSerializer(serializers.ModelSerializer):
    owner_id = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = '__all__'
        extra_fields = ['owner_id', 'members']

    @staticmethod
    def get_owner_id(obj):
        owner_participation = TripParticipation.objects.filter(trip=obj, is_owner=True).first()
        return owner_participation.user.user_id if owner_participation else None

    @staticmethod
    def get_members(obj):
        participations = TripParticipation.objects.filter(trip=obj)
        return PublicUserSerializer([p.user for p in participations], many=True).data


class TripInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['trip_name', 'start_date', 'end_date', 'latitude', 'longitude', 'radius']


class TripParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripParticipation
        fields = '__all__'


class TripInvitationSerializer(serializers.ModelSerializer):
    trip = TripSerializer()
    sender = PublicUserSerializer()
    receiver = PublicUserSerializer()

    class Meta:
        model = TripInvitation
        fields = '__all__'
