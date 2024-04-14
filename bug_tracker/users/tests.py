from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import CustomUser


class CustomUserManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user: CustomUser = User.objects.create_user(
            email="normal@test.com", first_name="John", last_name="Doe", password="test"
        )

        self.assertEqual(user.email, "normal@test.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(AttributeError):
            self.assertIsInstance(user.username)

        with self.assertRaises(TypeError):
            User.objects.create_user()

        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="", first_name="", last_name="", password="test"
            )

    def test_create_superuser(self):
        User = get_user_model()
        user: CustomUser = User.objects.create_superuser(
            email="super@test.com", first_name="John", last_name="Doe", password="test"
        )

        self.assertEqual(user.email, "super@test.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class CustomUserTests(TestCase):
    def test_custom_user(self):
        User = get_user_model()
        user: CustomUser = User.objects.create_user(
            email="normal@test.com", first_name="John", last_name="Doe", password="test"
        )

        self.assertEqual(str(user), "John Doe")
        self.assertTrue(user.is_developer)
        self.assertFalse(user.is_manager)
