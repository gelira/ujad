from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

from custom_auth.models import User
from sales.models import Product, Order, Ticket, Wallet, ConsumingToken
from sales.services import COSUMING_TOKEN_EXPIRATION_TIME


class WalletViewSetTest(APITestCase):
    def setUp(self):
        """Set up test users, products, and initial data."""
        self.consumer_user = User.objects.create(
            email='consumer@test.com',
            name='Consumer User',
            role=User.ROLE_CONSUMER,
            is_active=True
        )
        self.another_consumer = User.objects.create(
            email='another@test.com',
            name='Another Consumer',
            role=User.ROLE_CONSUMER,
            is_active=True
        )
        self.dispatcher_user = User.objects.create(
            email='dispatcher@test.com',
            name='Dispatcher User',
            role=User.ROLE_DISPATCHER,
            is_active=True
        )

        self.product1 = Product.objects.create(name='Test Product 1', price=1000, quantity=10)
        self.product2 = Product.objects.create(name='Test Product 2', price=2000, quantity=5)

        self.wallet = Wallet.objects.create(user=self.consumer_user)
        self.order = Order.objects.create(wallet=self.wallet, status=Order.STATUS_CONFIRMED, original_value=3000, remaining_value=3000)
        self.ticket1 = Ticket.objects.create(order=self.order, product=self.product1, product_price=self.product1.price)
        self.ticket2 = Ticket.objects.create(order=self.order, product=self.product2, product_price=self.product2.price, consumed=True, dispatcher=self.dispatcher_user)

        self.orders_url = reverse('wallet-orders-action')
        self.tickets_url = reverse('wallet-tickets')
        self.consuming_token_url = reverse('wallet-generate-consuming-token')
        self.consume_url = reverse('wallet-consume')

    def test_create_order_success(self):
        """Ensure a consumer can create a new order."""
        self.client.force_authenticate(user=self.consumer_user)
        data = {
            'products': [
                {'uid': str(self.product1.uid), 'quantity': 2},
                {'uid': str(self.product2.uid), 'quantity': 1}
            ]
        }
        response = self.client.post(self.orders_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('order_uid', response.data)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(Ticket.objects.filter(order__wallet__user=self.consumer_user).count(), 5) # 2 existing + 3 new
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.quantity, 8) # 10 - 2
        self.product2.refresh_from_db()
        self.assertEqual(self.product2.quantity, 4) # 5 - 1

    def test_create_order_insufficient_stock(self):
        """Ensure order creation fails with insufficient stock."""
        self.client.force_authenticate(user=self.consumer_user)
        data = {'products': [{'uid': str(self.product1.uid), 'quantity': 11}]}
        response = self.client.post(self.orders_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'].code, 'insufficient_product_stock')

    def test_create_order_unauthenticated(self):
        """Ensure unauthenticated users cannot create orders."""
        data = {'products': [{'uid': str(self.product1.uid), 'quantity': 1}]}
        response = self.client.post(self.orders_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_as_dispatcher_fails(self):
        """Ensure dispatchers cannot create orders."""
        self.client.force_authenticate(user=self.dispatcher_user)
        data = {'products': [{'uid': str(self.product1.uid), 'quantity': 1}]}
        response = self.client.post(self.orders_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_tickets_success(self):
        """Ensure a consumer can retrieve their non-consumed tickets."""
        self.client.force_authenticate(user=self.consumer_user)
        response = self.client.get(self.tickets_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['tickets']), 1)
        self.assertEqual(response.data['tickets'][0]['uid'], str(self.ticket1.uid))

    def test_get_all_tickets_success(self):
        """Ensure a consumer can retrieve all their tickets using 'all' query param."""
        self.client.force_authenticate(user=self.consumer_user)
        response = self.client.get(self.tickets_url, {'all': 'true'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['tickets']), 2)

    def test_get_tickets_unauthenticated(self):
        """Ensure unauthenticated users cannot retrieve tickets."""
        response = self.client.get(self.tickets_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_tickets_no_wallet(self):
        """Ensure a wallet is created if one doesn't exist when getting tickets."""
        self.client.force_authenticate(user=self.another_consumer)
        response = self.client.get(self.tickets_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Wallet.objects.filter(user=self.another_consumer).exists())
        self.assertEqual(len(response.data['tickets']), 0)

    def test_generate_consuming_token_success(self):
        """Ensure a consumer can generate a consuming token."""
        self.client.force_authenticate(user=self.consumer_user)
        response = self.client.get(self.consuming_token_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('consuming_token_uid', response.data)
        self.assertIn('expired_at', response.data)
        self.assertTrue(ConsumingToken.objects.filter(wallet=self.wallet, used=False).exists())

    def test_generate_consuming_token_reuse_existing(self):
        """Ensure an existing valid token is returned instead of creating a new one."""
        self.client.force_authenticate(user=self.consumer_user)
        
        # First call creates a token
        response1 = self.client.get(self.consuming_token_url)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        token_uid1 = response1.data['consuming_token_uid']

        # Second call should return the same token
        response2 = self.client.get(self.consuming_token_url)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        token_uid2 = response2.data['consuming_token_uid']

        self.assertEqual(token_uid1, token_uid2)
        self.assertEqual(ConsumingToken.objects.filter(wallet=self.wallet, used=False).count(), 1)

    def test_generate_consuming_token_unauthenticated(self):
        """Ensure unauthenticated users cannot generate a token."""
        response = self.client.get(self.consuming_token_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_consume_data_success(self):
        """Ensure a dispatcher can get consumer data using a valid token."""
        ct = ConsumingToken.objects.create(
            wallet=self.wallet,
            expired_at=timezone.now() + timedelta(minutes=COSUMING_TOKEN_EXPIRATION_TIME)
        )
        self.client.force_authenticate(user=self.dispatcher_user)
        url = f"{self.consume_url}?consuming_token_uid={ct.uid}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.consumer_user.name)
        self.assertEqual(response.data['email'], self.consumer_user.email)
        self.assertEqual(len(response.data['tickets']), 1)
        self.assertEqual(response.data['tickets'][0]['uid'], str(self.ticket1.uid))

    def test_get_consume_data_invalid_token(self):
        """Ensure getting consume data fails with an invalid token."""
        self.client.force_authenticate(user=self.dispatcher_user)
        url = f"{self.consume_url}?consuming_token_uid=12345678-1234-5678-1234-567812345678"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_consume_data_expired_token(self):
        """Ensure getting consume data fails with an expired token."""
        ct = ConsumingToken.objects.create(
            wallet=self.wallet,
            expired_at=timezone.now() - timedelta(minutes=1)
        )
        self.client.force_authenticate(user=self.dispatcher_user)
        url = f"{self.consume_url}?consuming_token_uid={ct.uid}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_consume_data_as_consumer_fails(self):
        """Ensure a consumer cannot get consume data."""
        ct = ConsumingToken.objects.create(
            wallet=self.wallet,
            expired_at=timezone.now() + timedelta(minutes=COSUMING_TOKEN_EXPIRATION_TIME)
        )
        self.client.force_authenticate(user=self.consumer_user)
        url = f"{self.consume_url}?consuming_token_uid={ct.uid}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_consume_tickets_success(self):
        """Ensure a dispatcher can consume tickets."""
        ct = ConsumingToken.objects.create(
            wallet=self.wallet,
            expired_at=timezone.now() + timedelta(minutes=COSUMING_TOKEN_EXPIRATION_TIME)
        )
        self.client.force_authenticate(user=self.dispatcher_user)
        
        # Create another ticket to consume
        ticket_to_consume = Ticket.objects.create(order=self.order, product=self.product1, product_price=self.product1.price)

        url = f"{self.consume_url}?consuming_token_uid={ct.uid}"
        data = {'tickets': [str(ticket_to_consume.uid)]}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tickets'], [str(ticket_to_consume.uid)])

        ticket_to_consume.refresh_from_db()
        self.assertTrue(ticket_to_consume.consumed)
        self.assertEqual(ticket_to_consume.dispatcher, self.dispatcher_user)

        ct.refresh_from_db()
        self.assertTrue(ct.used)

        self.order.refresh_from_db()
        self.assertEqual(self.order.remaining_value, 3000 - ticket_to_consume.product_price)

    def test_post_consume_ticket_not_found(self):
        """Ensure consuming a non-existent ticket fails."""
        ct = ConsumingToken.objects.create(
            wallet=self.wallet,
            expired_at=timezone.now() + timedelta(minutes=COSUMING_TOKEN_EXPIRATION_TIME)
        )
        self.client.force_authenticate(user=self.dispatcher_user)
        url = f"{self.consume_url}?consuming_token_uid={ct.uid}"
        data = {'tickets': ['12345678-1234-5678-1234-567812345678']}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'].code, 'cant_use_ticket')

    def test_post_consume_already_consumed_ticket(self):
        """Ensure consuming an already consumed ticket fails."""
        ct = ConsumingToken.objects.create(
            wallet=self.wallet,
            expired_at=timezone.now() + timedelta(minutes=COSUMING_TOKEN_EXPIRATION_TIME)
        )
        self.client.force_authenticate(user=self.dispatcher_user)
        url = f"{self.consume_url}?consuming_token_uid={ct.uid}"
        data = {'tickets': [str(self.ticket2.uid)]} # ticket2 is already consumed
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'].code, 'cant_use_ticket')

    def test_post_consume_ticket_from_another_user(self):
        """Ensure a dispatcher cannot consume a ticket that doesn't belong to the token's user."""
        another_wallet = Wallet.objects.create(user=self.another_consumer)
        another_order = Order.objects.create(wallet=another_wallet, status=Order.STATUS_CONFIRMED)
        another_ticket = Ticket.objects.create(order=another_order, product=self.product1, product_price=self.product1.price)

        ct = ConsumingToken.objects.create(
            wallet=self.wallet, # Token for the main consumer_user
            expired_at=timezone.now() + timedelta(minutes=COSUMING_TOKEN_EXPIRATION_TIME)
        )
        self.client.force_authenticate(user=self.dispatcher_user)
        url = f"{self.consume_url}?consuming_token_uid={ct.uid}"
        data = {'tickets': [str(another_ticket.uid)]}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'].code, 'cant_use_ticket')

    def test_post_consume_as_consumer_fails(self):
        """Ensure a consumer cannot consume tickets."""
        ct = ConsumingToken.objects.create(
            wallet=self.wallet,
            expired_at=timezone.now() + timedelta(minutes=COSUMING_TOKEN_EXPIRATION_TIME)
        )
        self.client.force_authenticate(user=self.consumer_user)
        url = f"{self.consume_url}?consuming_token_uid={ct.uid}"
        data = {'tickets': [str(self.ticket1.uid)]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)