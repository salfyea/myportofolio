"""API tests for skills (Individual Assignment 6), one case per portfolio role."""

import uuid

from django.contrib.auth.models import Group, User
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Skill


class SkillAPITest(APITestCase):
    def setUp(self):
        # Rate-limit counters live in the cache and would leak between tests.
        cache.clear()
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.editor = User.objects.create_user(
            username="editor", password="test-password", email="editor@example.com",
        )
        # Migration 0009 already seeds the Editor group in the test database.
        self.editor.groups.add(Group.objects.get_or_create(name="Editor")[0])
        self.visitor = User.objects.create_user(
            username="visitor", password="test-password", email="visitor@example.com",
        )
        # A data migration seeds skills, so the test skill gets a unique name and
        # counts are compared against a baseline instead of an absolute number.
        self.baseline_count = Skill.objects.count()
        self.skill = Skill.objects.create(
            name="Quokka", icon_url="https://example.com/quokka.svg", category="Language",
        )
        self.list_url = reverse("api:skill-list")
        self.detail_url = reverse("api:skill-detail", args=[self.skill.id])
        self.star_url = reverse("api:skill-star", args=[self.skill.id])
        self.payload = {
            "name": "Django", "icon_url": "https://example.com/django.svg",
            "category": "Framework",
        }

    def assertSkillUntouched(self):
        self.assertEqual(Skill.objects.count(), self.baseline_count + 1)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.name, "Quokka")
        self.assertEqual(self.skill.category, "Language")

    # --- reading -----------------------------------------------------------

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item = next(row for row in response.data if row["id"] == str(self.skill.id))
        self.assertEqual(item["star_count"], 0)
        self.assertFalse(item["is_starred"])
        self.assertNotIn("fields", item)
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"name": "QUOK"})
        self.assertEqual([row["id"] for row in response.data], [str(self.skill.id)])
        response = self.client.get(self.list_url, {"name": "not-found"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_category_filter_is_case_insensitive_and_exact(self):
        self.skill.category = "Zzcat"
        self.skill.save()
        response = self.client.get(self.list_url, {"category": "zzcat"})
        self.assertEqual([row["id"] for row in response.data], [str(self.skill.id)])
        # Exact match: a prefix of the category must not match.
        self.assertEqual(self.client.get(self.list_url, {"category": "zzc"}).data, [])

    def test_search_and_category_filters_combine(self):
        self.skill.category = "Zzcat"
        self.skill.save()
        response = self.client.get(self.list_url, {"name": "quok", "category": "Zzcat"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"name": "quok", "category": "other"})
        self.assertEqual(response.data, [])

    def test_ordering_by_stars_puts_most_starred_first(self):
        self.skill.starred_by.add(self.visitor, self.editor, self.owner)
        response = self.client.get(self.list_url, {"ordering": "stars"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.skill.id))
        self.assertEqual(response.data[0]["star_count"], 3)
        counts = [row["star_count"] for row in response.data]
        self.assertEqual(counts, sorted(counts, reverse=True))
        # Same number of rows as the default ordering: nothing is dropped or duplicated.
        self.assertEqual(len(response.data), len(self.client.get(self.list_url).data))

    def test_default_ordering_is_by_name(self):
        names = [row["name"] for row in self.client.get(self.list_url).data]
        self.assertEqual(names, [s.name for s in Skill.objects.order_by("name", "id")])

    def test_unknown_ordering_is_rejected(self):
        response = self.client.get(self.list_url, {"ordering": "created_at"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("ordering", response.data)

    def test_missing_skill(self):
        url = reverse("api:skill-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(
            self.client.delete(self.list_url).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_sensitive_account_data_is_not_exposed(self):
        self.skill.starred_by.add(self.visitor)
        body = self.client.get(self.list_url).content.decode()
        self.assertIn("visitor", body)
        for secret in ("visitor@example.com", "password", "pbkdf2"):
            self.assertNotIn(secret, body)

    # --- writing, role by role ---------------------------------------------

    def test_guest_and_regular_user_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"name": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertSkillUntouched()

    def test_editor_can_patch_and_put(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {"name": "Python 3"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.name, "Python 3")
        # PATCH is partial: untouched fields keep their values.
        self.assertEqual(self.skill.category, "Language")

        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.name, "Django")

    def test_editor_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertSkillUntouched()

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Skill.objects.filter(pk=response.data["id"], name="Django").exists())

    def test_owner_can_update_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.put(self.detail_url, {"name": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.patch(self.detail_url, {"name": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Skill.objects.filter(pk=self.skill.id).exists())

    def test_rejection_explains_why_in_the_response(self):
        # The page shows this text in a toast, so it must be readable, not generic.
        self.client.force_authenticate(user=self.editor)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("pemilik portofolio", response.data["detail"])

    def test_staff_flag_alone_grants_nothing(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.client.force_authenticate(user=self.visitor)
        self.assertEqual(self.client.patch(self.detail_url, {"name": "Changed"}, format="json").status_code, 403)
        self.assertSkillUntouched()

    # --- validation --------------------------------------------------------

    def test_validation_rejects_bad_input(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"name": "   "}, "name"),
            ({"name": "<b></b>"}, "name"),
            ({"icon_url": "javascript:alert(1)"}, "icon_url"),
            ({"icon_url": ""}, "icon_url"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, changes)
            self.assertIn(field, response.data)
        self.assertEqual(Skill.objects.count(), self.baseline_count + 1)

    def test_validation_strips_html_tags(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "name": " <script>alert(1)</script>Rust ",
            "category": "<i>Language</i>",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("<", response.data["name"])
        self.assertNotIn("<", response.data["category"])
        self.assertEqual(response.data["category"], "Language")

    def test_editor_patch_is_validated_too(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {"name": "<b></b>"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertSkillUntouched()

    # --- star --------------------------------------------------------------

    def test_star_requires_login(self):
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.skill.starred_by.count(), 0)

    def test_star_toggles_for_every_logged_in_role(self):
        for user in (self.visitor, self.editor, self.owner):
            self.client.force_authenticate(user=user)
            response = self.client.post(self.star_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data["is_starred"])
            self.assertTrue(self.skill.starred_by.filter(pk=user.pk).exists())
            response = self.client.post(self.star_url)
            self.assertFalse(response.data["is_starred"])
            self.assertFalse(self.skill.starred_by.filter(pk=user.pk).exists())

    def test_star_uses_request_user_not_request_body(self):
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(
            self.star_url, {"user": self.owner.id, "user_id": self.owner.id}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(self.skill.starred_by.all()), [self.visitor])

    def test_star_count_and_is_starred_are_per_viewer(self):
        self.skill.starred_by.add(self.visitor, self.editor)
        self.client.force_authenticate(user=self.visitor)
        data = self.client.get(self.detail_url).data
        self.assertEqual(data["star_count"], 2)
        self.assertTrue(data["is_starred"])
        self.assertEqual(sorted(data["starred_by_names"].split(", ")), ["editor", "visitor"])
        self.client.force_authenticate(user=self.owner)
        self.assertFalse(self.client.get(self.detail_url).data["is_starred"])

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(Skill.objects.get(pk=response.data["id"]).starred_by.count(), 0)

    # --- CSRF --------------------------------------------------------------

    def test_session_write_without_csrf_is_rejected(self):
        for username in ("owner", "editor", "visitor"):
            client = APIClient(enforce_csrf_checks=True)
            self.assertTrue(client.login(username=username, password="test-password"))
            self.assertEqual(client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(client.patch(self.detail_url, {"name": "Changed"}, format="json").status_code, 403)
            self.assertEqual(client.delete(self.detail_url).status_code, 403)
            self.assertEqual(client.post(self.star_url).status_code, 403)
        self.assertSkillUntouched()
        self.assertEqual(self.skill.starred_by.count(), 0)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        # The Browsable API form renders a real CSRF token into the response.
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class SkillPageTest(APITestCase):
    """The management page is a shell that talks to the API with fetch()."""

    def setUp(self):
        # Rate-limit counters live in the cache and would leak between tests.
        cache.clear()
        self.editor = User.objects.create_user(username="editor", password="test-password")
        self.editor.groups.add(Group.objects.get_or_create(name="Editor")[0])
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.url = reverse("main:show_skills_manage")

    def get_page(self, username=None):
        client = self.client_class()
        if username:
            client.login(username=username, password="test-password")
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response

    def test_page_uses_skill_api_endpoints(self):
        page = self.get_page().content.decode()
        for url in (
            reverse("api:skill-list"),
            reverse("api:skill-detail", args=[uuid.UUID(int=0)]),
            reverse("api:skill-star", args=[uuid.UUID(int=0)]),
        ):
            self.assertIn(url, page)

    def test_modals_are_rendered_only_for_permitted_roles(self):
        add_modal, edit_modal = 'id="add-skill-modal"', 'id="edit-skill-modal"'
        expected = {
            None: (False, False),
            "visitor": (False, False),
            "editor": (False, True),
            "owner": (True, True),
        }
        for username, (has_add, has_edit) in expected.items():
            page = self.get_page(username).content.decode()
            self.assertEqual(add_modal in page, has_add, username)
            self.assertEqual(edit_modal in page, has_edit, username)

    def test_page_sets_csrf_cookie_for_every_role(self):
        for username in (None, "visitor", "editor", "owner"):
            self.assertIn("csrftoken", self.get_page(username).cookies, username)

    def test_page_has_category_and_sort_controls(self):
        page = self.get_page().content.decode()
        self.assertIn('id="skills-category-select"', page)
        self.assertIn('id="skills-sort-select"', page)
        self.assertIn('value="stars"', page)

    def test_page_loads_its_javascript_as_modules_not_inline(self):
        page = self.get_page().content.decode()
        self.assertIn('<script type="module" src="/static/js/skills/main.js">', page)
        self.assertNotIn("fetch(", page)

    def test_page_config_reflects_the_role(self):
        expected = {
            None: ("false", "false", "false"),
            "visitor": ("true", "false", "false"),
            "editor": ("true", "true", "false"),
            "owner": ("true", "true", "true"),
        }
        for username, (authenticated, can_edit, can_delete) in expected.items():
            page = self.get_page(username).content.decode()
            self.assertIn(f'data-authenticated="{authenticated}"', page, username)
            self.assertIn(f'data-can-edit="{can_edit}"', page, username)
            self.assertIn(f'data-can-delete="{can_delete}"', page, username)
