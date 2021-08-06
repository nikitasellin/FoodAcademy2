import os

from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from courses.models import Course


class TestViews(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title='Index test',
            description='Test test test'
        )
        User = get_user_model()
        self.admin_email = os.environ.get('ADMIN_USER')
        self.admin_password = os.environ.get('ADMIN_PASSWORD')
        self.admin = User.objects.create_superuser(
            email=self.admin_email,
            password=self.admin_password,
        )

    def test_index_anonymous(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Index test')
        self.assertContains(response, 'Вход')
        self.assertNotContains(response, 'Редактировать')

        self.assertIn('object_list', response.context)

    def test_user_login_view(self):
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'E-mail')
        self.assertContains(response, 'Пароль')

    def test_user_profile_view(self):
        pk = self.admin.id
        response = self.client.get(f'/users/profile/{pk}/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/users/login/', response.url)

        c = Client()
        logged_in = c.login(
            username=self.admin_email,
            password=self.admin_password,
        )
        self.assertTrue(logged_in)
        response = c.get(f'/users/profile/{pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'refresh')

    def test_index_superuser(self):
        c = Client()
        c.login(
            username=self.admin_email,
            password=self.admin_password,
        )
        response = c.get('/')
        self.assertContains(response, 'Редактировать')
