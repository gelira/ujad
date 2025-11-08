from datetime import timedelta
from django.db import models
from django.utils import timezone
from utils import generate_random_numeric_string
from utils.models import BaseModel
from uuid import UUID

from custom_auth.exceptions import InvalidAuthCodeException

class User(BaseModel):
    ROLE_ADMIN = 'admin'
    ROLE_CONSUMER = 'consumer'
    ROLE_DISPATCHER = 'dispatcher'
    ROLE_CHOICES = [
        (ROLE_ADMIN, ROLE_ADMIN),
        (ROLE_CONSUMER, ROLE_CONSUMER),
        (ROLE_DISPATCHER, ROLE_DISPATCHER)
    ]

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True)
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default=ROLE_CONSUMER
    )
    is_active = models.BooleanField(default=True)

    @classmethod
    def get_or_create_by_email(cls, email: str):
        user, _ = cls.objects.get_or_create(
            email=email,
            defaults={
                'name': '',
                'role': cls.ROLE_CONSUMER
            }
        )

        return user

class AuthCode(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    code = models.CharField(max_length=6)
    is_active = models.BooleanField(default=True)
    expired_at = models.DateTimeField()

    @classmethod
    def generate(cls, user: User):
        return cls.objects.create(
            user=user,
            code=generate_random_numeric_string(),
            expired_at=timezone.now() + timedelta(minutes=10)
        )
    
    @classmethod
    def verify(cls, uid: UUID, code: str):
        auth_code = cls.objects.filter(
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
