"""Forms for the portfolio app."""

from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, Textarea, URLInput
from django.utils.html import strip_tags

from main.models import Project, Skill


class ProjectForm(ModelForm):
    """Form used to create a new ``Project`` from the "Tambah Project" page."""

    field_order = [
        "title",
        "description",
        "category",
        "link",
        "project_image_url",
    ]

    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "category",
            "link",
            "project_image_url",
        ]

        labels = {
            "title": "Nama Project",
            "description": "Deskripsi Project",
            "category": "Kategori",
            "link": "URL Project",
            "project_image_url": "URL Gambar Project",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Nama project",
                    "maxlength": 200,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan project kamu",
                    "rows": 4,
                }
            ),
            "category": TextInput(
                attrs={
                    "placeholder": "Contoh: Web Development",
                    "maxlength": 100,
                }
            ),
            "link": URLInput(
                attrs={
                    "placeholder": "https://github.com/...",
                }
            ),
            "project_image_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...",
                }
            ),
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()

        if not title:
            raise ValidationError("Nama project tidak boleh kosong.")

        return title

    def clean_category(self):
        return strip_tags(self.cleaned_data["category"]).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()


class SkillForm(ModelForm):
    """Form used to create/edit a ``Skill``."""

    field_order = ["name", "icon_url", "category"]

    class Meta:
        model = Skill
        fields = [
            "name",
            "icon_url",
            "category",
        ]

        labels = {
            "name": "Nama Skill",
            "icon_url": "URL Icon",
            "category": "Kategori",
        }

        widgets = {
            "name": TextInput(
                attrs={
                    "placeholder": "Nama skill",
                    "maxlength": 100,
                }
            ),
            "icon_url": URLInput(
                attrs={
                    "placeholder": "https://cdn.simpleicons.org/...",
                }
            ),
            "category": TextInput(
                attrs={
                    "placeholder": "Contoh: Tools",
                    "maxlength": 50,
                }
            ),
        }
