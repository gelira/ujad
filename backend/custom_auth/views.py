from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from .serializers import GenerateAuthCodeSerializer, VerifyAuthCodeSerializer
from .models import AuthCode, User

class AuthViewSet(ViewSet):
    @action(detail=False, methods=['post'], url_path='generate')
    def generate_auth_code(self, request):
        serializer = GenerateAuthCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.get_or_create_by_email(serializer.validated_data['email'])
        auth_code = AuthCode.generate(user)

        return Response({ 'auth_code_uid': auth_code.uid })
    
    @action(detail=False, methods=['post'], url_path='verify')
    def verify_auth_code(self, request):
        serializer = VerifyAuthCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        try:
            user = AuthCode.verify(
                uid=validated_data['auth_code_uid'],
                code=validated_data['code']
            )

            return Response({ 'user_uid': user.uid })
        
        except AuthCode.DoesNotExist:
            return Response(status=401)
