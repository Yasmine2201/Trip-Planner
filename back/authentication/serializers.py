from rest_framework import serializers


class AuthErrorSerializer(serializers.Serializer):
    message = serializers.CharField()
    error_code = serializers.CharField()


class LoginInputSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class UserSerializer(serializers.Serializer):
    id = serializers.CharField(source='user.id')
    email = serializers.EmailField(source='user.email')
    role = serializers.CharField(source='user.role')
    expires_in = serializers.IntegerField()
    expires_at = serializers.IntegerField()
