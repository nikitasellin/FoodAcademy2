import os

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase


class TestObtainTokenViews(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.admin_email = os.environ.get('ADMIN_USER')
        self.admin_password = os.environ.get('ADMIN_PASSWORD')
        self.admin = User.objects.create_user(
            email=self.admin_email,
            password=self.admin_password
        )

    def test_get_nok(self):
        response = self.client.get('/api/token/obtain/')
        self.assertEqual(response.status_code, 405)

    def test_post_valid_data(self):
        valid_data = {
            'email': self.admin_email,
            'password': self.admin_password,
        }
        response = self.client.post(
            '/api/token/obtain/',
            valid_data,
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['access'])

    def test_post_invalid_credentials(self):
        invalid_email = {
            'email': f'invalid-{self.admin_email}',
            'password': self.admin_password,
        }
        response = self.client.post(
            '/api/token/obtain/',
            invalid_email,
            format='json',
        )
        self.assertEqual(response.status_code, 401)
        with self.assertRaises(KeyError):
            access_token = response.data['access']
        invalid_pass = {
            'email': self.admin_email,
            'password': f'invalid-{self.admin_password}',
        }
        response = self.client.post(
            '/api/token/obtain/',
            invalid_pass,
            format='json',
        )
        self.assertEqual(response.status_code, 401)
        with self.assertRaises(KeyError):
            access_token = response.data['access']


class TestRefreshTokenViews(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.admin_email = os.environ.get('ADMIN_USER')
        self.admin_password = os.environ.get('ADMIN_PASSWORD')
        self.admin = User.objects.create_user(
            email=self.admin_email,
            password=self.admin_password
        )

    def test_get_nok(self):
        response = self.client.get('/api/token/refresh/')
        self.assertEqual(response.status_code, 405)

    def test_post_valid_data(self):
        credentials = {
            'email': self.admin_email,
            'password': self.admin_password,
        }
        response = self.client.post(
            '/api/token/obtain/',
            credentials,
            format='json',
        )
        refresh_token = response.data['refresh']
        valid_data = {'refresh': refresh_token}
        response = self.client.post(
            '/api/token/refresh/',
            valid_data,
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['access'])

    def test_post_empty_token(self):
        empty_token = {'refresh': ''}
        response = self.client.post(
            '/api/token/refresh/',
            empty_token,
            format='json',
        )
        self.assertEqual(response.status_code, 400)
        with self.assertRaises(KeyError):
            access_token = response.data['access']

    def test_post_invalid_token(self):
        invalid_token = {'refresh': '123456'}
        response = self.client.post(
            '/api/token/refresh/',
            invalid_token,
            format='json',
        )
        self.assertEqual(response.status_code, 401)
        with self.assertRaises(KeyError):
            access_token = response.data['access']
