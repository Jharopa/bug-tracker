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

    def test_view_contains_search_as_manager(self):
        self.client.login(username="manager@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_list"))

        self.assertContains(
            response, '<input type="text" name="assignee" class="form-control">'
        )

    def test_view_doesnt_contain_search_as_developer(self):
        self.client.login(username="normal@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_list"))

        self.assertNotContains(
            response, '<input type="text" name="assignee" class="form-control">'
        )


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


class BugDetailViewTest(TestCase):
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
        response = self.client.get("/detail/1/")

        self.assertEqual(response.status_code, 200)

    def test_view_not_logged_in(self):
        response = self.client.get("/detail/1/")

        self.assertRedirects(response, "/login/?next=/detail/1/")

    def test_view_bug_does_not_exist(self):
        self.client.login(username="manager@test.com", password="test")
        response = self.client.get("/detail/2/")

        self.assertEqual(response.status_code, 404)

    def test_view_url_accessible_by_name(self):
        self.client.login(username="normal@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_detail", args=[1]))

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username="normal@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_detail", args=[1]))

        self.assertTemplateUsed(response, "bugs/detail.html")

    def test_view_form_manager(self):
        self.client.login(username="manager@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_detail", args=[1]))

        self.assertContains(response, "Assignee")

    def test_view_form_contains_assignee_when_manager(self):
        self.client.login(username="manager@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_detail", args=[1]))

        self.assertContains(response, "Assignee")

    def test_view_form_does_not_contain_assignee_when_developer(self):
        self.client.login(username="normal@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_detail", args=[1]))

        self.assertNotContains(response, "Assignee")

    def test_view_contains_bug_report_title_header(self):
        self.client.login(username="normal@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_detail", args=[1]))

        self.assertContains(response, '<h1 class="card-header">A Title Details</h1>')


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

    def test_view_post_request_deletes_bug_report(self):
        self.client.login(username="manager@test.com", password="test")

        bug = Bug.objects.get(id=1)
        self.assertIsNotNone(bug)

        self.client.post(reverse("bugs:bug_delete", args=[1]))

        with self.assertRaises(Bug.DoesNotExist):
            bug = Bug.objects.get(id=1)


class BugCloseViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        user = User.objects.create_user(
            email="normal@test.com", first_name="John", last_name="Doe", password="test"
        )

        User.objects.create_user(
            email="unassigned@test.com",
            first_name="Jane",
            last_name="Doe",
            password="test",
        )

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
        response = self.client.get("/close/1/")

        self.assertEqual(response.status_code, 200)

    def test_view_not_logged_in(self):
        response = self.client.get("/close/1/")

        self.assertRedirects(response, "/login/?next=/close/1/")

    def test_view_bug_does_not_exist(self):
        self.client.login(username="normal@test.com", password="test")
        response = self.client.get("/close/2/")

        self.assertEqual(response.status_code, 404)

    def test_view_url_accessible_by_name(self):
        self.client.login(username="normal@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_close", args=[1]))

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username="normal@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_close", args=[1]))

        self.assertTemplateUsed(response, "bugs/close.html")

    def test_view_contains_bug_report_title_header(self):
        self.client.login(username="normal@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_close", args=[1]))

        self.assertContains(response, '<h1 class="card-header">Close A Title</h1>')

    def test_view_post_request_closes_bug_report(self):
        self.client.login(username="normal@test.com", password="test")

        bug = Bug.objects.get(id=1)
        self.assertEqual(bug.status, "Open")

        self.client.post(reverse("bugs:bug_close", args=[1]))

        bug = Bug.objects.get(id=1)
        self.assertEqual(bug.status, "Closed")

    def test_view_unassigned_user_redirected(self):
        self.client.login(username="unassigned@test.com", password="test")
        response = self.client.get(reverse("bugs:bug_close", args=[1]))

        self.assertRedirects(response, "/")
