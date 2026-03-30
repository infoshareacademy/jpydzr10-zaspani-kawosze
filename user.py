from dataclasses import asdict, dataclass


# Zostawiłem tu dataclass, bo te klasy głównie trzymają dane,
# a dzięki temu nie muszę ręcznie pisać __init__ dla każdego modelu.
# To upraszcza kod i łatwiej go potem rozwijać.
#
# Korzystałem z dokumentacji Pythona:
# https://docs.python.org/3/library/dataclasses.html
#
# I z prostego tutoriala wyjaśniającego dataclass na przykładach:
# https://realpython.com/python-data-classes/
@dataclass
class Person:
    # To jest podstawowy model osoby w aplikacji.
    # Trzymamy tu wspólne dane, które mogą mieć różne typy użytkowników.
    name: str
    surname: str
    tel_no: str


@dataclass
class GymMember(Person):
    # To jest model członka siłowni.
    # Dziedziczy dane po Person i dodaje numer karty członkowskiej.
    membership_card: str

    # Ta metoda zamienia obiekt na zwykły słownik.
    # Dzięki temu później łatwo zapisać dane do JSON.
    def to_dict(self):
        return asdict(self)

    @classmethod
    # Ta metoda robi obiekt GymMember z danych odczytanych z pliku.
    # Czyli działa odwrotnie niż to_dict().
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            surname=data["surname"],
            tel_no=data["tel_no"],
            membership_card=data["membership_card"],
        )


@dataclass
class Administrator(Person):
    # Na razie administrator ma tylko podstawowe dane z klasy Person.
    # Jeśli później dojdą uprawnienia albo login, to można rozbudować ten model.
    pass


@dataclass
class Employee(Person):
    # To jest model pracownika.
    # Dziedziczy dane wspólne po Person i dodaje numer karty pracownika.
    employee_card: str
