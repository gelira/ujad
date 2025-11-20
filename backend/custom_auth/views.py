from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from custom_auth.services import AuthCodeServices, UserServices
from custom_auth.serializers import (
    GenerateAuthCodeSerializer,
    VerifyAuthCodeSerializer,
    UserSerializer
)

class AuthCodeViewSet(ViewSet):
    authentication_classes = []
    permission_classes = []

    def create(self, request):
        serializer = GenerateAuthCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = UserServices.get_or_create_by_email(
            serializer.validated_data['email']
        )

        if not user.is_active:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        auth_code = AuthCodeServices.generate(user)

        AuthCodeServices.send_email(user.email, auth_code.code)

        return Response({ 'auth_code_uid': auth_code.uid })
    
    @action(detail=False, methods=['post'], url_path='verify')
    def verify_auth_code(self, request):
        serializer = VerifyAuthCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = AuthCodeServices.verify(
            serializer.validated_data['auth_code_uid'],
            serializer.validated_data['code']
        )

        if not user.is_active:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        token = AccessToken.for_user(user)

        return Response({ 'token': str(token) })
        
class UserViewSet(ViewSet):
    @action(detail=False, methods=['get', 'patch'], url_path='info')
    def user_info(self, request):
        user = request.user

        if request.method.lower() == 'patch':
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            user.name = serializer.validated_data['name']
            user.save()

        return Response(UserSerializer(user).data)
