import os

from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model

from courses.models import Course
from users.models import Teacher


class TestCoursesFullAccessViewSet(APITestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title='test',
            description='test test'
        )
        self.teacher = Teacher.objects.create(
            first_name='Pen',
            last_name='Dehuai',
            email='pen@selin.com.ru',
        )
        User = get_user_model()
        admin_email = os.environ.get('ADMIN_USER')
        admin_password = os.environ.get('ADMIN_PASSWORD')
        self.admin = User.objects.create_superuser(
            email=admin_email,
            password=admin_password,
        )
        valid_data = {
            'email': admin_email,
            'password': admin_password,
        }
        response = self.client.post(
            '/api/token/obtain/',
            valid_data,
            format='json',
        )
        access_token = response.data['access']

        self.api_client = APIClient()
        self.api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    def test_status_code_anonymous_user(self):
        response = self.client.get('/api/full-access/courses/')
        self.assertEqual(response.status_code, 401)

    def test_status_code_valid_user(self):
        response = self.api_client.get('/api/full-access/courses/')
        self.assertEqual(response.status_code, 200)

    def test_list_data_len(self):
        response = self.api_client.get('/api/full-access/courses/')
        self.assertEqual(len(response.data['results']), 1)

    def test_list_data(self):
        response = self.api_client.get('/api/full-access/courses/')
        courses = response.data['results']
        for course in courses:
            self.assertEqual(course['title'], 'test')
            self.assertEqual(course['description'], 'test test')

    def test_post_status_code(self):
        data = {
            'title': 'Post test',
            'description': 'Created via API',
            'teachers': [self.teacher.id],
        }
        response = self.api_client.post(
            '/api/full-access/courses/',
            data,
            format='json',
        )
        self.assertEqual(response.status_code, 201)

    def test_patch_status_code(self):
        pk = self.course.id
        response = self.api_client.patch(
            f'/api/full-access/courses/{pk}/',
            {'title': 'Patch test'},
            format='json',
        )
        self.assertEqual(response.status_code, 200)

    def test_patch_data(self):
        pk = self.course.id
        response = self.api_client.patch(
            f'/api/full-access/courses/{pk}/',
            {'title': 'Patch test'},
            format='json',
        )
        course = Course.objects.get(id=pk)
        self.assertEqual(course.title, 'Patch test')
