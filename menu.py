from funkcje import show_workout_schedule
from funkcje import show_membership


print("SIŁOWNIA ZASPANI")
menu_options = {
    1 : {
        "name": "Zajęcia",
        "function": show_workout_schedule
    },
    2 : {
        1 : {
            "name": "Karnety",
            "function": show_membership
        },
        2 : {
            "name": 'Pakiety dla firm',
            "function": show_workout_schedule
        },
        3 : {
            "name": 'Tutaj coś jeszcze dodać można',
            "function": show_workout_schedule
        },
        4 : {
            "name": 'Powrót',
            "function": show_workout_schedule
        },
    },
    3 : {
        "name": "FAQ",
        "function": show_workout_schedule
    },
    4 : {
        "name": "Kontakt",
        "function": show_workout_schedule
    },
    5 : {
        "name": "Grafik",
        "function": show_workout_schedule
    },
    6 : {
        "name": "Loguje się",
        "function": show_workout_schedule
    },
    7 : {
        "name": "Wyjście",
        "function": show_workout_schedule
    },
}

current_menu = menu_options

while True:
    for key, value in current_menu.items():
        print(f"{key}", end='. ')
        if "name" in value:
            print(value['name'])
        else:
            print("Cennik")
            for k, v in value.items():
                print(f"    {k}. {v['name']}")

    try:
        menu_choice = int(input("Wybierz numer z listy: \n"))
    except Exception:
        print("Wprowadź liczbę z zakresu 1-7")
        continue
    if menu_choice not in current_menu:
        print("Podany numer nie znajduje się na liście, proszę podać poprawny numer \n")
        continue

    subvalue = current_menu[menu_choice]
    if "name" not in subvalue:
        current_menu = subvalue
        continue
    elif 'function' in subvalue:
        subvalue['function']()
    elif subvalue == "Powrót":
        current_menu = menu_options
    elif subvalue == "Wyjście":
        break

print("Kończymy na dziś")