from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from custom_auth.models import User


class UserViewSetTests(APITestCase):
    def setUp(self):
        self.user_info_url = reverse('user-user-info')
        self.user = User.objects.create(email='test@example.com', name='Test User')

    def test_get_user_info_unauthenticated(self):
        """
        Garante que usuários não autenticados não possam acessar as informações do usuário.
        """
        response = self.client.get(self.user_info_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_info_authenticated(self):
        """
        Garante que um usuário autenticado possa visualizar suas próprias informações.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.user_info_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['name'], self.user.name)

    def test_update_user_info_authenticated(self):
        """
        Garante que um usuário autenticado possa atualizar seu nome.
        """
        self.client.force_authenticate(user=self.user)
        new_name = 'New Test Name'
        data = {'name': new_name}
        response = self.client.patch(self.user_info_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, new_name)
        self.assertEqual(response.data['name'], new_name)

    def test_update_user_info_with_invalid_data(self):
        """
        Garante que a atualização falhe se dados inválidos forem fornecidos (ex: nome em branco).
        """
        self.client.force_authenticate(user=self.user)
        original_name = self.user.name
        data = {'name': ''}  # Nome em branco, que é inválido
        response = self.client.patch(self.user_info_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, original_name)
