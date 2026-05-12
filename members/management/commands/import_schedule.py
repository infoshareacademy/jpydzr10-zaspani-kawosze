import csv

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from members.models import ScheduleEntry


class Command(BaseCommand):
    help = "Importuje grafik z lokalnego pliku CSV do bazy Django."

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            default=settings.BASE_DIR / "grafik _zaspani_k.csv",
            help="Sciezka do pliku CSV z grafikiem.",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Usuwa obecny grafik przed importem.",
        )

    def handle(self, *args, **options):
        file_path = options["file"]

        if options["clear"]:
            ScheduleEntry.objects.all().delete()

        try:
            with open(file_path, encoding="utf-8", newline="") as csv_file:
                reader = csv.reader(csv_file)
                rows = list(reader)
        except FileNotFoundError as exc:
            raise CommandError(f"Nie znaleziono pliku: {file_path}") from exc

        created_count = 0

        for row in rows[1:]:
            padded_row = row + [""] * (8 - len(row))
            ScheduleEntry.objects.create(
                time_range=padded_row[0],
                monday=padded_row[1],
                tuesday=padded_row[2],
                wednesday=padded_row[3],
                thursday=padded_row[4],
                friday=padded_row[5],
                saturday=padded_row[6],
                sunday=padded_row[7],
            )
            created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Import grafiku zakonczony. Dodano: {created_count}.")
        )
