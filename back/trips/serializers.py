from rest_framework import serializers

from trips.models import Trip, TripParticipation


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'

class TripParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripParticipation
        fields = '__all__'