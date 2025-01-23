from rest_framework import serializers

from core.serializers import ImageSerializer
from trips.models import Trip
from visits.models import Visit, Location, LocationPrice, LocationPicture


# Locations
class LocationQueryParamsSerializer(serializers.Serializer):
    lat: float = serializers.FloatField(required=False)
    lon: float = serializers.FloatField(required=False)
    radius: float = serializers.FloatField(required=False)
    min_price: float = serializers.FloatField(required=False)
    max_price: float = serializers.FloatField(required=False)
    search: str = serializers.CharField(required=False, allow_blank=True)
    sort_by: str = serializers.ChoiceField(choices=['name', 'location_id'], required=False)
    sort_order: str = serializers.ChoiceField(choices=['asc', 'desc'], required=False)
    min_lat: float = serializers.FloatField(required=False)
    max_lat: float = serializers.FloatField(required=False)
    min_lon: float = serializers.FloatField(required=False)
    max_lon: float = serializers.FloatField(required=False)

    def validate(self, data: dict):
        lat = data.get('lat')
        lon = data.get('lon')
        radius = data.get('radius')
        if any([lat, lon, radius]) and not all([lat, lon, radius]):
            raise serializers.ValidationError("lat, lon and radius must be provided together")

        min_lat = data.get('min_lat')
        max_lat = data.get('max_lat')
        min_lon = data.get('min_lon')
        max_lon = data.get('max_lon')
        if any([min_lat, max_lat, min_lon, max_lon]) and not all([min_lat, max_lat, min_lon, max_lon]):
            raise serializers.ValidationError("min_lat, max_lat, min_lon and max_lon must be provided together")
        if min_lat and max_lat and min_lat > max_lat:
            raise serializers.ValidationError("min_lat must be less than or equal to max_lat")
        if min_lon and max_lon and min_lon > max_lon:
            raise serializers.ValidationError("min_lon must be less than or equal to max_lon")

        if any([min_lat, max_lat, min_lon, max_lon]) and any([lat, lon, radius]):
            raise serializers.ValidationError("Cannot provide both lat, lon, radius and min_lat, max_lat, min_lon, max_lon")

        min_price = data.get('minPrice', 0)
        max_price = data.get('maxPrice', 10000000)
        if min_price < 0 or max_price < 0:
            raise serializers.ValidationError("Prices must be positive")
        if min_price > max_price:
            raise serializers.ValidationError("minPrice must be less than or equal to maxPrice")

        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if all([data.get('min_lat'), data.get('max_lat'), data.get('min_lon'), data.get('max_lon')]):
            data['is_viewport'] = True
        else:
            data['is_viewport'] = False

        return data


class LocationPictureSerializer(serializers.ModelSerializer):
    image = ImageSerializer(source='picture')

    class Meta:
        model = LocationPicture
        exclude = ['location']


class LocationPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationPrice
        exclude = ('location', 'created_on')


class LocationSerializer(serializers.ModelSerializer):
    prices = LocationPriceSerializer(many=True, read_only=True)
    pictures = LocationPictureSerializer(many=True, read_only=True)

    class Meta:
        model = Location
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if 'pictures' in data and data['pictures']:
            data['pictures'] = [picture['image'] for picture in data['pictures']]

        return data


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
