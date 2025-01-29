from rest_framework import serializers

from .models import User, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['name', 'url']


class PublicUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['user_id', 'alias', 'first_name', 'profile_picture', 'description', 'languages']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if 'profile_picture' in self.Meta.fields:
            if instance.profile_picture is not None:
                representation['profile_picture'] = ImageSerializer(instance.profile_picture).data
            else:
                representation['profile_picture'] = None
        return representation


class PrivateUserSerializer(PublicUserSerializer):

    class Meta(PublicUserSerializer.Meta):
        fields = ['user_id', 'email', 'alias', 'first_name', 'last_name', 'birthdate', 'profile_picture', 'description', 'languages']


class UserInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'alias', 'birthdate', 'description', 'languages']
