from io import StringIO
import json
from pathlib import Path
import tempfile

from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from members.models import GymMember, PriceItem, ScheduleEntry


class ImportMembersCommandTests(TestCase):
    def test_import_members_creates_records_from_json_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "members.json"
            file_path.write_text(
                json.dumps(
                    [
                        {
                            "name": "Jan",
                            "surname": "Kowalski",
                            "tel_no": "123456789",
                            "membership_card": "M-1",
                        },
                        {
                            "name": "Anna",
                            "surname": "Nowak",
                            "tel_no": "987654321",
                            "membership_card": "M-2",
                        },
                    ]
                ),
                encoding="utf-8",
            )

            output = StringIO()
            call_command("import_members", file=str(file_path), stdout=output)

        self.assertEqual(2, GymMember.objects.count())
        self.assertTrue(GymMember.objects.filter(membership_card="M-1").exists())
        self.assertIn("Import zakonczony", output.getvalue())

    def test_import_members_updates_existing_member(self):
        GymMember.objects.create(
            name="Jan",
            surname="Stary",
            tel_no="000000000",
            membership_card="M-1",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "members.json"
            file_path.write_text(
                json.dumps(
                    [
                        {
                            "name": "Jan",
                            "surname": "Nowy",
                            "tel_no": "111111111",
                            "membership_card": "M-1",
                        }
                    ]
                ),
                encoding="utf-8",
            )

            call_command("import_members", file=str(file_path))

        member = GymMember.objects.get(membership_card="M-1")
        self.assertEqual("Nowy", member.surname)
        self.assertEqual("111111111", member.tel_no)


class WebPageTests(TestCase):
    def test_home_page_works(self):
        response = self.client.get(reverse("members:home"))

        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Silownia Zaspani Kawosze")

    def test_price_list_shows_only_active_prices(self):
        PriceItem.objects.create(
            entry_type="karnet",
            visits_per_month="4",
            price="50",
            payment_method="gotowka",
            is_active=True,
        )
        PriceItem.objects.create(
            entry_type="stary plan",
            visits_per_month="1",
            price="999",
            payment_method="gotowka",
            is_active=False,
        )

        response = self.client.get(reverse("members:price_list"))

        self.assertEqual(200, response.status_code)
        self.assertContains(response, "50 zl")
        self.assertNotContains(response, "999 zl")

    def test_select_plan_shows_payment_simulation(self):
        price = PriceItem.objects.create(
            entry_type="karnet",
            visits_per_month="open",
            price="120",
            payment_method="blik",
            is_active=True,
        )

        response = self.client.get(reverse("members:select_plan", args=[price.id]))

        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Symulacja platnosci")
        self.assertContains(response, "120 zl")

    def test_payment_simulation_post_returns_to_price_list(self):
        price = PriceItem.objects.create(
            entry_type="karnet",
            visits_per_month="open",
            price="120",
            payment_method="blik",
            is_active=True,
        )

        response = self.client.post(
            reverse("members:select_plan", args=[price.id]),
            follow=True,
        )

        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Platnosc testowa")

    def test_schedule_page_works(self):
        ScheduleEntry.objects.create(
            time_range="10.00 - 11.00",
            monday="fitness",
        )

        response = self.client.get(reverse("members:schedule"))

        self.assertEqual(200, response.status_code)
        self.assertContains(response, "fitness")

    def test_faq_page_works(self):
        response = self.client.get(reverse("members:faq"))

        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Najczestsze pytania")

    def test_contact_page_works(self):
        response = self.client.get(reverse("members:contact"))

        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Wersja demo")

    def test_members_list_requires_admin_login(self):
        response = self.client.get(reverse("members:list"))

        self.assertEqual(302, response.status_code)
        self.assertIn("/admin/login/", response["Location"])

    def test_members_list_works_for_staff_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="admin",
            password="testpass123",
            is_staff=True,
        )
        self.client.force_login(user)

        response = self.client.get(reverse("members:list"))

        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Lista klubowiczow")
