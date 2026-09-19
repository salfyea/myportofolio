import json

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Project


class MainTest(TestCase):
    def setUp(self):
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
        self.project = Project.objects.create(
            title="Portfolio Django",
            description="Portfolio dinamis dengan Django.",
            category="Web Development",
            link="https://example.com/portfolio",
        )

    def test_projects_page_uses_project_data(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")
        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.description)
        self.assertContains(response, self.project.category)

    def test_projects_page_filters_by_title(self):
        Project.objects.create(
            title="Mobile App",
            description="Aplikasi mobile.",
            category="Mobile Development",
        )

        response = self.client.get(
            reverse("main:show_projects"),
            {"title": "django"},
        )

        self.assertContains(response, self.project.title)
        self.assertNotContains(response, "Mobile App")
        self.assertContains(response, "django")

    def test_projects_json_endpoint_returns_serialized_projects(self):
        response = self.client.get(reverse("main:get_projects_json"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        payload = json.loads(response.content)
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["model"], "main.project")
        self.assertEqual(payload[0]["fields"]["title"], self.project.title)

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

    def test_create_project_form_saves_project(self):
        response = self.client.post(
            reverse("main:create_project"),
            {
                "title": "Data Delivery API",
                "description": "Endpoint JSON untuk project.",
                "category": "Backend",
                "link": "https://example.com/api",
            },
        )

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertTrue(
            Project.objects.filter(title="Data Delivery API").exists()
        )

    def test_delete_project_requires_post(self):
        delete_url = reverse(
            "main:delete_project",
            kwargs={"project_id": self.project.id},
        )

        response = self.client.get(delete_url)

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertTrue(Project.objects.filter(pk=self.project.id).exists())

    def test_delete_project_post_removes_project(self):
        delete_url = reverse(
            "main:delete_project",
            kwargs={"project_id": self.project.id},
        )

        response = self.client.post(delete_url)

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())