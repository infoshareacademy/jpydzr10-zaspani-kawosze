from funkcje import show_workout_schedule, show_membership


MENU_OPTIONS = {
    1: {
        "name": "Zajęcia",
        "function": show_workout_schedule,
    },
    2: {
        1: {
            "name": "Karnety",
            "function": show_membership,
        },
        2: {
            "name": "Pakiety dla firm",
            "function": show_workout_schedule,
        },
        3: {
            "name": "Powrót",
        },
    },
    3: {
        "name": "FAQ",
        "function": show_workout_schedule,
    },
    4: {
        "name": "Kontakt",
        "function": show_workout_schedule,
    },
    5: {
        "name": "Grafik",
        "function": show_workout_schedule,
    },
    6: {
        "name": "Loguje się",
        "function": show_workout_schedule,
    },
    7: {
        "name": "Wyjście",
    },
}


def display_menu(menu_options):
    for key, value in menu_options.items():
        if "name" in value:
            print(f"{key}. {value['name']}")
        else:
            print(f"{key}. Cennik")
            for subkey, submenu_option in value.items():
                print(f"    {subkey}. {submenu_option['name']}")


def get_menu_choice():
    try:
        return int(input("Wybierz numer z listy: \n"))
    except ValueError:
        print("Wprowadź liczbę z zakresu 1-7")
        return None


def main():
    print("SIŁOWNIA ZASPANI")
    current_menu = MENU_OPTIONS

    while True:
        display_menu(current_menu)
        menu_choice = get_menu_choice()

        if menu_choice is None:
            continue

        if menu_choice not in current_menu:
            print("Podany numer nie znajduje się na liście, proszę podać poprawny numer \n")
            continue

        selected_option = current_menu[menu_choice]

        if "name" not in selected_option:
            current_menu = selected_option
            continue

        if selected_option["name"] == "Powrót":
            current_menu = MENU_OPTIONS
            continue

        if selected_option["name"] == "Wyjście":
            break

        if "function" in selected_option:
            selected_option["function"]()

    print("Kończymy na dziś")


if __name__ == "__main__":
    main()
