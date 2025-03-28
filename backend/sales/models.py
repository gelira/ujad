from django.db import models
from django.db import transaction
from django.shortcuts import get_object_or_404
from sales import exceptions
from custom_auth.models import User
from utils.models import BaseModel

class Wallet(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    @classmethod
    def get_or_create_wallet(cls, user):
        wallet, _ = cls.objects.get_or_create(
            user_id=user.id,
            is_active=True
        )

        return wallet
    
    @classmethod
    def process_new_order(cls, user, products):
        with transaction.atomic():
            wallet = cls.get_or_create_wallet(user)

            if not wallet.is_active:
                raise exceptions.InactiveWalletException()

            order = Order.objects.create(
                wallet=wallet,
                payment_method='teste'
            )

            for p in products:
                product = get_object_or_404(Product.objects.select_for_update(), uid=p['uid'])

                if product.quantity < p['quantity']:
                    raise exceptions.InsufficientProductStockException()

                for _ in range(p['quantity']):
                    ProductOrder.objects.create(
                        product=product,
                        order=order,
                        product_price=product.price
                    )

                order.original_value += product.price * p['quantity']
                
                product.quantity = models.F('quantity') - p['quantity']
                product.save()

            order.remaining_value = order.original_value
            order.save()
            
            return order

class Order(BaseModel):
    STATUS_PENDING = 'pending'
    STATUS_CANCELED = 'canceled'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CHOICES = [
        (STATUS_PENDING, STATUS_PENDING),
        (STATUS_CANCELED, STATUS_CANCELED),
        (STATUS_CONFIRMED, STATUS_CONFIRMED),
    ]

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.PROTECT,
        related_name='orders'
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )
    payment_method = models.CharField(max_length=50)
    original_value = models.IntegerField(default=0)
    remaining_value = models.IntegerField(default=0)

    @classmethod
    def webhook_handler(cls, uid, status):
        order = get_object_or_404(cls, uid=uid)

        if order.status != cls.STATUS_PENDING:
            return

        if status == cls.STATUS_CONFIRMED:
            order.status = cls.STATUS_CONFIRMED
            order.save()

            return
        
        with transaction.atomic():
            product_quantity_dict = {}

            for po in order.productorder_set.all():
                product_quantity_dict[po.product_id] = product_quantity_dict.get(po.product_id, 0) + 1

            for product_id, quantity in product_quantity_dict.items():
                Product.objects.filter(pk=product_id).update(quantity=models.F('quantity') + quantity)

            order.status = cls.STATUS_CANCELED
            order.save()

    def consume(self, productorder_uid_list):
        if self.status != self.STATUS_CONFIRMED:
            raise exceptions.CantUseTicketException()

        with transaction.atomic():
            consumed = 0

            for uid in productorder_uid_list:
                po = self.productorder_set.filter(uid=uid, consumed=False).first()

                if not po:
                    continue

                consumed += po.product_price

                po.consumed = True
                po.save()

            if consumed:
                self.remaining_value = models.F('remaining_value') - consumed
                self.save()

        self.refresh_from_db()

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

class ProductOrder(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    dispatcher = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    product_price = models.IntegerField()
    consumed = models.BooleanField(default=False)
