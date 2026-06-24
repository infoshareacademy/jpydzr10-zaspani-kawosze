from contextlib import redirect_stdout
from io import StringIO
from datetime import timedelta
import json
from pathlib import Path
import tempfile

from django.core.management import call_command
from django.core import mail
from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from members.management.commands.import_members import normalize_membership_card
from members.admin import GymMemberAdmin, export_members_pdf
from members.models import GymMember, PriceItem, ScheduleEntry
from django.contrib import admin
from members.views import _add_months


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
        self.assertTrue(
            GymMember.objects.filter(
                membership_card=normalize_membership_card("M-1")
            ).exists()
        )
        self.assertIn("Import zakonczony", output.getvalue())

    def test_import_members_updates_existing_member(self):
        GymMember.objects.create(
            name="Jan",
            surname="Stary",
            tel_no="000000000",
            membership_card=normalize_membership_card("M-1"),
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

        member = GymMember.objects.get(
            membership_card=normalize_membership_card("M-1")
        )
        self.assertEqual("Nowy", member.surname)
        self.assertEqual("111111111", member.tel_no)


class WebPageTests(TestCase):
    def test_price_list_has_three_allowed_durations(self):
        self.assertEqual(
            {1, 3, 6},
            {value for value, _ in PriceItem.DURATION_CHOICES},
        )

    def test_home_page_works(self):
        response = self.client.get(reverse("members:home"))

        self.assertEqual(200, response.status_code)

    def test_price_list_shows_only_active_prices(self):
        PriceItem.objects.create(
            entry_type="karnet",
            duration_months=1,
            price="50",
            payment_method="gotowka",
            is_active=True,
        )
        PriceItem.objects.create(
            entry_type="stary plan",
            duration_months=3,
            price="999",
            payment_method="gotowka",
            is_active=False,
        )

        response = self.client.get(reverse("members:price_list"))

        self.assertEqual(200, response.status_code)
        self.assertContains(response, "50 zł")
        self.assertNotContains(response, "999 zł")

    def test_select_plan_shows_payment_simulation(self):
        user = get_user_model().objects.create_user(
            username="buyer",
            password="testpass123",
        )
        GymMember.objects.create(user=user, name="Jan", surname="Kupujacy", tel_no="")
        self.client.force_login(user)
        price = PriceItem.objects.create(
            entry_type="karnet",
            duration_months=6,
            price="120",
            payment_method="blik",
        )

        response = self.client.get(reverse("members:select_plan", args=[price.id]))

        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Symulacja płatności")
        self.assertContains(response, "120 zł")

    def test_payment_simulation_post_returns_to_price_list(self):
        user = get_user_model().objects.create_user(
            username="buyer",
            password="testpass123",
        )
        member = GymMember.objects.create(
            user=user,
            name="Jan",
            surname="Kupujacy",
            tel_no="",
        )
        self.client.force_login(user)
        price = PriceItem.objects.create(
            entry_type="karnet",
            duration_months=3,
            price="120",
            payment_method="blik",
        )

        response = self.client.post(
            reverse("members:select_plan", args=[price.id]),
            follow=True,
        )

        member.refresh_from_db()
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "został aktywowany")
        self.assertContains(response, "Aktywny do")
        self.assertEqual(price, member.membership_plan)
        self.assertTrue(member.has_active_membership)
        self.assertIsNotNone(member.membership_started_at)
        self.assertIsNotNone(member.membership_expires_at)
        self.assertEqual(
            _add_months(member.membership_started_at, 3),
            member.membership_expires_at,
        )

    def test_schedule_page_works(self):
        ScheduleEntry.objects.create(time_range="10.00 - 11.00", monday="fitness")

        response = self.client.get(reverse("members:schedule"))

        self.assertEqual(200, response.status_code)
        self.assertContains(response, "fitness")

    def test_faq_page_works(self):
        response = self.client.get(reverse("members:faq"))

        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Najczęstsze pytania")
        self.assertContains(response, "Jak mogę kupić karnet")

    def test_contact_page_works(self):
        response = self.client.get(reverse("members:contact"))

        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Wersja demo")

    def test_members_list_requires_admin_login(self):
        response = self.client.get(reverse("members:list"))

        self.assertEqual(302, response.status_code)
        self.assertIn("/admin/login/", response["Location"])

    def test_members_list_works_for_superuser(self):
        user = get_user_model().objects.create_superuser(
            username="admin",
            password="testpass123",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("members:list"))

        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Lista klubowiczów")

    def test_members_list_is_not_cached(self):
        user = get_user_model().objects.create_superuser(
            username="admin",
            password="testpass123",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("members:list"))

        self.assertEqual(200, response.status_code)
        self.assertIn("no-cache", response["Cache-Control"])


class AccountPanelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="klubowicz",
            password="StareHaslo123!",
        )
        self.member = GymMember.objects.create(
            user=self.user,
            name="Jan",
            surname="Kowalski",
            tel_no="123456789",
            membership_card="A1B2C3",
        )

    def test_account_menu_is_hidden_for_anonymous_user(self):
        response = self.client.get(reverse("members:home"))

        self.assertNotContains(response, "Moje konto")
        self.assertContains(response, "Logowanie")

    def test_account_menu_is_visible_after_login(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("members:home"))

        self.assertContains(response, "Moje konto")
        self.assertContains(response, "Dane konta")
        self.assertContains(response, "Zmiana hasła")
        self.assertContains(response, "Wyloguj")
        self.assertContains(response, "Nieaktywny")

    def test_account_page_requires_login(self):
        response = self.client.get(reverse("members:account"))

        self.assertEqual(302, response.status_code)
        self.assertIn("/admin/login/", response["Location"])

    def test_account_page_shows_member_data(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("members:account"))

        self.assertEqual(200, response.status_code)
        self.assertContains(response, "klubowicz")
        self.assertContains(response, "Jan")
        self.assertContains(response, "Kowalski")
        self.assertContains(response, "A1B2C3")

    def test_password_change_keeps_user_logged_in(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("members:change_password"),
            {
                "old_password": "StareHaslo123!",
                "new_password1": "NoweHaslo456!",
                "new_password2": "NoweHaslo456!",
            },
            follow=True,
        )

        self.user.refresh_from_db()
        self.assertEqual(200, response.status_code)
        self.assertTrue(self.user.check_password("NoweHaslo456!"))
        self.assertIn("_auth_user_id", self.client.session)
        self.assertContains(response, "Hasło zostało pomyślnie zmienione.")

    def test_registration_generates_six_digit_hex_card(self):
        response = self.client.post(
            reverse("admin_login"),
            {
                "mode": "register",
                "next": reverse("members:home"),
                "username": "nowy_user",
                "password1": "MocneHaslo123!",
                "password2": "MocneHaslo123!",
            },
        )

        member = GymMember.objects.get(user__username="nowy_user")
        self.assertEqual(302, response.status_code)
        self.assertRegex(member.membership_card, r"^[0-9A-F]{6}$")
        self.assertEqual(
            "membershipcard",
            GymMember._meta.get_field("membership_card").db_column,
        )

    def test_account_data_can_be_edited_without_changing_card(self):
        self.client.force_login(self.user)
        original_card = self.member.membership_card

        response = self.client.post(
            reverse("members:account"),
            {
                "name": "Anna",
                "surname": "Nowak",
                "tel_no": "987654321",
                "membership_card": "FFFFFF",
            },
            follow=True,
        )

        self.member.refresh_from_db()
        self.assertEqual(200, response.status_code)
        self.assertEqual("Anna", self.member.name)
        self.assertEqual("Nowak", self.member.surname)
        self.assertEqual("987654321", self.member.tel_no)
        self.assertEqual(original_card, self.member.membership_card)

    def test_active_membership_is_shown_in_menu_and_account(self):
        plan = PriceItem.objects.create(
            entry_type="karnet",
            duration_months=1,
            price="50",
            payment_method="blik",
        )
        self.member.membership_plan = plan
        self.member.membership_started_at = timezone.now()
        self.member.membership_expires_at = timezone.now() + timedelta(days=30)
        self.member.save()
        self.client.force_login(self.user)

        home_response = self.client.get(reverse("members:home"))
        account_response = self.client.get(reverse("members:account"))

        self.assertContains(home_response, "Aktywny do")
        self.assertContains(account_response, "Karnet na 1 miesiąc")
        self.assertContains(account_response, "Pozostały czas")

    def test_expired_membership_is_inactive(self):
        plan = PriceItem.objects.create(
            entry_type="karnet",
            duration_months=1,
            price="50",
            payment_method="blik",
        )
        self.member.membership_plan = plan
        self.member.membership_started_at = timezone.now() - timedelta(days=40)
        self.member.membership_expires_at = timezone.now() - timedelta(days=10)
        self.member.save()
        self.client.force_login(self.user)

        response = self.client.get(reverse("members:home"))

        self.assertContains(response, "Nieaktywny")
        self.assertFalse(self.member.has_active_membership)


class AdminReportTests(TestCase):
    def test_admin_action_returns_pdf_report(self):
        GymMember.objects.create(
            name="Jan",
            surname="Kowalski",
            tel_no="123456789",
        )
        request = RequestFactory().get("/admin/members/gymmember/")
        model_admin = GymMemberAdmin(GymMember, admin.site)

        response = export_members_pdf(
            model_admin,
            request,
            GymMember.objects.all(),
        )

        self.assertEqual("application/pdf", response["Content-Type"])
        self.assertIn("raport_klubowiczow_", response["Content-Disposition"])
        self.assertTrue(response.content.startswith(b"%PDF"))
        self.assertGreater(len(response.content), 1000)


class ContactEmailTests(TestCase):
    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        DEFAULT_FROM_EMAIL="noreply@test.local",
    )
    def test_contact_form_sends_email_to_superuser(self):
        get_user_model().objects.create_superuser(
            username="admin-mail",
            email="admin@example.com",
            password="MocneHaslo123!",
        )

        response = self.client.post(
            reverse("members:contact"),
            {
                "name": "Jan Kowalski",
                "email": "jan@example.com",
                "message": "Prosze o kontakt.",
            },
            follow=True,
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(["admin@example.com"], mail.outbox[0].to)
        self.assertIn("jan@example.com", mail.outbox[0].body)
        self.assertContains(response, "Wiadomość została wysłana do administratora!")

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_contact_form_prints_to_console_without_superuser_email(self):
        output = StringIO()

        with redirect_stdout(output):
            response = self.client.post(
                reverse("members:contact"),
                {
                    "name": "Anna Nowak",
                    "email": "anna@example.com",
                    "message": "Wiadomosc testowa.",
                },
                follow=True,
            )

        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(mail.outbox))
        self.assertIn("BRAK SUPERUSERA Z ADRESEM E-MAIL", output.getvalue())
        self.assertIn("anna@example.com", output.getvalue())
        self.assertContains(response, "Wiadomość została zapisana w konsoli.")
