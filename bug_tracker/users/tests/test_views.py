from django.contrib.auth import get_user, get_user_model
from django.test import TestCase
from django.urls import reverse


class UserLoginViewTests(TestCase):
    def test_view_url_at_correct_location(self):
        response = self.client.get("/login/")

        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("users:login"))

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("users:login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")


class UserLogoutViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        User.objects.create_user(
            email="normal@test.com", first_name="John", last_name="Doe", password="test"
        )

    def test_view_url_at_correct_location(self):
        response = self.client.get("/logout/")

        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("users:logout"))

        self.assertEqual(response.status_code, 302)

    def test_view_redirects_to_login(self):
        response = self.client.get(reverse("users:logout"))

        self.assertRedirects(response, "/login/")

    def test_view_user_is_logged_out(self):
        self.client.login(username="normal@test.com", password="test")
        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

        self.client.get(reverse("users:logout"))
        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)
