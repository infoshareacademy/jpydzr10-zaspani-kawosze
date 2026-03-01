class Person:
    def __init__(self, name, surname, tel_no):
        self.name = name
        self.surname = surname
        self.tel_no = tel_no
class GymMember(Person):
    def __init__(self, membership_card):
        self.membership_card = membership_card
class Administrator(Person):
    def __init__(self):
        pass
class Employee(Person):
    def __init__(self, employee_card ):
        self.employee_card = employee_card

