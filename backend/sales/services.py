from datetime import timedelta
from django.db import models, transaction
from django.utils import timezone
from sales.exceptions import (
    InactiveWalletException,
    InsufficientProductStockException,
    CantUseTicketException,
)
from sales.models import (
    ConsumingToken,
    Order,
    Product,
    Ticket,
    Wallet,
)

COSUMING_TOKEN_EXPIRATION_TIME = 40 # minutes

class ProductServices:
    @staticmethod
    def update_quantity(product, diff):
        with transaction.atomic():
            product.quantity = models.F('quantity') + diff
            product.save()

class WalletServices:
    @staticmethod
    def get_or_create_wallet(user):
        wallet, _ = Wallet.objects.get_or_create(user_id=user.id)

        if not wallet.is_active:
            raise InactiveWalletException()

        return wallet

    @staticmethod
    def process_new_order(user, products):
        with transaction.atomic():
            wallet = WalletServices.get_or_create_wallet(user)

            order = Order.objects.create(
                wallet=wallet
            )

            for p in products:
                product = Product.find_by_uid_or_404(str(p['uid']))

                if product.quantity < p['quantity']:
                    raise InsufficientProductStockException()

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

    @staticmethod
    def get_tickets(user, all_tickets=False, wallet=None):
        if not wallet:
            wallet = WalletServices.get_or_create_wallet(user)

        qs = Ticket.objects.filter(
            order__wallet_id=wallet.id,
            order__status=Order.STATUS_CONFIRMED
        )

        if not all_tickets:
            qs = qs.filter(consumed=False)

        return qs.prefetch_related('product')

    @staticmethod
    def get_or_create_consuming_token(user):
        wallet = WalletServices.get_or_create_wallet(user)

        now = timezone.now()

        ct = ConsumingToken.objects.filter(
            wallet_id=wallet.id,
            expired_at__gt=now,
            used=False
        ).first()

        return ct or ConsumingToken.objects.create(
            wallet=wallet,
            expired_at=now + timedelta(minutes=COSUMING_TOKEN_EXPIRATION_TIME)
        )

    @staticmethod
    def get_consuming_token(uid):
        consuming_token = ConsumingToken.find_by_uid_or_404(
            uid,
            used=False,
            expired_at__gt=timezone.now(),
        )

        if not consuming_token.wallet.is_active:
            raise InactiveWalletException()
        
        return consuming_token

    @staticmethod
    def consume(dispatcher_user, consuming_token, ticket_uid_list):
        tickets_consumed = []

        with transaction.atomic():
            orders_consuming = {}

            for uid in ticket_uid_list:
                ticket = Ticket.objects.filter(
                    uid=uid,
                    consumed=False,
                    order__wallet_id=consuming_token.wallet_id,
                    order__status=Order.STATUS_CONFIRMED
                ).first()

                if not ticket:
                    raise CantUseTicketException()

                orders_consuming[ticket.order_id] = \
                    orders_consuming.get(ticket.order_id, 0) + ticket.product_price

                ticket.consumed = True
                ticket.dispatcher = dispatcher_user
                ticket.save()

                tickets_consumed.append(str(ticket.uid))

            for order_id, consumed in orders_consuming.items():
                Order.objects.filter(pk=order_id).update(
                    remaining_value=models.F('remaining_value') - consumed
                )

            consuming_token.used = True
            consuming_token.save()

        return tickets_consumed

class OrderServices:
    @staticmethod
    def webhook_handler(uid, status):
        order = Order.find_by_uid_or_404(uid)

        if order.status != Order.STATUS_PENDING:
            return

        if status == Order.STATUS_CONFIRMED:
            order.status = Order.STATUS_CONFIRMED
            order.save()

            return
        
        with transaction.atomic():
            product_quantity_dict = {}

            for po in order.tickets.all():
                product_quantity_dict[po.product_id] = \
                    product_quantity_dict.get(po.product_id, 0) + 1

            for product_id, quantity in product_quantity_dict.items():
                Product.objects.filter(pk=product_id)\
                    .update(quantity=models.F('quantity') + quantity)

            order.status = Order.STATUS_CANCELED
            order.save()
