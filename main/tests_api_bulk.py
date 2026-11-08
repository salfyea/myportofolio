"""Bulk delete of skills: owner only, validated, atomic and CSRF protected."""

import uuid

from django.contrib.auth.models import Group, User
from django.core.cache import cache
from django.db import connection
from django.test import override_settings
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Skill


class SkillBulkDeleteTest(APITestCase):
    def setUp(self):
        cache.clear()
        self.owner = User.objects.create_superuser("owner", "o@example.com", "pw-owner-1")
        self.editor = User.objects.create_user("editor", password="pw-editor-1")
        self.editor.groups.add(Group.objects.get_or_create(name="Editor")[0])
        self.visitor = User.objects.create_user("visitor", password="pw-visitor-1")
        self.url = reverse("api:skill-bulk-delete")
        self.baseline = Skill.objects.count()
        self.skills = [
            Skill.objects.create(name=f"Zzbulk{i}", icon_url="https://x.io/b.svg") for i in range(5)
        ]

    def ids(self, *skills):
        return [str(skill.id) for skill in skills]

    def assertNothingDeleted(self):
        self.assertEqual(Skill.objects.count(), self.baseline + 5)

    def test_owner_deletes_the_selected_skills_and_gets_the_count(self):
        self.client.force_authenticate(self.owner)
        response = self.client.post(self.url, {"ids": self.ids(*self.skills[:3])}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"deleted": 3})
        remaining = Skill.objects.filter(pk__in=[s.pk for s in self.skills])
        self.assertEqual(sorted(remaining.values_list("name", flat=True)), ["Zzbulk3", "Zzbulk4"])
        self.assertEqual(Skill.objects.count(), self.baseline + 2)

    def test_only_the_owner_may_bulk_delete(self):
        for user in (None, self.visitor, self.editor):
            self.client.force_authenticate(user)
            response = self.client.post(self.url, {"ids": self.ids(*self.skills)}, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, user)
        self.assertNothingDeleted()

    def test_guest_is_told_to_log_in(self):
        response = self.client.post(self.url, {"ids": self.ids(self.skills[0])}, format="json")
        self.assertIn("login", response.data["detail"].lower())

    def test_invalid_bodies_are_rejected_without_deleting_anything(self):
        self.client.force_authenticate(self.owner)
        cases = (
            ({}, "wajib diisi"),
            ({"ids": []}, "tidak boleh kosong"),
            ({"ids": "not-a-list"}, "daftar"),
            ({"ids": ["not-a-uuid"]}, "tidak valid"),
            ({"ids": [str(uuid.uuid4())] * 101}, "terlalu banyak"),
            ({"ids": self.ids(self.skills[0]) + [123456]}, "tidak valid"),
        )
        for payload, expected in cases:
            response = self.client.post(self.url, payload, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, payload)
            self.assertIn(expected, " ".join(map(str, response.data["ids"])).lower(), payload)
        self.assertNothingDeleted()

    def test_unknown_and_repeated_ids_are_harmless(self):
        self.client.force_authenticate(self.owner)
        target = self.skills[0]
        payload = {"ids": [str(target.id), str(target.id), str(uuid.uuid4())]}
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"deleted": 1})
        self.assertEqual(Skill.objects.count(), self.baseline + 4)

    def test_stars_go_away_with_the_skills_but_users_stay(self):
        self.skills[0].starred_by.add(self.visitor)
        self.client.force_authenticate(self.owner)
        self.client.post(self.url, {"ids": self.ids(self.skills[0])}, format="json")
        self.assertTrue(User.objects.filter(pk=self.visitor.pk).exists())
        self.assertEqual(self.visitor.starred_skills.count(), 0)

    def test_cost_does_not_grow_with_the_number_of_skills(self):
        self.client.force_authenticate(self.owner)
        with CaptureQueriesContext(connection) as few:
            self.client.post(self.url, {"ids": self.ids(*self.skills[:2])}, format="json")
        extra = [Skill.objects.create(name=f"Zzmore{i}", icon_url="https://x.io/m.svg") for i in range(30)]
        with CaptureQueriesContext(connection) as many:
            self.client.post(self.url, {"ids": self.ids(*extra)}, format="json")
        self.assertEqual(len(many), len(few))

    def test_get_is_not_allowed(self):
        self.client.force_authenticate(self.owner)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertNothingDeleted()

    def test_a_session_request_without_csrf_token_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="pw-owner-1"))
        response = client.post(self.url, {"ids": self.ids(*self.skills)}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNothingDeleted()

    @override_settings(REST_FRAMEWORK={
        "DEFAULT_THROTTLE_RATES": {"api_write": "1/min", "api_star": "1/min"},
        "EXCEPTION_HANDLER": "main.api_errors.exception_handler",
    })
    def test_counts_as_a_write_for_throttling(self):
        self.client.force_authenticate(self.owner)
        self.client.post(self.url, {"ids": self.ids(self.skills[0])}, format="json")
        response = self.client.post(self.url, {"ids": self.ids(self.skills[1])}, format="json")
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertEqual(Skill.objects.count(), self.baseline + 4)
