import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Project


class ProjectAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.project = Project.objects.create(
            title="Portfolio", description="My website", category="Web Development",
        )
        self.list_url = reverse("api:project-list")
        self.detail_url = reverse("api:project-detail", args=[self.project.id])
        self.star_url = reverse("api:project-star", args=[self.project.id])
        self.payload = {
            "title": "New project", "description": "A useful app", "category": "Backend",
            "link": "https://example.com/", "project_image_url": "",
        }

    def test_public_list(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.project.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "PORT"})
        self.assertEqual(len(response.data), 1)

        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_guest_and_visitor_cannot_create(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            response = self.client.post(self.list_url, self.payload, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(self.list_url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"link": "javascript:alert(1)"}, "link"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Project.objects.count(), 1)

    def test_html_tags_are_stripped_from_input(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            self.list_url,
            {**self.payload, "description": "<b>Bold</b> text", "category": "<i>Web</i>"},
            format="json",
        )

        self.assertEqual(response.data["description"], "Bold text")
        self.assertEqual(response.data["category"], "Web")

    def test_missing_project(self):
        url = reverse("api:project-detail", args=[uuid.uuid4()])

        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_update_or_delete(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            response = self.client.delete(self.detail_url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio")

    def test_visitor_gets_403_before_404_for_missing_project(self):
        self.client.force_authenticate(user=self.visitor)
        url = reverse("api:project-detail", args=[uuid.uuid4()])

        self.assertEqual(self.client.delete(url).status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_patch_changes_only_given_fields(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.patch(self.detail_url, {"title": "Updated"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Updated")
        self.assertEqual(self.project.description, "My website")

    def test_owner_put_requires_all_required_fields(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.put(self.detail_url, {"title": "Only title"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("description", response.data)

    def test_owner_put_replaces_project(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.put(self.detail_url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "New project")

    def test_owner_delete_returns_204_then_404(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_404_NOT_FOUND)

    def test_star_toggles_for_logged_in_user(self):
        self.client.force_authenticate(user=self.visitor)

        first = self.client.post(self.star_url)
        self.assertEqual(first.status_code, status.HTTP_200_OK)
        self.assertTrue(first.data["is_starred"])
        self.assertEqual(first.data["star_count"], 1)
        self.assertEqual(first.data["starred_by_names"], "visitor")

        second = self.client.post(self.star_url)
        self.assertFalse(second.data["is_starred"])
        self.assertEqual(second.data["star_count"], 0)

    def test_star_requires_login_and_post(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.client.get(self.star_url).status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.visitor)
        self.assertEqual(
            self.client.get(self.star_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_is_starred_depends_on_viewer(self):
        self.project.starred_by.add(self.visitor)

        self.client.force_authenticate(user=self.visitor)
        self.assertTrue(self.client.get(self.list_url).data[0]["is_starred"])

        self.client.force_authenticate(user=self.owner)
        self.assertFalse(self.client.get(self.list_url).data[0]["is_starred"])
