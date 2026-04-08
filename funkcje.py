from pathlib import Path
from members_storage import add_member_to_storage, load_members
from cennik import get_membership_table_text
from user import GymMember


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

#Funkcja pobiera dane od usera  następnie przekazuje je do zmiennej member (w oparciu o klasę GymMember)
# i  zapisuje przy użyciu funkcji add_member_to_storage
def add_member():
    name = input("Podaj imię: \n"),
    surname = input("Podaj nazwisko: \n"),
    tel_no = input("Podaj telefonu: \n"),
    membership_card = input("Wprowadź numer karty: \n"),

    member = GymMember(name = name,
                       surname = surname,
                       tel_no = tel_no,
                       membership_card = membership_card,
                       )

    add_member_to_storage(member)

def show_members():
    members = load_members()
    if not members:
        print("Brak zapisanych klubowiczów")
        return

    print("\n----- Lista klubowiczów -----")

    for i, member in enumerate(members, start=1):
        print(f"{i}. {member.name} {member.surname}")
        print(f"    Tel: {member.tel_no}")
        print(f"    Karta: {member.membership_card}")
        print("-" * 30)



