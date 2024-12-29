from rest_framework import serializers

from trips.models import Trip, TripParticipation


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
