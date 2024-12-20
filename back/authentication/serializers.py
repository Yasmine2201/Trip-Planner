from rest_framework import serializers


class AuthErrorSerializer(serializers.Serializer):
    message = serializers.CharField()
    error_code = serializers.CharField()


class LoginInputSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class RegisterInputSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    alias = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    birthdate = serializers.DateField(required=False, allow_null=True)
