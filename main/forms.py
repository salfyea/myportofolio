"""Forms for the portfolio app."""

from django.forms import CharField, Form, HiddenInput, ModelForm, TextInput, Textarea, URLInput

from main.models import Project, Skill


class SecretKeyFormMixin(Form):
    """Adds the shared-secret password field, since there's no auth/session
    system yet. The field is rendered hidden — the template shows a password
    gate first and copies the typed value into this field via JS once
    unlocked. The actual match against ``settings.PORTFOLIO_EDIT_KEY``
    happens in the view before saving, the same way the delete views check
    it.
    """

    secret_key = CharField(widget=HiddenInput())


class ProjectForm(SecretKeyFormMixin, ModelForm):
    """Form used to create a new ``Project`` from the "Tambah Project" page."""

    field_order = [
        "title",
        "description",
        "category",
        "link",
        "project_image_url",
        "secret_key",
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


class SkillForm(SecretKeyFormMixin, ModelForm):
    """Form used to create/edit a ``Skill``."""

    field_order = ["name", "icon_url", "category", "secret_key"]

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
