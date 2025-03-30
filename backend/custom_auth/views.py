from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from custom_auth.email import send_mail_async
from custom_auth.serializers import GenerateAuthCodeSerializer, UserSerializer, VerifyAuthCodeSerializer
from custom_auth.models import AuthCode, User

class AuthCodeViewSet(ViewSet):
    authentication_classes = []
    permission_classes = []

    def create(self, request):
        serializer = GenerateAuthCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.get_or_create_by_email(serializer.validated_data['email'])

        if not user.is_active:
            return Response(status=401)

        auth_code = AuthCode.generate(user)

        send_mail_async(
            'UJAD - Código de autenticação',
            user.email,
            f'Seu código de autenticação: {auth_code.code}'
        )

        return Response({ 'auth_code_uid': auth_code.uid })
    
    @action(detail=False, methods=['post'], url_path='verify')
    def verify_auth_code(self, request):
        serializer = VerifyAuthCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        user = AuthCode.verify(
            uid=validated_data['auth_code_uid'],
            code=validated_data['code']
        )

        if not user.is_active:
            return Response(status=401)

        token = AccessToken.for_user(user)

        return Response({ 'token': str(token) })
        
class UserViewSet(ViewSet):
    @action(detail=False, methods=['get', 'patch'], url_path='info')
    def user_info(self, request):
        user = request.user

        if request.method == 'PATCH':
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            user.name = serializer.validated_data['name']
            user.save()

        return Response(UserSerializer(user).data)
