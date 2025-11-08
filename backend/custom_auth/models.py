from django.db import models
from utils.models import BaseModel

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

class AuthCode(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    code = models.CharField(max_length=6)
    is_active = models.BooleanField(default=True)
    expired_at = models.DateTimeField()
