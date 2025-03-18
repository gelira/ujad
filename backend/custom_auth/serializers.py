from rest_framework import serializers

class GenerateAuthCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

class VerifyAuthCodeSerializer(serializers.Serializer):
    auth_code_uid = serializers.UUIDField()
    code = serializers.CharField(max_length=6)
