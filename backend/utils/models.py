import uuid
from django.db import models
from django_softdelete.models import SoftDeleteModel
from rest_framework.exceptions import NotFound

class BaseModel(SoftDeleteModel):
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def find_by_uid_or_404(cls, uid, **filters):
        try:
            validated_uid = uuid.UUID(uid)
            return cls.objects.get(uid=validated_uid, **filters)

        except Exception:
            raise NotFound()

    class Meta:
        abstract = True
