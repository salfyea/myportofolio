"""Turn DRF's English error texts into messages the page can show in a toast.

The status codes stay exactly as DRF decides them. Only ``detail`` changes, so
clients keep reading the same ``{"detail": "..."}`` shape for every non-field error.
"""

import math

from django.http import Http404
from rest_framework import exceptions
from rest_framework.views import exception_handler as drf_exception_handler

LOGIN_REQUIRED = "Anda perlu login untuk melakukan tindakan ini."
NOT_FOUND = "Data tidak ditemukan."
UNREADABLE_BODY = "Isi permintaan tidak dapat dibaca. Pastikan formatnya JSON yang valid."


def exception_handler(exc, context):
    """Call DRF's handler, then replace ``detail`` with an Indonesian message.

    Permission errors keep the ``message`` defined on their permission class, and
    validation errors keep the per-field messages written in the serializers.
    """
    response = drf_exception_handler(exc, context)

    if response is None:
        return None

    if isinstance(exc, (exceptions.NotAuthenticated, exceptions.AuthenticationFailed)):
        message = LOGIN_REQUIRED
    elif isinstance(exc, (Http404, exceptions.NotFound)):
        message = NOT_FOUND
    elif isinstance(exc, exceptions.MethodNotAllowed):
        method = context["request"].method
        message = f"Metode {method} tidak diizinkan untuk alamat ini."
    elif isinstance(exc, exceptions.Throttled):
        seconds = math.ceil(exc.wait) if exc.wait else 1
        message = f"Terlalu banyak permintaan. Coba lagi dalam {seconds} detik."
    elif isinstance(exc, exceptions.ParseError):
        message = UNREADABLE_BODY
    else:
        return response

    response.data = {"detail": message}
    return response
