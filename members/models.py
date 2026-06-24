import math
import secrets

from django.conf import settings
from django.db import models
from django.utils import timezone


def generate_membership_card():
    return secrets.token_hex(3).upper()


class GymMember(models.Model):
    # To jest webowa wersja modelu członka siłowni.
    # Przenosimy tu pola z wcześniejszej klasy GymMember z wersji konsolowej.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Użytkownik",
    )
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    tel_no = models.CharField(max_length=20)
    membership_card = models.CharField(
        "Numer karty",
        max_length=6,
        unique=True,
        default=generate_membership_card,
        editable=False,
        db_column="membershipcard",
    )
    membership_plan = models.ForeignKey(
        "PriceItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members",
        verbose_name="Zakupiony karnet",
    )
    membership_started_at = models.DateTimeField(
        "Data zakupu karnetu",
        null=True,
        blank=True,
    )
    membership_expires_at = models.DateTimeField(
        "Data wygaśnięcia karnetu",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name} {self.surname} ({self.membership_card})"

    @property
    def has_active_membership(self):
        return bool(
            self.membership_plan
            and self.membership_expires_at
            and self.membership_expires_at > timezone.now()
        )

    @property
    def membership_days_remaining(self):
        if not self.has_active_membership:
            return 0
        remaining = self.membership_expires_at - timezone.now()
        return max(0, math.ceil(remaining.total_seconds() / 86400))


class PriceItem(models.Model):
    DURATION_CHOICES = (
        (1, "1 miesiąc"),
        (3, "3 miesiące"),
        (6, "6 miesięcy"),
    )

    entry_type = models.CharField("Rodzaj wejścia", max_length=100, blank=True)
    duration_months = models.PositiveSmallIntegerField(
        "Okres karnetu",
        choices=DURATION_CHOICES,
    )
    price = models.CharField("Cena", max_length=50)
    payment_method = models.CharField("Sposób płatności", max_length=100)
    is_active = models.BooleanField("Aktywny plan", default=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.entry_type or 'Cennik'} - {self.price}"

    @property
    def display_name(self):
        return f"Karnet na {self.get_duration_months_display()}"

    @property
    def visits_description(self):
        return f"Okres ważności: {self.get_duration_months_display()}"


class ScheduleEntry(models.Model):
    time_range = models.CharField("Godzina", max_length=50)
    monday = models.CharField("Poniedziałek", max_length=100, blank=True)
    tuesday = models.CharField("Wtorek", max_length=100, blank=True)
    wednesday = models.CharField("Środa", max_length=100, blank=True)
    thursday = models.CharField("Czwartek", max_length=100, blank=True)
    friday = models.CharField("Piątek", max_length=100, blank=True)
    saturday = models.CharField("Sobota", max_length=100, blank=True)
    sunday = models.CharField("Niedziela", max_length=100, blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.time_range
