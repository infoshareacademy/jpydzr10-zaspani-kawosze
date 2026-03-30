from cennik import get_membership_table_text
from pathlib import Path

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
