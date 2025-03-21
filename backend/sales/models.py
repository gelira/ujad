from django.db import models
from django.db import transaction
from custom_auth.models import User
from utils.models import BaseModel

class Wallet(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    tickets_amount = models.IntegerField(default=0)

class Ticket(BaseModel):
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)
    status = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=50)
    original_value = models.IntegerField()
    remaining_value = models.IntegerField()

class Product(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    quantity = models.IntegerField(default=0)

    def update_quantity(self, diff):
        with transaction.atomic():
            self.quantity = models.F('quantity') + diff
            self.save()

        self.refresh_from_db()

class ProductTicket(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    ticket = models.ForeignKey(Ticket, on_delete=models.PROTECT)
    dispatcher = models.ForeignKey(User, on_delete=models.PROTECT)
    product_price = models.IntegerField()
    consumed = models.BooleanField(default=False)
