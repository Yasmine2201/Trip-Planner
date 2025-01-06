from rest_framework import serializers

from visits.models import Visit, Location


class VisitSerializerInput(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'

        extra_kwargs = {
            'visit_id': {'required': False},
        }

