import math

from rest_framework import serializers

from trips.models import Trip
from trips.services import TripService
from visits.models import Visit, Location, LocationPrice


# Locations
class LocationQueryParamsSerializer(serializers.Serializer):
    lat: float = serializers.FloatField(required=False)
    lon: float = serializers.FloatField(required=False)
    radius: float = serializers.FloatField(required=False)
    minPrice: float = serializers.FloatField(required=False)
    maxPrice: float = serializers.FloatField(required=False)
    search: str = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data: dict):
        lat = data.get('lat')
        lon = data.get('lon')
        radius = data.get('radius')
        if any([lat, lon, radius]) and not all([lat, lon, radius]):
            raise serializers.ValidationError("lat, lon and radius must be provided together")

        min_price = data.get('minPrice', 0)
        max_price = data.get('maxPrice', 10000000)
        if min_price < 0 or max_price < 0:
            raise serializers.ValidationError("Prices must be positive")
        if min_price > max_price:
            raise serializers.ValidationError("minPrice must be less than or equal to maxPrice")

        return data


class LocationPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationPrice
        exclude = ('location', 'created_on')


class LocationSerializer(serializers.ModelSerializer):
    prices = LocationPriceSerializer(many=True, read_only=True)

    class Meta:
        model = Location
        fields = '__all__'


# Visits
class VisitInputSerializer(serializers.ModelSerializer):
    trip_id = serializers.IntegerField()
    location_id = serializers.IntegerField()

    class Meta:
        model = Visit
        fields = ['visit_id', 'location_id', 'trip_id', 'name', 'start_date', 'end_date']

    def to_representation(self, instance):
        data = super().to_representation(instance)

        trip_id = instance['trip_id']
        if 'trip_id' in data:
            del data['trip_id']
        data['trip'] = Trip.objects.get(trip_id=trip_id)

        location_id = instance['location_id']
        if 'location_id' in data:
            del data['location_id']
        data['location'] = Location.objects.get(location_id=location_id)

        return data


class VisitSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    trip_id = serializers.IntegerField(source='trip.trip_id')

    class Meta:
        model = Visit
        exclude = ('trip',)
