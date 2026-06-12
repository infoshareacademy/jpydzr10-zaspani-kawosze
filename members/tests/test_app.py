import tempfile
import unittest
from pathlib import Path

from members_storage import add_member_to_storage, load_members, save_members, update_member
from user import GymMember, Person


class UserTests(unittest.TestCase):
    # Sprawdzamy, czy osoba zapisuje podstawowe dane.
    def test_person_data(self):
        person = Person("Jan", "Kowalski", "123456789")

        self.assertEqual("Jan", person.name)
        self.assertEqual("Kowalski", person.surname)
        self.assertEqual("123456789", person.tel_no)

    # Sprawdzamy, czy członek ma numer karty.
    def test_member_card(self):
        member = GymMember("Anna", "Nowak", "111222333", "M-1")

        self.assertEqual("M-1", member.membership_card)

    # Sprawdzamy zamianę obiektu na słownik.
    def test_member_to_dict(self):
        member = GymMember("Anna", "Nowak", "111222333", "M-1")
        member_data = member.to_dict()

        self.assertEqual("Anna", member_data["name"])
        self.assertEqual("M-1", member_data["membership_card"])

    # Sprawdzamy odtworzenie obiektu ze słownika.
    def test_member_from_dict(self):
        data = {
            "name": "Anna",
            "surname": "Nowak",
            "tel_no": "111222333",
            "membership_card": "M-1",
        }

        member = GymMember.from_dict(data)

        self.assertEqual("Anna", member.name)
        self.assertEqual("M-1", member.membership_card)


class StorageTests(unittest.TestCase):
    # Gdy plik nie istnieje, ma wrócić pusta lista.
    def test_load_empty_list_when_file_does_not_exist(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "members.json"
            members = load_members(file_path)

        self.assertEqual([], members)

    # Sprawdzamy zapis i odczyt danych z pliku.
    def test_save_and_load_members(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "members.json"
            members = [
                GymMember("Jan", "Kowalski", "123456789", "M-1"),
                GymMember("Anna", "Nowak", "987654321", "M-2"),
            ]

            save_members(members, file_path)
            loaded_members = load_members(file_path)

        self.assertEqual(2, len(loaded_members))
        self.assertEqual("Jan", loaded_members[0].name)
        self.assertEqual("M-2", loaded_members[1].membership_card)

    # Sprawdzamy dodanie nowego członka.
    def test_add_member(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "members.json"
            member = GymMember("Ola", "Zielinska", "555444333", "M-3")

            members = add_member_to_storage(member, file_path)

        self.assertEqual(1, len(members))
        self.assertEqual("M-3", members[0].membership_card)

    # Sprawdzamy edycję istniejącego członka.
    def test_update_member(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "members.json"
            save_members([GymMember("Jan", "Kowalski", "123456789", "M-1")], file_path)

            result = update_member(
                "M-1",
                GymMember("Jan", "Nowy", "000111222", "M-1"),
                file_path,
            )
            members = load_members(file_path)

        self.assertEqual(True, result)
        self.assertEqual("Nowy", members[0].surname)
        self.assertEqual("000111222", members[0].tel_no)

    # Gdy członka nie ma, funkcja ma zwrócić False.
    def test_update_missing_member(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "members.json"
            save_members([], file_path)

            result = update_member(
                "M-404",
                GymMember("Jan", "Nowy", "000111222", "M-404"),
                file_path,
            )

        self.assertEqual(False, result)


if __name__ == "__main__":
    unittest.main()
