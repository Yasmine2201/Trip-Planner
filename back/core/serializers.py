from rest_framework import serializers

from .models import User, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['name', 'url']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['user_id', 'email', 'alias', 'first_name', 'last_name', 'birthdate', 'profile_picture', 'description', 'languages']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.profile_picture is not None:
            representation['profile_picture'] = ImageSerializer(instance.profile_picture).data
        else:
            representation['profile_picture'] = None
        return representation
