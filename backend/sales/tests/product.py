from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from custom_auth.models import User
from sales.models import Product


class ProductViewSetTest(APITestCase):
    def setUp(self):
        """Set up test users and products."""
        self.admin_user = User.objects.create(
            email='admin@test.com',
            name='Admin User',
            role=User.ROLE_ADMIN,
            is_active=True
        )
        self.regular_user = User.objects.create(
            email='user@test.com',
            name='Regular User',
            role=User.ROLE_CONSUMER,
            is_active=True
        )

        self.product1 = Product.objects.create(name='Test Product 1', price=1000, quantity=10)
        self.product2 = Product.objects.create(name='Test Product 2', price=2000, quantity=20)

        self.list_url = reverse('products-list')

    def _detail_url(self, uid):
        return reverse('products-detail', kwargs={'uid': uid})

    def _quantity_url(self, uid):
        return reverse('products-update-quantity', kwargs={'uid': uid})

    def test_list_products_authenticated_regular_user_and_order_by_name(self):
        """
        Ensure a regular authenticated user can list products.
        """
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['products']), 2)

        product1 = response.data['products'][0]
        product2 = response.data['products'][1]

        self.assertEqual(product1['uid'], str(self.product1.uid))
        self.assertEqual(product2['uid'], str(self.product2.uid))

    def test_create_product_as_admin(self):
        """
        Ensure an admin user can create a new product.
        """
        self.client.force_authenticate(user=self.admin_user)
        data = {'name': 'New Product', 'price': 1500}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 3)
        self.assertEqual(response.data['name'], 'New Product')

    def test_create_product_as_regular_user_fails(self):
        """
        Ensure a regular user cannot create a product.
        """
        self.client.force_authenticate(user=self.regular_user)
        data = {'name': 'New Product', 'price': 1500}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_product_unauthenticated_fails(self):
        """
        Ensure an unauthenticated user cannot create a product.
        """
        data = {'name': 'New Product', 'price': 1500}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_product_as_admin(self):
        """
        Ensure an admin can retrieve a product.
        """
        self.client.force_authenticate(user=self.admin_user)
        url = self._detail_url(self.product1.uid)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product1.name)

    def test_retrieve_product_as_regular_user_fails(self):
        """
        Ensure a regular user cannot retrieve a product.
        """
        self.client.force_authenticate(user=self.regular_user)
        url = self._detail_url(self.product1.uid)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_product_as_admin(self):
        """
        Ensure an admin can fully update a product.
        """
        self.client.force_authenticate(user=self.admin_user)
        url = self._detail_url(self.product1.uid)
        data = {'name': 'Updated Product 1', 'price': 1200}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.name, 'Updated Product 1')
        self.assertEqual(self.product1.price, 1200)

    def test_update_product_as_regular_user_fails(self):
        """
        Ensure a regular user cannot update a product.
        """
        self.client.force_authenticate(user=self.regular_user)
        url = self._detail_url(self.product1.uid)
        data = {'name': 'Updated Product 1', 'price': 1200}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_product_as_admin(self):
        """
        Ensure an admin can partially update a product.
        """
        self.client.force_authenticate(user=self.admin_user)
        url = self._detail_url(self.product1.uid)
        data = {'price': 1300}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.price, 1300)

    def test_partial_update_product_as_regular_user_fails(self):
        """
        Ensure a regular user cannot partially update a product.
        """
        self.client.force_authenticate(user=self.regular_user)
        url = self._detail_url(self.product1.uid)
        data = {'price': 1300}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_product_as_admin(self):
        """
        Ensure an admin can delete a product.
        """
        self.client.force_authenticate(user=self.admin_user)
        url = self._detail_url(self.product1.uid)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 1)

    def test_destroy_product_as_regular_user_fails(self):
        """
        Ensure a regular user cannot delete a product.
        """
        self.client.force_authenticate(user=self.regular_user)
        url = self._detail_url(self.product1.uid)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_quantity_as_admin(self):
        """
        Ensure an admin can update a product's quantity.
        """
        self.client.force_authenticate(user=self.admin_user)
        url = self._quantity_url(self.product1.uid)
        initial_quantity = self.product1.quantity
        quantity_to_add = 5
        data = {'quantity': quantity_to_add}

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.product1.refresh_from_db()
        self.assertEqual(self.product1.quantity, initial_quantity + quantity_to_add)
        self.assertEqual(response.data['quantity'], initial_quantity + quantity_to_add)

    def test_update_quantity_as_admin_with_negative_value(self):
        """
        Ensure an admin can decrease a product's quantity.
        """
        self.client.force_authenticate(user=self.admin_user)
        url = self._quantity_url(self.product1.uid)
        initial_quantity = self.product1.quantity
        quantity_to_remove = -5
        data = {'quantity': quantity_to_remove}

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.product1.refresh_from_db()
        self.assertEqual(self.product1.quantity, initial_quantity + quantity_to_remove)
        self.assertEqual(response.data['quantity'], initial_quantity + quantity_to_remove)

    def test_update_quantity_as_regular_user_fails(self):
        """
        Ensure a regular user cannot update a product's quantity.
        """
        self.client.force_authenticate(user=self.regular_user)
        url = self._quantity_url(self.product1.uid)
        data = {'quantity': 5}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
