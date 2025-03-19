from rest_framework import serializers

from custom_auth.models import User

class GenerateAuthCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

class VerifyAuthCodeSerializer(serializers.Serializer):
    auth_code_uid = serializers.UUIDField()
    code = serializers.CharField(max_length=6)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uid', 'name', 'email', 'role']
