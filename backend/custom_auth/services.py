from custom_auth.email import send_mail_async
from custom_auth.exceptions import InvalidAuthCodeException
from custom_auth.models import AuthCode, User
from django.utils import timezone
from datetime import timedelta
from utils import generate_random_numeric_string

class AuthCodeServices:
    @staticmethod
    def send_email(user_email, auth_code):
        subject = 'UJAD - Código de autenticação'
        body = f'Seu código de autenticação: {auth_code}'

        send_mail_async(subject, user_email, body)

    @staticmethod
    def generate(user):
        return AuthCode.objects.create(
            user=user,
            code=generate_random_numeric_string(),
            expired_at=timezone.now() + timedelta(minutes=10)
        )

    @staticmethod
    def verify(uid, code):
        auth_code = AuthCode.objects.filter(
            uid=uid,
            code=code,
            is_active=True,
            expired_at__gt=timezone.now()
        ).first()

        if not auth_code:
            raise InvalidAuthCodeException()

        auth_code.is_active = False
        auth_code.save()

        return auth_code.user

class UserServices:
    @staticmethod
    def get_or_create_by_email(email):
        user, _ = User.objects.get_or_create(
            email=email
        )

        return user
