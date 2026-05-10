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

# Create your models here.
