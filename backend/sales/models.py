import uuid
from datetime import timedelta
from django.db import models, transaction
from django.utils import timezone
from rest_framework.exceptions import NotFound
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
                product = Product.find_by_uid_or_404(p['uid'])

                if product.quantity < p['quantity']:
                    raise exceptions.InsufficientProductStockException()

                for _ in range(p['quantity']):
                    Ticket.objects.create(
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

    def get_tickets(self, all=False):
        qs = Ticket.objects.filter(
            order__wallet_id=self.id,
            order__status=Order.STATUS_CONFIRMED
        )

        if not all:
            qs = qs.filter(consumed=False)

        return qs.prefetch_related('product')

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
        on_delete=models.PROTECT
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
        order = cls.find_by_uid_or_404(uid)

        if order.status != cls.STATUS_PENDING:
            return

        if status == cls.STATUS_CONFIRMED:
            order.status = cls.STATUS_CONFIRMED
            order.save()

            return
        
        with transaction.atomic():
            product_quantity_dict = {}

            for po in order.ticket_set.all():
                product_quantity_dict[po.product_id] = product_quantity_dict.get(po.product_id, 0) + 1

            for product_id, quantity in product_quantity_dict.items():
                Product.objects.filter(pk=product_id).update(quantity=models.F('quantity') + quantity)

            order.status = cls.STATUS_CANCELED
            order.save()

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

class Ticket(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    dispatcher = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    product_price = models.IntegerField()
    consumed = models.BooleanField(default=False)

class ConsumingToken(BaseModel):
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)
    expired_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    @classmethod
    def get_or_create_consuming_token(cls, wallet):
        now = timezone.now()

        ct = cls.objects.filter(
            wallet_id=wallet.id,
            expired_at__gt=now,
            used=False
        ).first()

        return ct or cls.objects.create(
            wallet=wallet,
            expired_at=now + timedelta(minutes=40)
        )
    
    @classmethod
    def find_by_uid_or_404(cls, uid):
        try:
            validated_uid = uuid.UUID(uid)
            
            return cls.objects.get(
                uid=validated_uid,
                expired_at__gt=timezone.now(),
                used=False
            )
        
        except Exception:
            raise NotFound()

    def consume(self, dispatcher, ticket_uid_list):
        tickets_consumed = []

        with transaction.atomic():
            orders_consuming = {}

            for uid in ticket_uid_list:
                ticket = Ticket.objects.filter(
                    uid=uid,
                    consumed=False,
                    order__wallet_id=self.wallet_id,
                    order__status=Order.STATUS_CONFIRMED
                ).first()

                if not ticket:
                    raise exceptions.CantUseTicketException()

                orders_consuming[ticket.order_id] = \
                    orders_consuming.get(ticket.order_id, 0) + ticket.product_price

                ticket.consumed = True
                ticket.dispatcher = dispatcher
                ticket.save()

                tickets_consumed.append(str(ticket.uid))

            for order_id, consumed in orders_consuming.items():
                Order.objects.filter(pk=order_id).update(
                    remaining_value=models.F('remaining_value') - consumed
                )

            self.used = True
            self.save()

        return tickets_consumed

