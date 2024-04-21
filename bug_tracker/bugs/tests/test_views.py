from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser

from ..models import Bug


class BugListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        User.objects.create_user(
            email="normal@test.com", first_name="John", last_name="Doe", password="test"
        )

    def test_view_logged_in(self):
        self.client.login(username="normal@test.com", password="test")
        response = self.client.get("")

        self.assertEqual(response.status_code, 200)

    def test_view_not_logged_in(self):
        response = self.client.get("")

        self.assertRedirects(response, "/login/?next=/")

    def test_view_url_accessible_by_name(self):
        self.client.login(username="normal@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_list"))

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username="normal@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_list"))

        self.assertTemplateUsed(response, "bugs/list.html")


class BugCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        User.objects.create_user(
            email="normal@test.com", first_name="John", last_name="Doe", password="test"
        )

        manager: CustomUser = User.objects.create_user(
            email="manager@test.com",
            first_name="Jane",
            last_name="Doe",
            password="test",
        )

        manager.user_type = CustomUser.MANAGER
        manager.save()

    def test_view_logged_in(self):
        self.client.login(username="normal@test.com", password="test")
        response = self.client.get("/create/")

        self.assertEqual(response.status_code, 200)

    def test_view_not_logged_in(self):
        response = self.client.get("/create/")

        self.assertRedirects(response, "/login/?next=/create/")

    def test_view_url_accessible_by_name(self):
        self.client.login(username="normal@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_create"))

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username="normal@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_create"))

        self.assertTemplateUsed(response, "bugs/create.html")

    def test_view_form_manager(self):
        self.client.login(username="manager@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_create"))

        self.assertContains(response, "Assignee")

    def test_view_form_contains_assignee_when_manager(self):
        self.client.login(username="manager@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_create"))

        self.assertContains(response, "Assignee")

    def test_view_form_does_not_contain_assignee_when_developer(self):
        self.client.login(username="normal@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_create"))

        self.assertNotContains(response, "Assignee")


class BugUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        user = User.objects.create_user(
            email="normal@test.com", first_name="John", last_name="Doe", password="test"
        )

        manager: CustomUser = User.objects.create_user(
            email="manager@test.com",
            first_name="Jane",
            last_name="Doe",
            password="test",
        )

        manager.user_type = CustomUser.MANAGER
        manager.save()

        Bug.objects.create(
            title="A Title",
            severity="Minor",
            status="Open",
            description="This is a description",
            bug_creator=user,
            assignee=user,
        )

    def test_view_logged_in(self):
        self.client.login(username="normal@test.com", password="test")
        response = self.client.get("/update/1/")

        self.assertEqual(response.status_code, 200)

    def test_view_not_logged_in(self):
        response = self.client.get("/update/1/")

        self.assertRedirects(response, "/login/?next=/update/1/")

    def test_view_bug_does_not_exist(self):
        self.client.login(username="manager@test.com", password="test")
        response = self.client.get("/update/2/")

        self.assertEqual(response.status_code, 404)

    def test_view_url_accessible_by_name(self):
        self.client.login(username="normal@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_update", args=[1]))

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username="normal@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_update", args=[1]))

        self.assertTemplateUsed(response, "bugs/update.html")

    def test_view_form_manager(self):
        self.client.login(username="manager@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_update", args=[1]))

        self.assertContains(response, "Assignee")

    def test_view_form_contains_assignee_when_manager(self):
        self.client.login(username="manager@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_update", args=[1]))

        self.assertContains(response, "Assignee")

    def test_view_form_does_not_contain_assignee_when_developer(self):
        self.client.login(username="normal@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_update", args=[1]))

        self.assertNotContains(response, "Assignee")

    def test_view_contains_bug_report_title_header(self):
        self.client.login(username="normal@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_update", args=[1]))

        self.assertContains(response, '<h1 class="card-header">Update A Title</h1>')


class BugDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        User.objects.create_user(
            email="normal@test.com", first_name="John", last_name="Doe", password="test"
        )

        manager: CustomUser = User.objects.create_user(
            email="manager@test.com",
            first_name="Jane",
            last_name="Doe",
            password="test",
        )

        manager.user_type = CustomUser.MANAGER
        manager.save()

        Bug.objects.create(
            title="A Title",
            severity="Minor",
            status="Open",
            description="This is a description",
            bug_creator=manager,
            assignee=manager,
        )

    def test_view_logged_in(self):
        self.client.login(username="manager@test.com", password="test")
        response = self.client.get("/delete/1/")

        self.assertEqual(response.status_code, 200)

    def test_view_not_logged_in(self):
        response = self.client.get("/delete/1/")

        self.assertRedirects(response, "/login/?next=/delete/1/")

    def test_view_bug_does_not_exist(self):
        self.client.login(username="manager@test.com", password="test")
        response = self.client.get("/delete/2/")

        self.assertEqual(response.status_code, 404)

    def test_view_url_accessible_by_name(self):
        self.client.login(username="manager@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_delete", args=[1]))

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username="manager@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_delete", args=[1]))

        self.assertTemplateUsed(response, "bugs/delete.html")

    def test_view_contains_bug_report_title_header(self):
        self.client.login(username="manager@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_delete", args=[1]))

        self.assertContains(response, '<h1 class="card-header">Delete A Title</h1>')

    def test_view_redirects_when_accessing_as_developer(self):
        self.client.login(username="normal@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_delete", args=[1]))

        self.assertRedirects(response, "/")
