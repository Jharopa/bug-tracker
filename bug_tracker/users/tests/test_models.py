from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import CustomUser


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
