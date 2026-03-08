class Person:
    def __init__(self, name, surname, tel_no):
        self.name = name
        self.surname = surname
        self.tel_no = tel_no

class GymMember(Person):
    # dodalem name surname tel_no bo bez tego nie dzialalo, trzeba przekazac do Person
    def __init__(self, name, surname, tel_no, membership_card):
        super().__init__(name, surname, tel_no)  # to inicjalizuje klase bazowa
        self.membership_card = membership_card

class Administrator(Person):
    # bylo samo pass co nic nie robilo, poprawilem zeby przyjmowalo dane uzytkownika
    def __init__(self, name, surname, tel_no):
        super().__init__(name, surname, tel_no)

class Employee(Person):
    # tak samo jak GymMember, brakwalo przekazania danych do Person wiec dodalem
    def __init__(self, name, surname, tel_no, employee_card):
        super().__init__(name, surname, tel_no)
        self.employee_card = employee_card