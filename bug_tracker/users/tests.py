from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import CustomUser


class CustomUserManagersTests(TestCase):
    User = get_user_model()

    @classmethod
    def setUpTestData(cls):
        cls.User.objects.create_user(
            email="normal@test.com", first_name="John", last_name="Doe", password="test"
        )

        cls.User.objects.create_superuser(
            email="super@test.com", first_name="John", last_name="Doe", password="test"
        )

    def test_create_user_email(self):
        user: CustomUser = self.User.objects.get(pk=1)

        self.assertEqual(user.email, "normal@test.com")

    def test_create_user_first_name(self):
        user: CustomUser = self.User.objects.get(pk=1)

        self.assertEqual(user.first_name, "John")

    def test_create_user_last_name(self):
        user: CustomUser = self.User.objects.get(pk=1)

        self.assertEqual(user.last_name, "Doe")

    def test_create_user_is_active(self):
        user: CustomUser = self.User.objects.get(pk=1)

        self.assertTrue(user.is_active)

    def test_create_user_is_not_staff(self):
        user: CustomUser = self.User.objects.get(pk=1)

        self.assertFalse(user.is_staff)

    def test_create_user_is_not_superuser(self):
        user: CustomUser = self.User.objects.get(pk=1)

        self.assertFalse(user.is_superuser)

    def test_create_user_no_values_rasies_type_error(self):
        with self.assertRaises(TypeError):
            self.User.objects.create_user()

    def test_create_user_empty_attributes_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                email="", first_name="", last_name="", password="test"
            )

    def test_create_superuser_is_active(self):
        user: CustomUser = self.User.objects.get(pk=2)

        self.assertTrue(user.is_active)

    def test_create_superuser_is_staff(self):
        user: CustomUser = self.User.objects.get(pk=2)

        self.assertTrue(user.is_staff)

    def test_create_superuser_is_superuser(self):
        user: CustomUser = self.User.objects.get(pk=2)

        self.assertTrue(user.is_superuser)


class CustomUserTests(TestCase):
    User = get_user_model()

    @classmethod
    def setUpTestData(cls):
        cls.User.objects.create_user(
            email="normal@test.com", first_name="John", last_name="Doe", password="test"
        )

    def test_custom_user_str(self):
        user: CustomUser = self.User.objects.get(pk=1)

        self.assertEqual(str(user), "John Doe")

    def test_custom_user_default_is_developer(self):
        user: CustomUser = self.User.objects.get(pk=1)

        self.assertTrue(user.is_developer)

    def test_custom_user_default_is_not_manager(self):
        user: CustomUser = self.User.objects.get(pk=1)

        self.assertFalse(user.is_manager)
