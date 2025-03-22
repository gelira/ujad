from django.db import models
from django.db import transaction
from django.shortcuts import get_object_or_404
from sales import exceptions
from custom_auth.models import User
from utils.models import BaseModel

class Wallet(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    tickets_amount = models.IntegerField(default=0)

    @classmethod
    def get_or_create_wallet(cls, user):
        wallet, _ = cls.objects.get_or_create(
            user_id=user.id
        )

        return wallet
    
    @classmethod
    def process_purchase(cls, user, products):
        with transaction.atomic():
            wallet = cls.get_or_create_wallet(user)

            if not wallet.is_active:
                raise exceptions.InactiveWalletException()

            ticket = Ticket.objects.create(
                wallet=wallet,
                status='pending',
                payment_method='teste',
                original_value=0,
                remaining_value=0
            )

            for p in products:
                product = get_object_or_404(Product.objects.select_for_update(), uid=p['uid'])

                if product.quantity < p['quantity']:
                    raise exceptions.InsufficientProductStockException()

                for _ in range(p['quantity']):
                    ProductTicket.objects.create(
                        product=product,
                        ticket=ticket,
                        product_price=product.price
                    )

                ticket.original_value += product.price * p['quantity']
                
                product.quantity = models.F('quantity') - p['quantity']
                product.save()

            ticket.remaining_value = ticket.original_value
            ticket.save()
            
            return ticket

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
    dispatcher = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    product_price = models.IntegerField()
    consumed = models.BooleanField(default=False)
