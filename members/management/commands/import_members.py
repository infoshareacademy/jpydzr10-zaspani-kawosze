import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from members.models import GymMember


class Command(BaseCommand):
    help = "Importuje klubowiczow z pliku JSON do bazy Django."

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            default=str(settings.BASE_DIR / "members.json"),
            help="Sciezka do pliku JSON z klubowiczami.",
        )

    def handle(self, *args, **options):
        file_path = Path(options["file"])

        if not file_path.exists():
            raise CommandError(f"Nie znaleziono pliku: {file_path}")

        with file_path.open("r", encoding="utf-8") as file:
            raw_members = json.load(file)

        created_count = 0
        updated_count = 0

        for member_data in raw_members:
            member, created = GymMember.objects.update_or_create(
                membership_card=member_data["membership_card"],
                defaults={
                    "name": member_data["name"],
                    "surname": member_data["surname"],
                    "tel_no": member_data["tel_no"],
                },
            )

            if created:
                created_count += 1
                self.stdout.write(
                    f"Dodano: {member.name} {member.surname} ({member.membership_card})"
                )
            else:
                updated_count += 1
                self.stdout.write(
                    f"Zaktualizowano: {member.name} {member.surname} ({member.membership_card})"
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Import zakonczony. Dodano: {created_count}, zaktualizowano: {updated_count}."
            )
        )
