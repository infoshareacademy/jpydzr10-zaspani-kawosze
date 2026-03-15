from funkcje import show_workout_schedule, show_membership, show_cennik



print("SIŁOWNIA ZASPANI")
menu_options = {
    1 : {
        "name": "Zajęcia",
        "function": show_workout_schedule
    },
    2 : {
            "name": "CENNIK",
            "function": show_cennik
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
    },
}

current_menu = menu_options

while True:
    for key, value in current_menu.items():
        if "name" in value:
            print(f"{key}. {value['name']}")
        else:
            print(f"{key}. Cennik")
            for k, v in value.items():
                print(f"    {k}. {v['name']}")

    try:
        menu_choice = int(input("Wybierz numer z listy: \n"))
    except ValueError:
        print("Wprowadź liczbę z zakresu 1-7")
        continue

    if menu_choice not in current_menu:
        print("Podany numer nie znajduje się na liście, proszę podać poprawny numer \n")
        continue

    subvalue = current_menu[menu_choice]

    if "name" not in subvalue:
        current_menu = subvalue
        continue

    if subvalue["name"] == "Powrót":
        current_menu = menu_options
        continue

    if subvalue["name"] == "Wyjście":
        break

    if "function" in subvalue:
        subvalue["function"]()

print("Kończymy na dziś")