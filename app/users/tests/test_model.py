from django.test import TestCase
from django.contrib.auth import get_user_model


class EmployeeManagerTestCase(TestCase):
    """
    CommonUser model tests.
    """

    def setUp(self):
        self.User = get_user_model()

    def test_create_user_ok(self):
        user = self.User.objects.create_user(
            email="user@selin.com.ru", password="testuser")
        self.assertEqual(user.email, "user@selin.com.ru")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNone(user.username)

    def test_create_user_nok(self):
        with self.assertRaises(TypeError):
            self.User.objects.create_user(username="user")
        with self.assertRaises(TypeError):
            self.User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            self.User.objects.create_user(email="", password="testuser")

    def test_create_superuser_ok(self):
        super_user = self.User.objects.create_superuser(
            email="superuser@selin.com.ru", password="testsuperuser")
        self.assertEqual(super_user.email, "superuser@selin.com.ru")
        self.assertTrue(super_user.is_active)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_superuser)
        self.assertIsNone(super_user.username)

    def test_create_superuser_nok(self):
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                email="superuser@selin.com.ru",
                password="testsuperuser",
                is_superuser=False)
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                email="superuser@selin.com.ru",
                password="testsuperuser",
                is_staff=False)
