from rest_framework import serializers

from core.serializers import PublicUserSerializer
from trips.models import Trip, TripParticipation, TripInvitation


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'


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
