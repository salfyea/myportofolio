"""Database models for the portfolio app.

Two entities are tracked:

- ``Experience``: a professional/academic experience shown on the
  Experience page.
- ``Project``: a personal project shown on the Projects page.
"""

import uuid

from django.db import models


class Experience(models.Model):
    """A single professional, academic, or volunteer experience entry."""

    EXPERIENCE_CHOICES = [
        ("internship", "Internship"),
        ("research", "Research"),
        ("volunteer", "Volunteer"),
        ("part-time", "Part-Time"),
        ("full-time", "Full-Time"),
        ("freelance", "Freelance"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICES,
        default="full-time",
    )
    thumbnail = models.URLField(blank=True, default="")
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        """Whether this experience has no end date yet."""
        return self.ended_at is None


class Project(models.Model):
    """A personal project showcased on the Projects page."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    link = models.URLField(blank=True)
    project_image_url = models.URLField(blank=True, default="")

    def __str__(self):
        return self.title


class Skill(models.Model):
    """A skill or tool shown in the Skills section."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    icon_url = models.URLField()
    category = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
