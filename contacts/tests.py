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
            {"name": "Budi", "email": "budi@example.com", "phone": "0812"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contacts/_contact_row.html")
        self.assertNotContains(response, "<html")
        self.assertContains(response, "Budi")
        self.assertContains(response, "0812")
        self.assertEqual(Contact.objects.count(), 1)

    def test_add_returns_only_the_new_row(self):
        Contact.objects.create(name="Lama", email="lama@example.com")

        response = self.client.post(
            reverse("contacts:contact_add"),
            {"name": "Baru", "email": "baru@example.com"},
        )

        self.assertContains(response, "Baru")
        self.assertNotContains(response, "Lama")
        self.assertContains(response, 'hx-swap-oob="delete"')
        self.assertContains(response, "Kontak berhasil ditambahkan!")

    def test_get_does_not_create_contact(self):
        self.client.get(reverse("contacts:contact_add"))

        self.assertEqual(Contact.objects.count(), 0)


class ContactDeleteTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(name="Citra", email="citra@example.com")

    def test_delete_removes_contact_and_returns_empty_200(self):
        response = self.client.delete(
            reverse("contacts:contact_delete", args=[self.contact.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"")
        self.assertFalse(Contact.objects.filter(pk=self.contact.pk).exists())

    def test_delete_rejects_other_methods(self):
        response = self.client.post(
            reverse("contacts:contact_delete", args=[self.contact.pk])
        )

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Contact.objects.filter(pk=self.contact.pk).exists())

    def test_delete_missing_contact_returns_404(self):
        response = self.client.delete(reverse("contacts:contact_delete", args=[999]))

        self.assertEqual(response.status_code, 404)


class ContactSearchTest(TestCase):
    def setUp(self):
        Contact.objects.create(name="Annisa", email="annisa@example.com")
        Contact.objects.create(name="Budi", email="budi@example.com")

    def test_search_filters_case_insensitively(self):
        response = self.client.get(reverse("contacts:contact_search"), {"q": "ANN"})

        self.assertContains(response, "Annisa")
        self.assertNotContains(response, "Budi")

    def test_empty_query_returns_all_contacts(self):
        response = self.client.get(reverse("contacts:contact_search"), {"q": ""})

        self.assertContains(response, "Annisa")
        self.assertContains(response, "Budi")

    def test_no_match_shows_empty_message(self):
        response = self.client.get(reverse("contacts:contact_search"), {"q": "zzz"})

        self.assertContains(response, "Tidak ada kontak.")


class ContactEditTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(name="Dewi", email="dewi@example.com")

    def test_edit_returns_form_row(self):
        response = self.client.get(
            reverse("contacts:contact_edit", args=[self.contact.pk])
        )

        self.assertTemplateUsed(response, "contacts/_contact_edit_row.html")
        self.assertContains(response, 'value="Dewi"')

    def test_row_returns_display_row(self):
        response = self.client.get(
            reverse("contacts:contact_row", args=[self.contact.pk])
        )

        self.assertTemplateUsed(response, "contacts/_contact_row.html")
        self.assertContains(response, "dewi@example.com")

    def test_update_saves_put_body_and_returns_display_row(self):
        response = self.client.put(
            reverse("contacts:contact_update", args=[self.contact.pk]),
            data="name=Dewi+Baru&email=baru%40example.com&phone=0899",
            content_type="application/x-www-form-urlencoded",
        )
        self.contact.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.contact.name, "Dewi Baru")
        self.assertEqual(self.contact.email, "baru@example.com")
        self.assertEqual(self.contact.phone, "0899")
        self.assertTemplateUsed(response, "contacts/_contact_row.html")

    def test_update_rejects_post(self):
        response = self.client.post(
            reverse("contacts:contact_update", args=[self.contact.pk]),
            {"name": "X", "email": "x@example.com"},
        )

        self.assertEqual(response.status_code, 405)
