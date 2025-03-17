import uuid
from django_softdelete.models import SoftDeleteModel
from django.db import models

class BaseModel(SoftDeleteModel):
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
