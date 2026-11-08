"""DRF throttles that slow down abusive writes without affecting normal reading."""

from django.conf import settings
from rest_framework.permissions import SAFE_METHODS
from rest_framework.throttling import UserRateThrottle


class _UnsafeMethodThrottle(UserRateThrottle):
    """Count only requests that change data; GET, HEAD and OPTIONS stay free."""

    def get_rate(self):
        """Look up this scope's rate, e.g. ``"30/min"``."""
        # Read at call time so the rates in settings can be overridden in tests.
        return settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"][self.scope]

    def allow_request(self, request, view):
        """Skip counting for safe methods and defer to DRF for the rest."""
        if request.method in SAFE_METHODS:
            return True
        return super().allow_request(request, view)


class ApiWriteThrottle(_UnsafeMethodThrottle):
    """Create, update and delete requests, per account."""

    scope = "api_write"


class ApiStarThrottle(_UnsafeMethodThrottle):
    """Star toggles, per account. Looser than writes because toggling is cheap."""

    scope = "api_star"
