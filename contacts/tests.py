from django.test import TestCase
from django.urls import reverse

from contacts.models import Contact


class ContactListTest(TestCase):
    def test_list_page_shows_contacts(self):
        Contact.objects.create(name="Ani", email="ani@example.com")

        response = self.client.get(reverse("contacts:contact_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contacts/index.html")
        self.assertContains(response, "ani@example.com")

    def test_list_page_shows_empty_message(self):
        response = self.client.get(reverse("contacts:contact_list"))

        self.assertContains(response, "Tidak ada kontak.")


class ContactAddTest(TestCase):
    def test_add_creates_contact_and_returns_rows_fragment(self):
        response = self.client.post(
            reverse("contacts:contact_add"),
            {"name": "Budi", "email": "budi@example.com"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contacts/_contact_rows.html")
        self.assertNotContains(response, "<html")
        self.assertContains(response, "Budi")
        self.assertEqual(Contact.objects.count(), 1)

    def test_get_does_not_create_contact(self):
        self.client.get(reverse("contacts:contact_add"))

        self.assertEqual(Contact.objects.count(), 0)
