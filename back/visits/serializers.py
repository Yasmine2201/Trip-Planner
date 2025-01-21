from rest_framework import serializers

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
        max_price = data.get('maxPrice', float('inf'))
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
    class Meta:
        model = Visit
        fields = '__all__'

        extra_kwargs = {
            'visit_id': {'required': False},
        }

    # As trip is a foreign key, we want to return the trip_id instead of the trip object
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['trip_id'] = instance.trip.trip_id
        if 'trip' in data:
            del data['trip']
        return data


class VisitSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    trip_id = serializers.IntegerField(source='trip.trip_id')

    class Meta:
        model = Visit
        exclude = ('trip',)
