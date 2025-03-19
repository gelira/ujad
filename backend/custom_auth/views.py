from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from custom_auth.email import send_auth_code

from .serializers import GenerateAuthCodeSerializer, VerifyAuthCodeSerializer
from .models import AuthCode, User

class AuthViewSet(ViewSet):
    @action(detail=False, methods=['post'], url_path='generate')
    def generate_auth_code(self, request):
        serializer = GenerateAuthCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.get_or_create_by_email(serializer.validated_data['email'])
        auth_code = AuthCode.generate(user)

        send_auth_code(user.email, auth_code.code)

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

            token = AccessToken.for_user(user)

            return Response({ 'token': str(token) })
        
        except AuthCode.DoesNotExist:
            return Response(status=401)
