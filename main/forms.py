from django.forms import ModelForm, TextInput, Textarea, URLInput

from main.models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "category",
            "link",
        ]

        labels = {
            "title": "Nama Project",
            "description": "Deskripsi Project",
            "category": "Kategori",
            "link": "URL Project",
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
        }
        