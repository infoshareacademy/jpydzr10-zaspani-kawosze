from pathlib import Path
from members_storage import add_member_to_storage, load_members, delete_member, update_member
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
    name = input("Podaj imię: \n")
    surname = input("Podaj nazwisko: \n")
    tel_no = input("Podaj telefonu: \n")
    membership_card = input("Wprowadź numer karty: \n")

    member = GymMember(
        name = name,
        surname = surname,
        tel_no = tel_no,
        membership_card = membership_card,
    )

    add_member_to_storage(member)
    print(f"Dodano użytkownika {name} {surname} o numerze karty {membership_card}")

def show_members():
    members = load_members()
    if not members:
        print("Brak klubowiczów w bazie")
        return

    print("\n----- Lista klubowiczów -----")

    for i, member in enumerate(members, start=1):
        print(f"{i}. {member.name} {member.surname}")
        print(f"    Tel: {member.tel_no}")
        print(f"    Karta: {member.membership_card}")
        print("-" * 30)

def remove_member():
    members = load_members()

    if not members:
        print ("Brak użytkowników do usunięcia")
        return
    show_members()
    try:
        choice = int(input("Podaj numer który chcesz usunąć: \n"))
        index = choice - 1
    except ValueError:
        print("Nieprawidłowy numer")
        return

    succes = delete_member(index)
    if succes:
        print("Użytkownik usunięty.")
    else:
        print("Nieprawidłowy numer lub brak użytkownika")

def change_member():
    members = load_members()

    if not members:
        print("Brak klubowiczów do edycji.")
        return

    show_members()
    card = input("Podaj numer karty użytkownika do edycji: ").strip()

    member_to_edit = next((m for m in members if m.membership_card == card), None)

    if member_to_edit is None:
        print(f"Nie znaleziono użytkownika z kartą {card}")
        return

    name = input(f"Nowe imię [{member_to_edit.name}]: ").strip() or member_to_edit.name
    surname = input(f"Nowe nazwisko [{member_to_edit.surname}]: ").strip() or member_to_edit.surname
    tel_no = input(f"Nowy tel. [{member_to_edit.tel_no}]: ").strip() or member_to_edit.tel_no

    updated_member = GymMember(
        name = name,
        surname = surname,
        tel_no = tel_no,
        membership_card = member_to_edit.membership_card
    )

    if update_member(member_to_edit.membership_card, updated_member):
        print("Użytkownik zaktualizowany.")
    else:
        print("Nie udało się zaktualizować użytkownika.")


