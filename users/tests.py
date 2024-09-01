from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import UserProfile

User = get_user_model()


class UserTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass',
            first_name='Test',
            last_name='User'
        )
        self.profile_url = reverse('user-profile')
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.telegram_url = reverse('user-profile-telegram')

    def test_register_user(self):
        """Тест регистрации пользователя"""
        data = {
            'email': 'newuser@example.com',
            'password': 'newpass',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_login_user(self):
        """Тест логина пользователя и получения токенов"""
        data = {
            'username': self.user.email,
            'password': 'testpass',
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_get_user_profile(self):
        """Тест получения профиля пользователя"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.profile_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что ключи присутствуют в ответе
        self.assertIn('email', response.data)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        # Проверяем, что значения совпадают с ожидаемыми
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(response.data['last_name'], self.user.last_name)

    def test_update_user_profile(self):
        """Тест обновления профиля пользователя"""
        self.client.force_authenticate(user=self.user)
        data = {
            'email': 'testuser@example.com',
            'first_name': 'Updated',
            'last_name': 'User'
        }
        response = self.client.put(self.profile_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'User')

    def test_get_user_telegram_profile(self):
        """Тест получения Telegram профиля пользователя"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.telegram_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['telegram_chat_id'], self.user.userprofile.telegram_chat_id)
        self.assertEqual(response.data['telegram_token'], self.user.userprofile.telegram_token)

    def test_update_user_telegram_profile(self):
        """Тест обновления Telegram профиля пользователя"""
        self.client.force_authenticate(user=self.user)
        data = {
            'telegram_chat_id': 'new_chat_id',
            'telegram_token': 'new_token'
        }
        response = self.client.put(self.telegram_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.userprofile.refresh_from_db()
        self.assertEqual(self.user.userprofile.telegram_chat_id, 'new_chat_id')
        self.assertEqual(self.user.userprofile.telegram_token, 'new_token')
