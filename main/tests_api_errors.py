"""Every API error shown in the page's toast must be readable Indonesian, with the right status."""

import uuid

from django.contrib.auth.models import Group, User
from django.core.cache import cache
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from main.models import Skill


class ApiErrorMessageTest(APITestCase):
    def setUp(self):
        cache.clear()
        self.owner = User.objects.create_superuser("owner", "o@example.com", "pw-owner-1")
        self.visitor = User.objects.create_user("visitor", password="pw-visitor-1")
        self.skill = Skill.objects.create(name="Zzerr", icon_url="https://x.io/e.svg", category="Err")
        self.list_url = reverse("api:skill-list")
        self.detail_url = reverse("api:skill-detail", args=[self.skill.id])
        self.star_url = reverse("api:skill-star", args=[self.skill.id])

    def detail(self, response):
        return response.data["detail"]

    def test_guest_gets_a_login_prompt_on_write_and_star(self):
        payload = {"name": "N", "icon_url": "https://x.io/n.svg"}
        for response in (
            self.client.post(self.list_url, payload, format="json"),
            self.client.patch(self.detail_url, {"name": "X"}, format="json"),
            self.client.delete(self.detail_url),
            self.client.post(self.star_url),
        ):
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertIn("login", self.detail(response).lower())
            self.assertNotIn("credentials", self.detail(response))
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.name, "Zzerr")

    def test_missing_skill_says_it_was_not_found(self):
        response = self.client.get(reverse("api:skill-detail", args=[uuid.uuid4()]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.detail(response), "Data tidak ditemukan.")

    def test_wrong_method_names_the_method(self):
        self.client.force_authenticate(self.owner)
        response = self.client.delete(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertIn("DELETE", self.detail(response))
        self.assertIn("tidak diizinkan", self.detail(response))

    def test_malformed_json_is_explained(self):
        self.client.force_authenticate(self.owner)
        response = self.client.post(self.list_url, "{not json", content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("JSON", self.detail(response))

    @override_settings(REST_FRAMEWORK={
        "DEFAULT_THROTTLE_RATES": {"api_write": "1/min", "api_star": "1/min"},
        "EXCEPTION_HANDLER": "main.api_errors.exception_handler",
    })
    def test_throttled_request_says_when_to_retry(self):
        self.client.force_authenticate(self.owner)
        self.client.post(self.star_url)
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertIn("Terlalu banyak permintaan", self.detail(response))
        self.assertRegex(self.detail(response), r"\d+ detik")
        self.assertIn("Retry-After", response)

    def test_serializer_errors_are_indonesian(self):
        self.client.force_authenticate(self.owner)
        cases = (
            ({"name": "N", "icon_url": "bukan-url"}, "icon_url", "URL icon tidak valid."),
            ({"name": "N", "icon_url": ""}, "icon_url", "URL icon wajib diisi."),
            ({"icon_url": "https://x.io/n.svg"}, "name", "Nama skill wajib diisi."),
            ({"name": "x" * 101, "icon_url": "https://x.io/n.svg"}, "name", "terlalu panjang"),
            ({"name": "N", "icon_url": "https://x.io/n.svg", "category": "c" * 51}, "category", "terlalu panjang"),
        )
        for payload, field, expected in cases:
            response = self.client.post(self.list_url, payload, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, payload)
            self.assertIn(expected, " ".join(response.data[field]), payload)

    def test_editor_rejection_message_is_unchanged(self):
        editor = User.objects.create_user("editor", password="pw-editor-1")
        editor.groups.add(Group.objects.get_or_create(name="Editor")[0])
        self.client.force_authenticate(editor)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("pemilik", self.detail(response))
