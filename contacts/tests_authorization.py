"""Only the portfolio owner may change contacts; reading and searching stay public."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from contacts.models import Contact


class ContactAuthorizationTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser("owner", "o@example.com", "pw-owner-1")
        self.visitor = User.objects.create_user("visitor", password="pw-visitor-1")
        self.contact = Contact.objects.create(name="Eka", email="eka@example.com")

    def assertContactUntouched(self):
        self.assertEqual(Contact.objects.count(), 1)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.name, "Eka")

    def attempt_every_write(self):
        pk = self.contact.pk
        return {
            "add": self.client.post(
                reverse("contacts:contact_add"), {"name": "Baru", "email": "b@example.com"},
            ),
            "edit": self.client.get(reverse("contacts:contact_edit", args=[pk])),
            "update": self.client.put(
                reverse("contacts:contact_update", args=[pk]),
                data="name=Diubah&email=d%40example.com",
                content_type="application/x-www-form-urlencoded",
            ),
            "delete": self.client.delete(reverse("contacts:contact_delete", args=[pk])),
        }

    def test_guest_cannot_write(self):
        for action, response in self.attempt_every_write().items():
            self.assertEqual(response.status_code, 403, action)
        self.assertContactUntouched()

    def test_regular_user_cannot_write(self):
        self.client.force_login(self.visitor)
        for action, response in self.attempt_every_write().items():
            self.assertEqual(response.status_code, 403, action)
        self.assertContactUntouched()

    def test_staff_flag_alone_grants_nothing(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.client.force_login(self.visitor)
        self.assertEqual(self.attempt_every_write()["delete"].status_code, 403)
        self.assertContactUntouched()

    def test_owner_can_write(self):
        self.client.force_login(self.owner)
        responses = self.attempt_every_write()
        self.assertEqual(
            [responses[a].status_code for a in ("add", "edit", "update", "delete")],
            [200, 200, 200, 200],
        )
        self.assertFalse(Contact.objects.filter(pk=self.contact.pk).exists())

    def test_reading_is_public(self):
        pk = self.contact.pk
        for url in (
            reverse("contacts:contact_list"),
            reverse("contacts:contact_search"),
            reverse("contacts:contact_row", args=[pk]),
        ):
            self.assertEqual(self.client.get(url).status_code, 200, url)

    def test_page_hides_write_controls_from_non_owners(self):
        for user in (None, self.visitor):
            if user:
                self.client.force_login(user)
            page = self.client.get(reverse("contacts:contact_list")).content.decode()
            self.assertNotIn("hx-post", page)
            self.assertNotIn("hx-delete", page)
            self.assertNotIn("Tambah Kontak", page)

    def test_page_shows_write_controls_to_the_owner(self):
        self.client.force_login(self.owner)
        page = self.client.get(reverse("contacts:contact_list")).content.decode()
        self.assertIn("hx-post", page)
        self.assertIn("hx-delete", page)

    def test_search_fragment_hides_row_buttons_from_non_owners(self):
        fragment = self.client.get(reverse("contacts:contact_search")).content.decode()
        self.assertIn("eka@example.com", fragment)
        self.assertNotIn("hx-delete", fragment)


class ContactValidationTest(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.create_superuser("owner", "o@example.com", "pw-owner-1"))
        self.contact = Contact.objects.create(name="Fani", email="fani@example.com")

    def test_add_rejects_missing_or_invalid_fields_without_saving(self):
        url = reverse("contacts:contact_add")
        for data in (
            {},
            {"name": "", "email": "x@example.com"},
            {"name": "   ", "email": "x@example.com"},
            {"name": "Gita", "email": "not-an-email"},
            {"name": "Gita", "email": "g@example.com", "phone": "1" * 21},
        ):
            self.assertEqual(self.client.post(url, data).status_code, 400, data)
        self.assertEqual(Contact.objects.count(), 1)

    def test_add_strips_html_tags_from_text_fields(self):
        response = self.client.post(
            reverse("contacts:contact_add"),
            {"name": "<script>alert(1)</script>Hana", "email": "h@example.com", "phone": "<b>08</b>"},
        )
        self.assertEqual(response.status_code, 200)
        saved = Contact.objects.get(email="h@example.com")
        self.assertEqual(saved.name, "alert(1)Hana")
        self.assertEqual(saved.phone, "08")

    def test_update_rejects_invalid_input_without_changing_data(self):
        url = reverse("contacts:contact_update", args=[self.contact.pk])
        response = self.client.put(
            url, data="name=&email=bad", content_type="application/x-www-form-urlencoded",
        )
        self.assertEqual(response.status_code, 400)
        self.contact.refresh_from_db()
        self.assertEqual((self.contact.name, self.contact.email), ("Fani", "fani@example.com"))
