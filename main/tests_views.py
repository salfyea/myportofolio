"""Tests for the server-rendered views, forms and models kept from Tutorials 3 to 5."""

import json
from types import SimpleNamespace
from unittest import mock

from django.contrib.auth.models import Group, User
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse
from google.api_core import exceptions as google_exceptions

from main.forms import ProjectForm, SkillForm
from main.models import Experience, Project, Skill


class RoleTestCase(TestCase):
    """Creates one account per role; seeded data means tests use unique names."""

    def setUp(self):
        cache.clear()
        self.owner = User.objects.create_superuser("owner", "o@example.com", "pw-owner-1")
        self.editor = User.objects.create_user("editor", password="pw-editor-1")
        self.editor.groups.add(Group.objects.get_or_create(name="Editor")[0])
        self.visitor = User.objects.create_user("visitor", password="pw-visitor-1")

    def login(self, user):
        self.client.force_login(user)


class ModelStringTest(TestCase):
    def test_str_returns_the_main_text_field(self):
        self.assertEqual(str(Project(title="Judul")), "Judul")
        self.assertEqual(str(Skill(name="Rust")), "Rust")
        self.assertEqual(str(Experience(title="Intern")), "Intern")


class FormCleaningTest(TestCase):
    def test_project_form_strips_tags_and_rejects_empty_title(self):
        form = ProjectForm({
            "title": " <b>Judul</b> ", "description": "<i>desk</i>", "category": "<u>Web</u>",
            "link": "https://example.com", "project_image_url": "",
        })
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["title"], "Judul")
        self.assertEqual(form.cleaned_data["description"], "desk")
        self.assertEqual(form.cleaned_data["category"], "Web")
        empty = ProjectForm({"title": "<b></b>", "description": "d", "category": "c"})
        self.assertIn("title", empty.errors)

    def test_skill_form_strips_tags_and_rejects_empty_name(self):
        form = SkillForm({"name": "<b>Py</b>", "icon_url": "https://x.io/a.svg", "category": "<i>Lang</i>"})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["name"], "Py")
        self.assertEqual(form.cleaned_data["category"], "Lang")
        self.assertIn("name", SkillForm({"name": "  ", "icon_url": "https://x.io/a.svg"}).errors)
        self.assertIn("icon_url", SkillForm({"name": "a", "icon_url": "javascript:alert(1)"}).errors)


class SkillJsonViewTest(RoleTestCase):
    def setUp(self):
        super().setUp()
        self.skill = Skill.objects.create(name="Zzquokka", icon_url="https://x.io/q.svg", category="Fun")
        self.skill.starred_by.add(self.visitor)

    def fields_for(self, response):
        return next(item["fields"] for item in response.json() if item["pk"] == str(self.skill.pk))

    def test_filters_by_name_and_reports_stars(self):
        response = self.client.get(reverse("main:get_skills_json"), {"name": "zzquo"})
        self.assertEqual([item["pk"] for item in response.json()], [str(self.skill.pk)])
        fields = self.fields_for(response)
        self.assertEqual(fields["star_count"], 1)
        self.assertEqual(fields["starred_by_names"], ["visitor"])
        self.assertFalse(fields["is_starred"])

    def test_is_starred_depends_on_the_viewer(self):
        self.login(self.visitor)
        self.assertTrue(self.fields_for(self.client.get(reverse("main:get_skills_json")))["is_starred"])

    def test_no_match_returns_an_empty_list(self):
        response = self.client.get(reverse("main:get_skills_json"), {"name": "nothing-like-this"})
        self.assertEqual(response.json(), [])


class ProjectFormViewTest(RoleTestCase):
    data = {
        "title": "Proyek Uji", "description": "Deskripsi", "category": "Web",
        "link": "https://example.com", "project_image_url": "",
    }

    def setUp(self):
        super().setUp()
        self.project = Project.objects.create(
            title="Lama", description="d", category="c", link="https://example.com/old",
        )
        self.edit_url = reverse("main:update_project", args=[self.project.id])

    def test_owner_sees_the_empty_add_form(self):
        self.login(self.owner)
        response = self.client.get(reverse("main:create_project"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects_form.html")

    def test_invalid_add_form_is_shown_again_without_saving(self):
        self.login(self.owner)
        before = Project.objects.count()
        response = self.client.post(reverse("main:create_project"), {**self.data, "title": "<b></b>"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Project.objects.count(), before)

    def test_editor_and_owner_can_edit_and_visitor_cannot(self):
        for user, allowed in ((self.editor, True), (self.owner, True), (self.visitor, False)):
            self.login(user)
            self.assertEqual(self.client.get(self.edit_url).status_code, 200 if allowed else 403)
            response = self.client.post(self.edit_url, {**self.data, "title": f"Oleh {user.username}"})
            self.project.refresh_from_db()
            if allowed:
                self.assertRedirects(response, reverse("main:show_projects"))
                self.assertEqual(self.project.title, f"Oleh {user.username}")
            else:
                self.assertEqual(response.status_code, 403)
                self.assertNotEqual(self.project.title, "Oleh visitor")

    def test_guest_is_sent_to_login(self):
        self.assertEqual(self.client.get(self.edit_url).status_code, 302)

    def test_invalid_edit_keeps_the_old_title(self):
        self.login(self.editor)
        response = self.client.post(self.edit_url, {**self.data, "title": "  "})
        self.assertEqual(response.status_code, 200)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Lama")


class SkillViewTest(RoleTestCase):
    data = {"name": "Zzskill", "icon_url": "https://x.io/s.svg", "category": "Tool"}

    def setUp(self):
        super().setUp()
        self.skill = Skill.objects.create(name="Zzold", icon_url="https://x.io/o.svg", category="Old")
        self.edit_url = reverse("main:update_skill", args=[self.skill.id])
        self.delete_url = reverse("main:delete_skill", args=[self.skill.id])
        self.baseline = Skill.objects.count()

    def test_manage_page_renders_for_every_role(self):
        for user in (None, self.visitor, self.editor, self.owner):
            if user:
                self.login(user)
            self.assertEqual(self.client.get(reverse("main:show_skills_manage")).status_code, 200)

    def test_only_the_owner_gets_the_add_form(self):
        url = reverse("main:create_skill")
        self.assertEqual(self.client.get(url).status_code, 302)
        for user in (self.visitor, self.editor):
            self.login(user)
            self.assertEqual(self.client.get(url).status_code, 403)
            self.assertEqual(self.client.post(url, self.data).status_code, 403)
        self.assertEqual(Skill.objects.count(), self.baseline)
        self.login(self.owner)
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertRedirects(self.client.post(url, self.data), reverse("main:show_skills_manage"))
        self.assertEqual(Skill.objects.count(), self.baseline + 1)

    def test_invalid_add_form_does_not_save(self):
        self.login(self.owner)
        response = self.client.post(reverse("main:create_skill"), {**self.data, "name": "<i></i>"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Skill.objects.count(), self.baseline)

    def test_ajax_create_by_role(self):
        url = reverse("main:create_skill_ajax")
        for user in (None, self.visitor, self.editor):
            if user:
                self.login(user)
            self.assertEqual(self.client.post(url, self.data).status_code, 403)
        self.assertEqual(Skill.objects.count(), self.baseline)
        self.login(self.owner)
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Skill.objects.filter(pk=response.json()["pk"]).exists())
        bad = self.client.post(url, {**self.data, "icon_url": "nope"})
        self.assertEqual(bad.status_code, 400)
        self.assertIn("icon_url", bad.json()["errors"])
        self.assertEqual(self.client.get(url).status_code, 405)

    def test_edit_form_by_role(self):
        self.assertEqual(self.client.get(self.edit_url).status_code, 302)
        self.login(self.visitor)
        self.assertEqual(self.client.post(self.edit_url, self.data).status_code, 403)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.name, "Zzold")
        for user in (self.editor, self.owner):
            self.login(user)
            self.assertEqual(self.client.get(self.edit_url).status_code, 200)
            response = self.client.post(self.edit_url, {**self.data, "name": f"Zz{user.username}"})
            self.assertRedirects(response, reverse("main:show_skills_manage"))
            self.skill.refresh_from_db()
            self.assertEqual(self.skill.name, f"Zz{user.username}")

    def test_invalid_edit_keeps_the_old_name(self):
        self.login(self.editor)
        self.assertEqual(self.client.post(self.edit_url, {**self.data, "name": " "}).status_code, 200)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.name, "Zzold")

    def test_delete_is_owner_only_and_needs_post(self):
        self.assertEqual(self.client.post(self.delete_url).status_code, 302)
        for user in (self.visitor, self.editor):
            self.login(user)
            self.assertEqual(self.client.post(self.delete_url).status_code, 403)
        self.login(self.owner)
        self.client.get(self.delete_url)
        self.assertTrue(Skill.objects.filter(pk=self.skill.pk).exists())
        self.assertRedirects(self.client.post(self.delete_url), reverse("main:show_skills_manage"))
        self.assertFalse(Skill.objects.filter(pk=self.skill.pk).exists())

    def test_star_toggle_needs_login_and_post(self):
        url = reverse("main:toggle_skill_star", args=[self.skill.id])
        self.assertEqual(self.client.post(url).status_code, 302)
        self.assertEqual(self.skill.starred_by.count(), 0)
        self.login(self.visitor)
        self.client.get(url)
        self.assertEqual(self.skill.starred_by.count(), 0)
        self.assertRedirects(self.client.post(url), reverse("main:show_main") + "#skills", fetch_redirect_response=False)
        self.assertEqual(self.skill.starred_by.count(), 1)
        self.client.post(url)
        self.assertEqual(self.skill.starred_by.count(), 0)


class AccountViewTest(RoleTestCase):
    def test_register_creates_an_account_and_redirects_to_login(self):
        response = self.client.post(reverse("main:register"), {
            "username": "newbie", "password1": "a-strong-pass-9", "password2": "a-strong-pass-9",
        })
        self.assertRedirects(response, reverse("main:login"))
        self.assertTrue(User.objects.filter(username="newbie").exists())

    def test_register_rejects_mismatched_passwords(self):
        response = self.client.post(reverse("main:register"), {
            "username": "newbie", "password1": "a-strong-pass-9", "password2": "different-pass-9",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="newbie").exists())

    def test_register_page_renders(self):
        self.assertEqual(self.client.get(reverse("main:register")).status_code, 200)

    def test_login_starts_a_session_and_sets_the_last_login_cookie(self):
        response = self.client.post(reverse("main:login"), {"username": "visitor", "password": "pw-visitor-1"})
        self.assertRedirects(response, reverse("main:show_main"))
        self.assertIn("last_login", response.cookies)
        self.assertIn("_auth_user_id", self.client.session)

    def test_wrong_password_does_not_log_in(self):
        response = self.client.post(reverse("main:login"), {"username": "visitor", "password": "wrong"})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout_ends_the_session_and_clears_the_cookie(self):
        self.login(self.visitor)
        response = self.client.post(reverse("main:logout"))
        self.assertRedirects(response, reverse("main:show_main"))
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertEqual(response.cookies["last_login"].value, "")

    def test_logout_by_get_is_refused_so_a_link_or_image_cannot_log_you_out(self):
        self.login(self.visitor)
        response = self.client.get(reverse("main:logout"))
        self.assertEqual(response.status_code, 405)
        self.assertIn("_auth_user_id", self.client.session)

    def test_logout_needs_a_csrf_token(self):
        from django.test import Client

        client = Client(enforce_csrf_checks=True)
        client.force_login(self.visitor)
        self.assertEqual(client.post(reverse("main:logout")).status_code, 403)
        self.assertIn("_auth_user_id", client.session)

    def test_nav_offers_logout_as_a_csrf_protected_form(self):
        self.login(self.visitor)
        page = self.client.get(reverse("main:show_main")).content.decode()
        self.assertIn(f'action="{reverse("main:logout")}"', page)
        self.assertIn('method="post"', page)
        self.assertNotIn(f'<a href="{reverse("main:logout")}">', page)


@override_settings(GEMINI_API_KEY="test-key")
class ChatViewTest(TestCase):
    def setUp(self):
        cache.clear()
        self.url = reverse("main:chat_with_ai")

    def post(self, payload):
        body = payload if isinstance(payload, str) else json.dumps(payload)
        return self.client.post(self.url, body, content_type="application/json")

    def fake_genai(self, text="Halo!", error=None):
        model = mock.Mock()
        if error:
            model.generate_content.side_effect = error
        else:
            model.generate_content.return_value = SimpleNamespace(text=text)
        genai = mock.Mock()
        genai.GenerativeModel.return_value = model
        return genai, model

    def test_returns_the_model_reply(self):
        genai, model = self.fake_genai("  Halo juga!  ")
        with mock.patch("main.views.genai", genai):
            response = self.post({"message": "  hai  "})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"reply": "Halo juga!"})
        model.generate_content.assert_called_once_with("hai")

    def test_rejects_bad_requests_before_calling_the_model(self):
        genai, model = self.fake_genai()
        with mock.patch("main.views.genai", genai):
            self.assertEqual(self.post("not json").status_code, 400)
            self.assertEqual(self.post({}).status_code, 400)
            self.assertEqual(self.post({"message": "   "}).status_code, 400)
            self.assertEqual(self.post({"message": 123}).status_code, 400)
        model.generate_content.assert_not_called()

    def test_get_is_not_allowed(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)

    @override_settings(GEMINI_API_KEY="")
    def test_missing_api_key_gives_503(self):
        self.assertEqual(self.post({"message": "hai"}).status_code, 503)

    def test_upstream_failures_map_to_clear_statuses(self):
        cases = (
            (google_exceptions.Unauthenticated("bad key"), 502, "GEMINI_API_KEY"),
            (google_exceptions.ServiceUnavailable("down"), 502, "Gagal menghubungi"),
            (RuntimeError("boom"), 500, "tak terduga"),
        )
        for error, status, text in cases:
            genai, _ = self.fake_genai(error=error)
            with mock.patch("main.views.genai", genai):
                response = self.post({"message": "hai"})
            self.assertEqual(response.status_code, status)
            self.assertIn(text, response.json()["error"])

    def test_empty_reply_gives_502(self):
        genai, _ = self.fake_genai(text="   ")
        with mock.patch("main.views.genai", genai):
            self.assertEqual(self.post({"message": "hai"}).status_code, 502)
