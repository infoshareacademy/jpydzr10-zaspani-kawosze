from django.db import models


class GymMember(models.Model):
    # To jest webowa wersja modelu członka siłowni.
    # Przenosimy tu pola z wcześniejszej klasy GymMember z wersji konsolowej.
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    tel_no = models.CharField(max_length=20)
    membership_card = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.name} {self.surname} ({self.membership_card})"


class PriceItem(models.Model):
    entry_type = models.CharField("Rodzaj wejscia", max_length=100, blank=True)
    visits_per_month = models.CharField("Ilosc wejsc/mies", max_length=50, blank=True)
    price = models.CharField("Cena", max_length=50)
    payment_method = models.CharField("Sposob platnosci", max_length=100)
    is_active = models.BooleanField("Aktywny plan", default=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.entry_type or 'Cennik'} - {self.price}"

    @property
    def display_name(self):
        if self.entry_type:
            return self.entry_type.capitalize()
        if self.visits_per_month:
            return "Karnet"
        return "Plan"

    @property
    def visits_description(self):
        if self.visits_per_month == "open":
            return "Nielimitowane wejscia w miesiacu"
        if self.visits_per_month:
            return f"{self.visits_per_month} wejsc/mies"
        return "Wejscie jednorazowe"


class ScheduleEntry(models.Model):
    time_range = models.CharField("Godzina", max_length=50)
    monday = models.CharField("Poniedzialek", max_length=100, blank=True)
    tuesday = models.CharField("Wtorek", max_length=100, blank=True)
    wednesday = models.CharField("Sroda", max_length=100, blank=True)
    thursday = models.CharField("Czwartek", max_length=100, blank=True)
    friday = models.CharField("Piatek", max_length=100, blank=True)
    saturday = models.CharField("Sobota", max_length=100, blank=True)
    sunday = models.CharField("Niedziela", max_length=100, blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.time_range
