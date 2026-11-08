"""Custom DRF permissions for the portfolio app."""

from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsPortfolioOwnerOrReadOnly(BasePermission):
    """Anyone can read; only a superuser can change data."""

    message = "Only the portfolio owner can change projects."

    def has_permission(self, request, view):
        """Allow reads for everyone and writes for superusers only."""
        return request.method in SAFE_METHODS or request.user.is_superuser


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    """Anyone can read; superusers can do everything; Editors can only edit."""

    message = (
        "Hanya pemilik portofolio yang dapat menambah atau menghapus data, "
        "dan hanya pemilik atau Editor yang dapat mengubahnya."
    )

    def has_permission(self, request, view):
        """Reads: anyone. PUT and PATCH: Editor or owner. POST and DELETE: owner only."""
        if request.method in SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return (
            request.method in ("PUT", "PATCH")
            and request.user.groups.filter(name="Editor").exists()
        )
