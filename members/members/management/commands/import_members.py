import json

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from members.models import GymMember


class Command(BaseCommand):
    help = "Importuje klubowiczow z lokalnego pliku members.json do bazy Django."

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            default=settings.BASE_DIR / "members.json",
            help="Sciezka do pliku JSON z klubowiczami.",
        )

    def handle(self, *args, **options):
        file_path = options["file"]

        try:
            with open(file_path, encoding="utf-8") as json_file:
                members_data = json.load(json_file)
        except FileNotFoundError as exc:
            raise CommandError(f"Nie znaleziono pliku: {file_path}") from exc
        except json.JSONDecodeError as exc:
            raise CommandError(f"Niepoprawny JSON w pliku: {file_path}") from exc

        created_count = 0
        updated_count = 0

        for member_data in members_data:
            membership_card = member_data.get("membership_card")

            if not membership_card:
                self.stdout.write(
                    self.style.WARNING("Pominieto rekord bez numeru karty.")
                )
                continue

            _, created = GymMember.objects.update_or_create(
                membership_card=membership_card,
                defaults={
                    "name": member_data.get("name", ""),
                    "surname": member_data.get("surname", ""),
                    "tel_no": member_data.get("tel_no", ""),
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Import zakonczony. Dodano: {created_count}, zaktualizowano: {updated_count}."
            )
        )
