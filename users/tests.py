from django.contrib.auth.hashers import check_password

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
User = get_user_model()
from django.urls import reverse


class UserAPITestCase(APITestCase):
    def setUp(self):
        self.data = {
            'nickname': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword1234'
        }

    def test_user_signup(self):
        response = self.client.post(reverse('user-signup'), self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data.get('nickname'), 'testuser')
        self.assertEqual(response.data.get('email'), 'test@example.com')

    def test_user_login(self):
        user = User.objects.create_user(**self.data)
        data = {
            'email': user.email,
            'password': 'testpassword1234'
        }

        response = self.client.post(reverse('user-login'), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data.get('message'), 'login successful.')

    def test_user_login_invalid_credentials(self):
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('user-login'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_details(self):
        user = User.objects.create_user(**self.data)
        self.client.login(email='test@example.com', password='testpassword1234')

        response = self.client.get(reverse('user-detail', kwargs={'pk': user.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('nickname'), 'testuser')
        self.assertEqual(response.data.get('email'), 'test@example.com')

    def test_update_user_details(self):
        user = User.objects.create_user(**self.data)
        self.client.login(email='test@example.com', password='testpassword1234')
        data = {
            'nickname': 'updateduser',
            'password': 'updatepw1234'
        }

        response = self.client.patch(reverse('user-detail', kwargs={'pk': user.id}), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('nickname'), 'updateduser')
        # 요청으로 인한 변경사항을 db로 부터 가져옴
        user.refresh_from_db()
        self.assertTrue(check_password('updatepw1234', user.password))

    def test_delete_user(self):
        user = User.objects.create_user(**self.data)
        self.client.login(email='test@example.com', password='testpassword1234')

        response = self.client.delete(reverse('user-detail', kwargs={'pk': user.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(email='test@example.com').exists())