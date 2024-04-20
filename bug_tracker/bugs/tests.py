from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser

from .models import Bug


class BugModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        user = User.objects.create_user(
            email="normal@test.com", first_name="John", last_name="Doe", password="test"
        )

        Bug.objects.create(
            title="A Title",
            severity="Minor",
            status="Open",
            description="This is a description",
            bug_creator=user,
            assignee=user,
        )

    def test_title_verbose_name(self):
        bug = Bug.objects.get(pk=1)
        verbose_name = bug._meta.get_field("title").verbose_name

        self.assertEqual(verbose_name, "title")

    def test_title_max_length(self):
        bug = Bug.objects.get(pk=1)
        max_length = bug._meta.get_field("title").max_length

        self.assertEqual(max_length, 255)

    def test_title_not_blankable(self):
        bug = Bug.objects.get(pk=1)
        blank = bug._meta.get_field("title").blank

        self.assertFalse(blank)

    def test_title_severity_verbose_name(self):
        bug = Bug.objects.get(pk=1)
        verbose_name = bug._meta.get_field("severity").verbose_name

        self.assertEqual(verbose_name, "severity")

    def test_severity_max_length(self):
        bug = Bug.objects.get(pk=1)
        max_length = bug._meta.get_field("severity").max_length

        self.assertEqual(max_length, 8)

    def test_severity_not_blankable(self):
        bug = Bug.objects.get(pk=1)
        blank = bug._meta.get_field("severity").blank

        self.assertFalse(blank)

    def test_title_status_verbose_name(self):
        bug = Bug.objects.get(pk=1)
        verbose_name = bug._meta.get_field("status").verbose_name

        self.assertEqual(verbose_name, "status")

    def test_status_max_length(self):
        bug = Bug.objects.get(pk=1)
        max_length = bug._meta.get_field("status").max_length

        self.assertEqual(max_length, 6)

    def test_status_not_blankable(self):
        bug = Bug.objects.get(pk=1)
        blank = bug._meta.get_field("status").blank

        self.assertFalse(blank)

    def test_title_description_verbose_name(self):
        bug = Bug.objects.get(pk=1)
        verbose_name = bug._meta.get_field("description").verbose_name

        self.assertEqual(verbose_name, "description")

    def test_description_not_blankable(self):
        bug = Bug.objects.get(pk=1)
        blank = bug._meta.get_field("description").blank

        self.assertFalse(blank)

    def test_bug_created_verbose_name(self):
        bug = Bug.objects.get(pk=1)
        verbose_name = bug._meta.get_field("bug_created").verbose_name

        self.assertEqual(verbose_name, "created at")

    def test_title_bug_creator_verbose_name(self):
        bug = Bug.objects.get(pk=1)
        verbose_name = bug._meta.get_field("bug_creator").verbose_name

        self.assertEqual(verbose_name, "creator")

    def test_bug_creator_nullable(self):
        bug = Bug.objects.get(pk=1)
        nullable = bug._meta.get_field("bug_creator").null

        self.assertTrue(nullable)

    def test_title_assignee_verbose_name(self):
        bug = Bug.objects.get(pk=1)
        verbose_name = bug._meta.get_field("assignee").verbose_name

        self.assertEqual(verbose_name, "assignee")

    def test_assignee_nullable(self):
        bug = Bug.objects.get(pk=1)
        nullable = bug._meta.get_field("assignee").null

        self.assertTrue(nullable)

    def test_bug_str(self):
        bug = Bug.objects.get(pk=1)

        self.assertEqual(str(bug), "A Title")


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

    def test_view_from_contains_assignee_when_manager(self):
        self.client.login(username="manager@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_create"))

        self.assertContains(response, "Assignee")

    def test_view_from_does_not_contains_assignee_when_developer(self):
        self.client.login(username="normal@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_create"))

        self.assertNotContains(response, "Assignee")
