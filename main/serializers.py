"""Serializers for the REST API of the portfolio app."""

from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Project, Skill


class ProjectSerializer(serializers.ModelSerializer):
    """Serialize a ``Project`` along with its star information."""

    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "category",
            "link",
            "project_image_url",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]
        read_only_fields = ["id"]

    def get_star_count(self, obj):
        """Count the users who starred this project."""
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        """Whether the logged-in viewer starred this item; always False for guests."""
        request = self.context.get("request")

        if request is None or not request.user.is_authenticated:
            return False

        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        """List usernames only, so no email or password hash can leak through the relation."""
        return ", ".join(user.username for user in obj.starred_by.all())

    def validate_title(self, value):
        """Strip HTML tags and reject a title that is empty afterwards."""
        title = strip_tags(value).strip()

        if not title:
            raise serializers.ValidationError("Title cannot be empty.")

        return title

    def validate_description(self, value):
        """Strip HTML tags so stored text can never carry markup."""
        return strip_tags(value)

    def validate_category(self, value):
        """Strip HTML tags from the category."""
        return strip_tags(value)


class SkillSerializer(serializers.ModelSerializer):
    """Serialize a ``Skill`` along with its star information.

    Star data is computed per request and read-only, and only usernames are
    exposed so no email or password hash can leak through ``starred_by``.
    """

    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Skill
        fields = [
            "id",
            "name",
            "icon_url",
            "category",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]
        read_only_fields = ["id"]
        # Messages shown in the page's toast, so they are written for visitors.
        extra_kwargs = {
            "name": {"error_messages": {
                "required": "Nama skill wajib diisi.",
                "blank": "Nama skill tidak boleh kosong.",
                "null": "Nama skill wajib diisi.",
                "max_length": "Nama skill terlalu panjang (maksimal 100 karakter).",
            }},
            "icon_url": {"error_messages": {
                "required": "URL icon wajib diisi.",
                "blank": "URL icon wajib diisi.",
                "null": "URL icon wajib diisi.",
                "invalid": "URL icon tidak valid.",
                "max_length": "URL icon terlalu panjang (maksimal 200 karakter).",
            }},
            "category": {"error_messages": {
                "max_length": "Kategori terlalu panjang (maksimal 50 karakter).",
            }},
        }

    def get_star_count(self, obj):
        """Count the stars; .all() reuses prefetched users, so listing does not query per skill."""
        return len(obj.starred_by.all())

    def get_is_starred(self, obj):
        """Whether the logged-in viewer starred this item; always False for guests."""
        request = self.context.get("request")

        if request is None or not request.user.is_authenticated:
            return False

        return any(user.pk == request.user.pk for user in obj.starred_by.all())

    def get_starred_by_names(self, obj):
        """List usernames only, so no email or password hash can leak through the relation."""
        return ", ".join(user.username for user in obj.starred_by.all())

    def validate_name(self, value):
        """Strip HTML tags and reject a name that is empty afterwards."""
        name = strip_tags(value).strip()

        if not name:
            raise serializers.ValidationError("Nama skill tidak boleh kosong.")

        return name

    def validate_category(self, value):
        """Strip HTML tags from the category."""
        return strip_tags(value).strip()
