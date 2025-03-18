from django.db import models
from utils.models import BaseModel

class User(BaseModel):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)

class AuthCode(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    is_active = models.BooleanField(default=True)
    expired_at = models.DateTimeField()
