from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import timedelta
from django.utils import timezone

from custom_auth.models import AuthCode, User


class AuthCodeViewSetTests(APITestCase):
    def setUp(self):
        self.generate_url = reverse('auth-code-list')
        self.verify_url = reverse('auth-code-verify-auth-code')
        self.user = User.objects.create(email='test@example.com', name='Test User')

    @patch('custom_auth.services.AuthCodeServices.send_email')
    def test_generate_auth_code_with_new_user(self, mock_send_email):
        """
        Garante que um novo usuário e um código de autenticação sejam criados
        quando um e-mail não existente é fornecido.
        """
        email = 'newuser@example.com'
        response = self.client.post(self.generate_url, {'email': email})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.filter(email=email).exists())
        user = User.objects.get(email=email)
        self.assertTrue(AuthCode.objects.filter(user=user, uid=response.data['auth_code_uid']).exists())
        self.assertIn('auth_code_uid', response.data)
        mock_send_email.assert_called_once()

    @patch('custom_auth.services.AuthCodeServices.send_email')
    def test_generate_auth_code_with_existing_user(self, mock_send_email):
        """
        Garante que um código de autenticação seja gerado para um usuário existente.
        """
        response = self.client.post(self.generate_url, {'email': self.user.email})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(AuthCode.objects.filter(user=self.user, uid=response.data['auth_code_uid']).exists())
        self.assertIn('auth_code_uid', response.data)
        mock_send_email.assert_called_once()

    @patch('custom_auth.services.AuthCodeServices.send_email')
    def test_generate_auth_code_with_inactive_user(self, mock_send_email):
        """
        Garante que usuários inativos não possam gerar códigos de autenticação.
        """
        self.user.is_active = False
        self.user.save()

        response = self.client.post(self.generate_url, {'email': self.user.email})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        mock_send_email.assert_not_called()

    def test_generate_auth_code_with_invalid_email(self):
        """
        Garante que um erro de validação seja retornado para um e-mail inválido.
        """
        response = self.client.post(self.generate_url, {'email': 'not-an-email'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_auth_code_successfully(self):
        """
        Garante que um código de autenticação válido retorne um token JWT.
        """
        auth_code = AuthCode.objects.create(
            user=self.user,
            code='123456',
            expired_at=timezone.now() + timedelta(minutes=10)
        )

        data = {
            'auth_code_uid': str(auth_code.uid),
            'code': '123456'
        }
        response = self.client.post(self.verify_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

        auth_code.refresh_from_db()
        self.assertFalse(auth_code.is_active)

    def test_verify_auth_code_with_invalid_code(self):
        """
        Garante que um código inválido retorne um erro de autenticação.
        """
        auth_code = AuthCode.objects.create(
            user=self.user,
            code='123456',
            expired_at=timezone.now() + timedelta(minutes=10)
        )

        data = {
            'auth_code_uid': str(auth_code.uid),
            'code': '654321'
        }
        response = self.client.post(self.verify_url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_verify_auth_code_with_expired_code(self):
        """
        Garante que um código expirado retorne um erro de autenticação.
        """
        auth_code = AuthCode.objects.create(
            user=self.user,
            code='123456',
            expired_at=timezone.now() - timedelta(minutes=10, seconds=1)
        )

        data = {'auth_code_uid': str(auth_code.uid), 'code': '123456'}
        response = self.client.post(self.verify_url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
