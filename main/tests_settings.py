"""Settings must be safe by default in production (no debug pages, secure cookies)."""

import json
import os
import subprocess
import sys

from django.conf import settings
from django.test import SimpleTestCase


def load_settings(**env):
    """Import the settings module in a clean subprocess with the given environment."""
    code = (
        "import json; import portofolio.settings as s; "
        "print(json.dumps({'debug': s.DEBUG, 'session': s.SESSION_COOKIE_SECURE, "
        "'csrf': s.CSRF_COOKIE_SECURE, 'hsts': s.SECURE_HSTS_SECONDS}))"
    )
    clean = {k: v for k, v in os.environ.items() if k not in ("PRODUCTION", "DEBUG")}
    clean.update({"SECRET_KEY": "x", **env})
    result = subprocess.run(
        [sys.executable, "-c", code], cwd=settings.BASE_DIR, env=clean,
        capture_output=True, text=True, check=True,
    )
    return json.loads(result.stdout.strip().splitlines()[-1])


class ProductionSettingsTest(SimpleTestCase):
    def test_production_turns_debug_off_and_secures_cookies(self):
        loaded = load_settings(PRODUCTION="True")
        self.assertFalse(loaded["debug"])
        self.assertTrue(loaded["session"])
        self.assertTrue(loaded["csrf"])
        self.assertEqual(loaded["hsts"], 3600)

    def test_development_keeps_debug_on_and_cookies_usable_over_http(self):
        loaded = load_settings(PRODUCTION="False")
        self.assertTrue(loaded["debug"])
        self.assertFalse(loaded["session"])
        self.assertFalse(loaded["csrf"])
        self.assertEqual(loaded["hsts"], 0)

    def test_debug_can_be_overridden_explicitly(self):
        self.assertFalse(load_settings(PRODUCTION="False", DEBUG="False")["debug"])
        self.assertTrue(load_settings(PRODUCTION="True", DEBUG="True")["debug"])
