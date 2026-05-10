from io import StringIO
import json
from pathlib import Path
import tempfile

from django.core.management import call_command
from django.test import TestCase

from members.models import GymMember


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
