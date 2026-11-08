"""Security tests: custom decorators, rate limiting and API throttling."""

import uuid

from django.contrib.auth.models import AnonymousUser, User
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase, TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APITestCase

from main.decorators import client_ip, rate_limit, superuser_required
from main.models import Skill

LIMITS = {"demo": (3, 60), "chat": (3, 60), "auth": (3, 60)}


class SuperuserRequiredTest(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = superuser_required(lambda request: HttpResponse("ok"))

    def request_as(self, user):
        request = self.factory.get("/")
        request.user = user
        return request

    def test_superuser_passes(self):
        self.assertEqual(self.view(self.request_as(User(is_superuser=True))).status_code, 200)

    def test_regular_user_and_guest_are_denied(self):
        for user in (User(is_superuser=False), User(is_staff=True), AnonymousUser()):
            with self.assertRaises(PermissionDenied):
                self.view(self.request_as(user))


@override_settings(RATE_LIMITS=LIMITS)
class RateLimitDecoratorTest(SimpleTestCase):
    def setUp(self):
        cache.clear()
        self.factory = RequestFactory()
        self.view = rate_limit("demo")(lambda request: HttpResponse("ok"))

    def get(self, ip="1.1.1.1", user=None):
        request = self.factory.get("/", REMOTE_ADDR=ip)
        request.user = user or AnonymousUser()
        return self.view(request)

    def test_blocks_after_the_limit_with_retry_after(self):
        for _ in range(3):
            self.assertEqual(self.get().status_code, 200)
        response = self.get()
        self.assertEqual(response.status_code, 429)
        self.assertEqual(response["Retry-After"], "60")

    def test_each_client_has_its_own_budget(self):
        for _ in range(3):
            self.get(ip="1.1.1.1")
        self.assertEqual(self.get(ip="1.1.1.1").status_code, 429)
        self.assertEqual(self.get(ip="2.2.2.2").status_code, 200)

    def test_logged_in_users_are_counted_per_account_not_per_ip(self):
        first, second = User(pk=1), User(pk=2)
        for _ in range(3):
            self.get(user=first)
        self.assertEqual(self.get(user=first).status_code, 429)
        self.assertEqual(self.get(user=second).status_code, 200)

    def test_json_variant_returns_a_machine_readable_error(self):
        view = rate_limit("demo", json=True)(lambda request: HttpResponse("ok"))
        request = self.factory.get("/", REMOTE_ADDR="3.3.3.3")
        request.user = AnonymousUser()
        for _ in range(3):
            view(request)
        response = view(request)
        self.assertEqual(response.status_code, 429)
        self.assertIn(b"error", response.content)

    def test_only_listed_methods_are_counted(self):
        view = rate_limit("demo", methods=("POST",))(lambda request: HttpResponse("ok"))
        request = self.factory.get("/", REMOTE_ADDR="4.4.4.4")
        request.user = AnonymousUser()
        for _ in range(10):
            self.assertEqual(view(request).status_code, 200)


class ClientIpTest(SimpleTestCase):
    def test_uses_remote_addr_outside_production(self):
        request = RequestFactory().get("/", REMOTE_ADDR="9.9.9.9", HTTP_X_FORWARDED_FOR="1.2.3.4")
        with override_settings(PRODUCTION=False):
            self.assertEqual(client_ip(request), "9.9.9.9")

    def test_trusts_only_the_last_forwarded_hop_in_production(self):
        # The proxy appends the real client, so earlier entries are client-supplied.
        request = RequestFactory().get(
            "/", REMOTE_ADDR="10.0.0.1", HTTP_X_FORWARDED_FOR="6.6.6.6, 7.7.7.7",
        )
        with override_settings(PRODUCTION=True):
            self.assertEqual(client_ip(request), "7.7.7.7")


@override_settings(RATE_LIMITS=LIMITS)
class SensitiveViewLimitTest(TestCase):
    def setUp(self):
        cache.clear()

    def test_chat_endpoint_is_rate_limited(self):
        url = reverse("main:chat_with_ai")
        for _ in range(3):
            self.assertEqual(self.client.post(url, "{}", content_type="application/json").status_code, 400)
        response = self.client.post(url, "{}", content_type="application/json")
        self.assertEqual(response.status_code, 429)
        self.assertIn("error", response.json())

    def test_login_attempts_are_limited_but_the_page_still_loads(self):
        url = reverse("main:login")
        for _ in range(3):
            self.assertEqual(self.client.post(url, {"username": "x", "password": "y"}).status_code, 200)
        self.assertEqual(self.client.post(url, {"username": "x", "password": "y"}).status_code, 429)
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_correct_password_is_also_blocked_once_the_limit_is_hit(self):
        User.objects.create_user("real", password="correct-horse-1")
        url = reverse("main:login")
        for _ in range(3):
            self.client.post(url, {"username": "real", "password": "wrong"})
        response = self.client.post(url, {"username": "real", "password": "correct-horse-1"})
        self.assertEqual(response.status_code, 429)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_registration_is_limited(self):
        url = reverse("main:register")
        for i in range(3):
            self.client.post(url, {"username": f"u{i}", "password1": "x", "password2": "y"})
        self.assertEqual(self.client.post(url, {}).status_code, 429)


API_RATES = {"DEFAULT_THROTTLE_RATES": {"api_write": "2/min", "api_star": "2/min"}}


@override_settings(REST_FRAMEWORK=API_RATES)
class ApiThrottleTest(APITestCase):
    def setUp(self):
        cache.clear()
        self.owner = User.objects.create_superuser("owner", "o@x.io", "pw")
        self.visitor = User.objects.create_user("visitor", password="pw")
        self.skill = Skill.objects.create(name="Throttled", icon_url="https://x.io/t.svg")
        self.payload = {"name": "N", "icon_url": "https://x.io/n.svg", "category": "C"}

    def test_writes_are_throttled_per_account_but_reads_are_not(self):
        url = reverse("api:skill-list")
        self.client.force_authenticate(self.owner)
        for _ in range(2):
            self.assertEqual(self.client.post(url, self.payload, format="json").status_code, 201)
        response = self.client.post(url, self.payload, format="json")
        self.assertEqual(response.status_code, 429)
        self.assertIn("Retry-After", response)
        for _ in range(5):
            self.assertEqual(self.client.get(url).status_code, 200)

    def test_throttled_write_does_not_change_the_database(self):
        url = reverse("api:skill-list")
        self.client.force_authenticate(self.owner)
        for _ in range(3):
            self.client.post(url, self.payload, format="json")
        self.assertEqual(Skill.objects.filter(name="N").count(), 2)

    def test_star_is_throttled(self):
        url = reverse("api:skill-star", args=[self.skill.id])
        self.client.force_authenticate(self.visitor)
        self.assertEqual(self.client.post(url).status_code, 200)
        self.assertEqual(self.client.post(url).status_code, 200)
        self.assertEqual(self.client.post(url).status_code, 429)

    def test_one_account_does_not_exhaust_another_accounts_budget(self):
        url = reverse("api:skill-star", args=[self.skill.id])
        self.client.force_authenticate(self.visitor)
        for _ in range(3):
            self.client.post(url)
        self.client.force_authenticate(self.owner)
        self.assertEqual(self.client.post(url).status_code, 200)

    def test_project_endpoints_are_throttled_too(self):
        url = reverse("api:project-list")
        self.client.force_authenticate(self.owner)
        payload = {"title": "P", "description": "d", "category": "c", "link": "https://x.io/p"}
        codes = [self.client.post(url, payload, format="json").status_code for _ in range(3)]
        self.assertEqual(codes[-1], 429)

    def test_missing_project_is_still_404_when_not_throttled(self):
        self.client.force_authenticate(self.owner)
        url = reverse("api:project-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.patch(url, {"title": "x"}, format="json").status_code, 404)
