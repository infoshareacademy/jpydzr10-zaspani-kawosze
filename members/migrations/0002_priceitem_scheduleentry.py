# Generated manually because Django is not available in the current shell.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PriceItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "entry_type",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        verbose_name="Rodzaj wejscia",
                    ),
                ),
                (
                    "visits_per_month",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        verbose_name="Ilosc wejsc/mies",
                    ),
                ),
                (
                    "price",
                    models.CharField(max_length=50, verbose_name="Cena"),
                ),
                (
                    "payment_method",
                    models.CharField(
                        max_length=100,
                        verbose_name="Sposob platnosci",
                    ),
                ),
            ],
            options={
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="ScheduleEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "time_range",
                    models.CharField(max_length=50, verbose_name="Godzina"),
                ),
                (
                    "monday",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        verbose_name="Poniedzialek",
                    ),
                ),
                (
                    "tuesday",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        verbose_name="Wtorek",
                    ),
                ),
                (
                    "wednesday",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        verbose_name="Sroda",
                    ),
                ),
                (
                    "thursday",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        verbose_name="Czwartek",
                    ),
                ),
                (
                    "friday",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        verbose_name="Piatek",
                    ),
                ),
                (
                    "saturday",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        verbose_name="Sobota",
                    ),
                ),
                (
                    "sunday",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        verbose_name="Niedziela",
                    ),
                ),
            ],
            options={
                "ordering": ["id"],
            },
        ),
    ]
