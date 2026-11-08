"""Model behaviour and query efficiency."""

import uuid

from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import IntegrityError, connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from rest_framework.test import APITestCase

from main.models import Experience, Project, Skill


class SkillModelTest(TestCase):
    def test_primary_key_is_a_generated_uuid(self):
        first = Skill.objects.create(name="Zza", icon_url="https://x.io/a.svg")
        second = Skill.objects.create(name="Zza", icon_url="https://x.io/a.svg")
        self.assertIsInstance(first.pk, uuid.UUID)
        self.assertNotEqual(first.pk, second.pk)

    def test_category_is_optional(self):
        self.assertEqual(Skill.objects.create(name="Zzb", icon_url="https://x.io/b.svg").category, "")

    def test_stars_are_per_user_and_deduplicated(self):
        user = User.objects.create_user("starrer", password="pw-starrer-1")
        skill = Skill.objects.create(name="Zzc", icon_url="https://x.io/c.svg")
        skill.starred_by.add(user, user)
        self.assertEqual(skill.starred_by.count(), 1)
        self.assertEqual(list(user.starred_skills.all()), [skill])

    def test_deleting_a_user_removes_only_their_stars(self):
        user = User.objects.create_user("gone", password="pw-gone-1")
        skill = Skill.objects.create(name="Zzd", icon_url="https://x.io/d.svg")
        skill.starred_by.add(user)
        user.delete()
        skill.refresh_from_db()
        self.assertEqual(skill.starred_by.count(), 0)

    def test_deleting_a_skill_keeps_the_users(self):
        user = User.objects.create_user("stays", password="pw-stays-1")
        skill = Skill.objects.create(name="Zze", icon_url="https://x.io/e.svg")
        skill.starred_by.add(user)
        skill.delete()
        self.assertTrue(User.objects.filter(pk=user.pk).exists())

    def test_name_is_required_by_the_database(self):
        with self.assertRaises(IntegrityError):
            Skill.objects.create(name=None, icon_url="https://x.io/f.svg")


class ProjectAndExperienceModelTest(TestCase):
    def test_project_stars_use_their_own_relation(self):
        user = User.objects.create_user("pstar", password="pw-pstar-1")
        project = Project.objects.create(title="P", description="d", category="c")
        project.starred_by.add(user)
        self.assertEqual(list(user.starred_projects.all()), [project])
        self.assertEqual(user.starred_skills.count(), 0)

    def test_experience_defaults_and_ongoing_flag(self):
        experience = Experience.objects.create(title="Intern", description="d")
        self.assertEqual(experience.category, "full-time")
        self.assertTrue(experience.is_ongoing)
        experience.ended_at = experience.started_at
        self.assertFalse(experience.is_ongoing)


class QueryEfficiencyTest(APITestCase):
    """Listing must cost the same number of queries however many rows exist."""

    def setUp(self):
        cache.clear()
        self.viewer = User.objects.create_user("viewer", password="pw-viewer-1")
        self.client.force_authenticate(self.viewer)

    def make_skills(self, count):
        for i in range(count):
            skill = Skill.objects.create(name=f"Zzq{Skill.objects.count()}-{i}", icon_url="https://x.io/q.svg")
            skill.starred_by.add(self.viewer)

    def count_queries(self, url, **params):
        with CaptureQueriesContext(connection) as queries:
            self.assertEqual(self.client.get(url, params).status_code, 200)
        return len(queries)

    def test_skill_list_does_not_query_per_skill(self):
        url = reverse("api:skill-list")
        self.make_skills(2)
        few = self.count_queries(url)
        self.make_skills(40)
        self.assertEqual(self.count_queries(url), few)

    def test_filtering_and_star_ordering_stay_constant_too(self):
        url = reverse("api:skill-list")
        self.make_skills(2)
        few = self.count_queries(url, ordering="stars", category="")
        self.make_skills(40)
        self.assertEqual(self.count_queries(url, ordering="stars", category=""), few)

    def test_project_list_does_not_query_per_project(self):
        url = reverse("api:project-list")
        for i in range(2):
            Project.objects.create(title=f"P{i}", description="d", category="c").starred_by.add(self.viewer)
        few = self.count_queries(url)
        for i in range(2, 30):
            Project.objects.create(title=f"P{i}", description="d", category="c").starred_by.add(self.viewer)
        self.assertEqual(self.count_queries(url), few)
