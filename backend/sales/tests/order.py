from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from custom_auth.models import User
from sales.models import Product, Order, Ticket, Wallet


class OrderViewSetTest(APITestCase):
    def setUp(self):
        """Set up test users, products, and orders."""
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

        self.wallet = Wallet.objects.create(user=self.consumer_user)
        self.another_wallet = Wallet.objects.create(user=self.another_consumer)

        self.order1 = Order.objects.create(wallet=self.wallet, status=Order.STATUS_PENDING, original_value=1000)
        self.ticket1 = Ticket.objects.create(order=self.order1, product=self.product1, product_price=self.product1.price)

        self.order2 = Order.objects.create(wallet=self.wallet, status=Order.STATUS_CONFIRMED, original_value=2000)
        self.order_another_user = Order.objects.create(wallet=self.another_wallet, status=Order.STATUS_PENDING)

        self.list_url = reverse('orders-list')
        self.webhook_url = reverse('orders-webhook')

    def test_list_orders_as_consumer_success(self):
        """Ensure a consumer can list their own orders."""
        self.client.force_authenticate(user=self.consumer_user)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['orders']), 2)
        order_uids = [order['uid'] for order in response.data['orders']]
        self.assertIn(str(self.order1.uid), order_uids)
        self.assertIn(str(self.order2.uid), order_uids)

    def test_list_orders_unauthenticated(self):
        """Ensure unauthenticated users cannot list orders."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_orders_as_dispatcher_fails(self):
        """Ensure dispatchers cannot list orders."""
        self.client.force_authenticate(user=self.dispatcher_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_order_as_owner_success(self):
        """Ensure a user can retrieve their own order."""
        self.client.force_authenticate(user=self.consumer_user)
        url = reverse('orders-detail', kwargs={'uid': self.order1.uid})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['uid'], str(self.order1.uid))

    def test_retrieve_order_as_non_owner_success(self):
        """
        Ensure any authenticated user can retrieve any order by its UID.
        Note: This tests the current behavior. Consider if this is the desired security model.
        """
        self.client.force_authenticate(user=self.another_consumer)
        url = reverse('orders-detail', kwargs={'uid': self.order1.uid})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['uid'], str(self.order1.uid))

    def test_retrieve_order_unauthenticated_success(self):
        """
        Ensure unauthenticated users can retrieve any order by its UID.
        Note: This tests the current behavior. Consider if this is the desired security model.
        """
        url = reverse('orders-detail', kwargs={'uid': self.order1.uid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['uid'], str(self.order1.uid))

    def test_webhook_confirm_order_success(self):
        """Ensure the webhook can confirm a pending order."""
        data = {
            'uid': str(self.order1.uid),
            'status': Order.STATUS_CONFIRMED
        }
        response = self.client.post(self.webhook_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.order1.refresh_from_db()
        self.assertEqual(self.order1.status, Order.STATUS_CONFIRMED)

    def test_webhook_cancel_order_success_and_restock(self):
        """Ensure the webhook can cancel a pending order and restock products."""
        initial_quantity = self.product1.quantity
        data = {
            'uid': str(self.order1.uid),
            'status': Order.STATUS_CANCELED
        }
        response = self.client.post(self.webhook_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.order1.refresh_from_db()
        self.assertEqual(self.order1.status, Order.STATUS_CANCELED)

        self.product1.refresh_from_db()
        # Assuming 1 ticket for product1 was in the order
        self.assertEqual(self.product1.quantity, initial_quantity + 1)

    def test_webhook_invalid_order_uid(self):
        """Ensure the webhook returns 404 for a non-existent order UID."""
        data = {
            'uid': '12345678-1234-5678-1234-567812345678',
            'status': Order.STATUS_CONFIRMED
        }
        response = self.client.post(self.webhook_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_webhook_on_non_pending_order(self):
        """Ensure the webhook does not change the status of a non-pending order."""
        # order2 has status 'confirmed'
        initial_status = self.order2.status
        data = {
            'uid': str(self.order2.uid),
            'status': Order.STATUS_CANCELED
        }
        response = self.client.post(self.webhook_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.order2.refresh_from_db()
        self.assertEqual(self.order2.status, initial_status) # Status should not change

    def test_webhook_invalid_status(self):
        """Ensure the webhook returns a validation error for an invalid status."""
        data = {
            'uid': str(self.order1.uid),
            'status': 'invalid_status'
        }
        response = self.client.post(self.webhook_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('status', response.data)

    def test_webhook_missing_data(self):
        """Ensure the webhook returns a validation error for missing data."""
        response = self.client.post(self.webhook_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('uid', response.data)
        self.assertIn('status', response.data)