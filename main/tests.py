import json

from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Project


class MainTest(TestCase):
    def setUp(self):
        # Rate-limit counters live in the cache and would leak between tests.
        cache.clear()
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(
            response,
            f'href="{reverse("main:show_experience")}"',
        )

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(
            response,
            f'href="{reverse("main:show_main")}"',
        )

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(
            response,
            "Belum ada pengalaman yang ditambahkan.",
        )

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")

    def test_profile_bio_has_word_spacing(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertContains(
            response,
            "interests in product management",
        )

    def test_profile_has_no_static_experience_cards(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertNotContains(response, "VPIC Business Development")
        self.assertContains(response, 'id="experience"')

    def test_page_titles_are_unique(self):
        for name, title in (
            ("main:show_main", "Salwa Alifia Putri - Portofolio"),
            ("main:show_experience", "Experience - Salwa Alifia Putri"),
        ):
            with self.subTest(page=name):
                response = self.client.get(reverse(name))

                self.assertContains(response, "<title>", count=1)
                self.assertContains(
                    response,
                    f"<title>{title}</title>",
                )

    def test_brand_returns_to_profile(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(
            response,
            '<a href="/" class="brand">Salwa Alifia Putri</a>',
            html=True,
        )


class ProjectTest(TestCase):
    def setUp(self):
        # Rate-limit counters live in the cache and would leak between tests.
        cache.clear()
        self.project = Project.objects.create(
            title="Portfolio Django",
            description="Portfolio dinamis dengan Django.",
            category="Web Development",
            link="https://example.com/portfolio",
        )
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password"
        )
        self.visitor = User.objects.create_user(
            username="visitor", password="test-password"
        )
        self.delete_url = reverse(
            "main:delete_project", kwargs={"project_id": self.project.id}
        )
        self.star_url = reverse(
            "main:toggle_star", kwargs={"project_id": self.project.id}
        )
        self.form_data = {
            "title": "Data Delivery API",
            "description": "Endpoint JSON untuk project.",
            "category": "Backend",
            "link": "https://example.com/api",
        }

    def test_projects_page_renders_ajax_shell(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")
        for element_id in ("loading", "error", "empty", "grid", "search-input"):
            self.assertContains(response, f'id="{element_id}"')

    def test_projects_page_script_uses_drf_endpoints(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, reverse("api:project-list"))
        self.assertContains(response, "api/v1/projects/00000000-0000-0000-0000-000000000000/")
        self.assertNotContains(response, reverse("main:get_projects_json"))
        # The page must always set the csrftoken cookie for AJAX writes.
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_projects_page_renders_for_every_role(self):
        for user in (None, self.visitor, self.owner):
            if user:
                self.client.force_login(user)
            response = self.client.get(reverse("main:show_projects"))

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "api/v1/projects/")
            self.assertEqual(
                'id="add-project-modal"' in response.content.decode(),
                bool(user and user.is_superuser),
            )

    def test_projects_page_keeps_title_query_in_search_box(self):
        response = self.client.get(reverse("main:show_projects"), {"title": "django"})

        self.assertContains(response, 'value="django"')

    def test_projects_json_endpoint_returns_serialized_projects(self):
        response = self.client.get(reverse("main:get_projects_json"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        payload = json.loads(response.content)
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["pk"], str(self.project.pk))
        self.assertEqual(payload[0]["fields"]["title"], self.project.title)
        self.assertEqual(payload[0]["fields"]["category"], self.project.category)
        self.assertEqual(payload[0]["fields"]["star_count"], 0)
        self.assertFalse(payload[0]["fields"]["is_starred"])

    def test_projects_json_endpoint_filters_by_title(self):
        Project.objects.create(
            title="Mobile App",
            description="Aplikasi mobile.",
            category="Mobile Development",
        )

        response = self.client.get(
            reverse("main:get_projects_json"),
            {"title": "django"},
        )

        payload = json.loads(response.content)
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["fields"]["title"], self.project.title)

    def test_projects_json_reports_stars_per_user(self):
        self.project.starred_by.add(self.visitor)

        self.client.force_login(self.visitor)
        fields = json.loads(
            self.client.get(reverse("main:get_projects_json")).content
        )[0]["fields"]
        self.assertTrue(fields["is_starred"])
        self.assertEqual(fields["star_count"], 1)
        self.assertEqual(fields["starred_by_names"], ["visitor"])

        self.client.force_login(self.owner)
        fields = json.loads(
            self.client.get(reverse("main:get_projects_json")).content
        )[0]["fields"]
        self.assertFalse(fields["is_starred"])

    def test_create_project_form_requires_login(self):
        response = self.client.post(reverse("main:create_project"), self.form_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response["Location"].startswith("/login/"))
        self.assertFalse(Project.objects.filter(title="Data Delivery API").exists())

    def test_create_project_form_forbidden_for_visitor(self):
        self.client.force_login(self.visitor)

        response = self.client.post(reverse("main:create_project"), self.form_data)

        self.assertEqual(response.status_code, 403)
        self.assertFalse(Project.objects.filter(title="Data Delivery API").exists())

    def test_create_project_form_saves_project_for_owner(self):
        self.client.force_login(self.owner)

        response = self.client.post(reverse("main:create_project"), self.form_data)

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertTrue(Project.objects.filter(title="Data Delivery API").exists())

    def test_create_project_ajax_for_owner(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse("main:create_project_ajax"), self.form_data
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Project.objects.filter(title="Data Delivery API").exists())

    def test_create_project_ajax_rejects_invalid_input(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse("main:create_project_ajax"), {**self.form_data, "title": "   "}
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.json()["errors"])

    def test_create_project_ajax_forbidden_for_visitor_and_guest(self):
        for user in (self.visitor, None):
            if user:
                self.client.force_login(user)
            response = self.client.post(
                reverse("main:create_project_ajax"), self.form_data
            )

            self.assertEqual(response.status_code, 403)
        self.assertEqual(Project.objects.count(), 1)

    def test_create_project_ajax_requires_post(self):
        self.client.force_login(self.owner)

        response = self.client.get(reverse("main:create_project_ajax"))

        self.assertEqual(response.status_code, 405)

    def test_delete_project_requires_login(self):
        response = self.client.post(self.delete_url)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response["Location"].startswith("/login/"))
        self.assertTrue(Project.objects.filter(pk=self.project.id).exists())

    def test_delete_project_forbidden_for_visitor(self):
        self.client.force_login(self.visitor)

        response = self.client.post(self.delete_url)

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Project.objects.filter(pk=self.project.id).exists())

    def test_delete_project_get_does_not_delete(self):
        self.client.force_login(self.owner)

        response = self.client.get(self.delete_url)

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertTrue(Project.objects.filter(pk=self.project.id).exists())

    def test_delete_project_post_removes_project_for_owner(self):
        self.client.force_login(self.owner)

        response = self.client.post(self.delete_url)

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_toggle_star_adds_then_removes_star(self):
        self.client.force_login(self.visitor)

        self.client.post(self.star_url)
        self.assertEqual(self.project.starred_by.count(), 1)

        self.client.post(self.star_url)
        self.assertEqual(self.project.starred_by.count(), 0)

    def test_toggle_star_requires_login(self):
        response = self.client.post(self.star_url)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response["Location"].startswith("/login/"))
        self.assertEqual(self.project.starred_by.count(), 0)
