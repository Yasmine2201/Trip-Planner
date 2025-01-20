from rest_framework import serializers

from visits.models import Visit, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


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
