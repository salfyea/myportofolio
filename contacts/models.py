"""Database models for the contacts app (Tutorial 06: HTMX)."""

from django.db import models


class Contact(models.Model):
    """A person with a name and an email address."""

    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name
