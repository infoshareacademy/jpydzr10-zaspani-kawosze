
from pathlib import Path

from cennik import get_membership_table_text


PROJECT_ROOT = Path(__file__).resolve().parent
SCHEDULE_FILE = PROJECT_ROOT / "grafik.csv"


def show_workout_schedule():
    if not SCHEDULE_FILE.exists():
        print("Grafik nie jest jeszcze dostępny.")
        return

    with SCHEDULE_FILE.open(mode="r", encoding="utf-8") as file:
        content = file.read()
        print(content)


def show_membership():
    print(get_membership_table_text())

def show_faq():
    with open('Faq.txt', 'r', encoding="utf-8") as file:
        print(file.read())

def show_contact():
    with open('Kontakt.txt', 'r', encoding="utf-8") as file:
        print(file.read())




from prettytable import from_csv

def kawosze_cennik():
    with open("cennik _zaspani_k.csv") as file:
        table = from_csv(file)
        return table

def kawosze_grafik():
    with open("grafik _zaspani_k.csv") as file:
        table = from_csv(file)
        return table
