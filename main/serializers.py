"""Serializers for the REST API of the portfolio app."""

from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Project


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
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")

        if request is None or not request.user.is_authenticated:
            return False

        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())

    def validate_title(self, value):
        title = strip_tags(value).strip()

        if not title:
            raise serializers.ValidationError("Title cannot be empty.")

        return title

    def validate_category(self, value):
        return strip_tags(value).strip()

    def validate_description(self, value):
        return strip_tags(value).strip()
