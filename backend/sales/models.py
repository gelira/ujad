from django.db import models
from custom_auth.models import User
from utils.models import BaseModel

class Wallet(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

class Order(BaseModel):
    STATUS_CREATED = 'created'
    STATUS_PENDING = 'pending'
    STATUS_CANCELED = 'canceled'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CHOICES = [
        (STATUS_CREATED, STATUS_CREATED),
        (STATUS_PENDING, STATUS_PENDING),
        (STATUS_CANCELED, STATUS_CANCELED),
        (STATUS_CONFIRMED, STATUS_CONFIRMED),
    ]

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.PROTECT,
        null=True
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=STATUS_CREATED
    )
    original_value = models.IntegerField(default=0)
    remaining_value = models.IntegerField(default=0)
    reference_id = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=200, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']

class Product(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    quantity = models.IntegerField(default=0)

    class Meta:
        ordering = ['name']

class Ticket(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='tickets')
    dispatcher = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    product_price = models.IntegerField()
    consumed = models.BooleanField(default=False)

class ConsumingToken(BaseModel):
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)
    expired_at = models.DateTimeField()
    used = models.BooleanField(default=False)
