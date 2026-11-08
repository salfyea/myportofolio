"""Custom security decorators for the portfolio's plain Django views."""

import functools

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse

RATE_LIMIT_MESSAGE = "Terlalu banyak permintaan. Silakan coba lagi sebentar lagi."


def superuser_required(view):
    """Allow only the portfolio owner; everyone else gets a 403.

    Stack it under ``@login_required`` so anonymous visitors are sent to the
    login page first, while logged-in users without the role see the 403 page.
    """

    @functools.wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return view(request, *args, **kwargs)

    return wrapper


def client_ip(request):
    """Best-effort client address used to key rate limits.

    Behind the production proxy ``REMOTE_ADDR`` is the proxy itself, which would
    put every visitor in one bucket. The proxy appends the real client to
    ``X-Forwarded-For``, so only the last entry is trusted; earlier entries
    are supplied by the client and could be forged.
    """
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if settings.PRODUCTION and forwarded:
        return forwarded.split(",")[-1].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


def _count_hit(key, window):
    """Increment a fixed-window counter and return the new count."""
    if cache.add(key, 1, timeout=window):
        return 1
    try:
        return cache.incr(key)
    except ValueError:
        # The key expired between add() and incr().
        cache.set(key, 1, timeout=window)
        return 1


def rate_limit(scope, *, json=False, methods=None):
    """Limit how often one client may call a view.

    ``settings.RATE_LIMITS[scope]`` holds ``(max_requests, window_seconds)``.
    Logged-in users are counted per account, anonymous visitors per IP address.
    ``methods`` restricts counting to some HTTP methods (all by default), and
    ``json=True`` answers with a JSON error for fetch() clients.
    """

    def decorator(view):
        @functools.wraps(view)
        def wrapper(request, *args, **kwargs):
            if methods is not None and request.method not in methods:
                return view(request, *args, **kwargs)

            limit, window = settings.RATE_LIMITS[scope]
            user = request.user
            ident = f"user:{user.pk}" if user.is_authenticated else f"ip:{client_ip(request)}"

            if _count_hit(f"ratelimit:{scope}:{ident}", window) > limit:
                if json:
                    response = JsonResponse({"error": RATE_LIMIT_MESSAGE}, status=429)
                else:
                    response = HttpResponse(RATE_LIMIT_MESSAGE, status=429)
                response["Retry-After"] = str(window)
                return response

            return view(request, *args, **kwargs)

        return wrapper

    return decorator
