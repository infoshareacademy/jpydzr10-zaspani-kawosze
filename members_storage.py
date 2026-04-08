import json
from pathlib import Path

from user import GymMember


# Importujemy json, bo dane członków zapisujemy do pliku JSON.
# Path używamy do wygodnej pracy ze ścieżkami do plików.

# Tu ustawiamy domyślną ścieżkę do pliku z zapisanymi członkami.
# Dzięki temu wszystkie funkcje korzystają z jednego miejsca zapisu danych.
PROJECT_ROOT = Path(__file__).resolve().parent
MEMBERS_FILE = PROJECT_ROOT / "members.json"


# Ta funkcja wczytuje członków z pliku JSON.
# Jeśli plik jeszcze nie istnieje, zwracamy pustą listę zamiast błędu.
# def load_members(file_path):
#     try:
#         with open(file_path, "r") as file:
#             data = json.load(file)
#             return [GymMember.from_dict(member) for member in data]
#     except FileNotFoundError:
#         return []
def load_members(file_path=MEMBERS_FILE):
    storage_path = Path(file_path)

    if not storage_path.exists():
        return []

    with storage_path.open("r", encoding="utf-8") as file:
        raw_data = json.load(file)

    return [GymMember.from_dict(member_data) for member_data in raw_data]


# Ta funkcja zapisuje całą listę członków do pliku JSON.
# Najpierw zamieniamy obiekty na słowniki, żeby JSON mógł je zapisać.
def save_members(members, file_path=MEMBERS_FILE):
    storage_path = Path(file_path)
    serialized_members = [member.to_dict() for member in members]

    with storage_path.open("w", encoding="utf-8") as file:
        json.dump(serialized_members, file, ensure_ascii=False, indent=2)


# Ta funkcja dodaje nowego członka do aktualnej listy.
# Po dodaniu zapisujemy od razu całą listę z powrotem do pliku.
def add_member_to_storage(member, file_path=MEMBERS_FILE):
    members = load_members(file_path)
    members.append(member)
    save_members(members, file_path)
    return members


# Ta funkcja szuka członka po numerze karty członkowskiej.
# Jeśli znajdzie pasujący wpis, podmienia dane na nowe i zapisuje plik.
# Jeśli takiego członka nie ma, zwraca False.
def update_member(membership_card, updated_member, file_path=MEMBERS_FILE):
    members = load_members(file_path)

    for index, member in enumerate(members):
        if member.membership_card == membership_card:
            members[index] = updated_member
            save_members(members, file_path)
            return True

    return False
