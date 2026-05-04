import csv

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from members.models import PriceItem


class Command(BaseCommand):
    help = "Importuje cennik z lokalnego pliku CSV do bazy Django."

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            default=settings.BASE_DIR / "cennik _zaspani_k.csv",
            help="Sciezka do pliku CSV z cennikiem.",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Usuwa obecny cennik przed importem.",
        )

    def handle(self, *args, **options):
        file_path = options["file"]

        if options["clear"]:
            PriceItem.objects.all().delete()

        try:
            with open(file_path, encoding="utf-8", newline="") as csv_file:
                rows = list(csv.DictReader(csv_file))
        except FileNotFoundError as exc:
            raise CommandError(f"Nie znaleziono pliku: {file_path}") from exc

        created_count = 0

        for row in rows:
            PriceItem.objects.create(
                entry_type=row.get("rodzaj wejścia", ""),
                visits_per_month=row.get("ilość wejść/mies", ""),
                price=row.get("cena", ""),
                payment_method=row.get("sposób płatności", ""),
            )
            created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Import cennika zakonczony. Dodano: {created_count}.")
        )
