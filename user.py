from dataclasses import asdict, dataclass


@dataclass
class Person:
    name: str
    surname: str
    tel_no: str


@dataclass
class GymMember(Person):
    membership_card: str

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            surname=data["surname"],
            tel_no=data["tel_no"],
            membership_card=data["membership_card"],
        )


@dataclass
class Administrator(Person):
    pass


@dataclass
class Employee(Person):
    employee_card: str
