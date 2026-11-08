"""Validation for contacts submitted through HTMX."""

from django import forms
from django.utils.html import strip_tags

from contacts.models import Contact


class ContactForm(forms.ModelForm):
    """Validate and clean a contact so views never trust raw request data."""

    class Meta:
        model = Contact
        fields = ["name", "email", "phone"]

    def clean_name(self):
        name = strip_tags(self.cleaned_data["name"]).strip()

        if not name:
            raise forms.ValidationError("Nama tidak boleh kosong.")

        return name

    def clean_phone(self):
        return strip_tags(self.cleaned_data["phone"]).strip()
