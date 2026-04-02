
from funkcje import kawosze_cennik, kawosze_grafik


MENU_OPTIONS = {
    1: {
        "name": "Zajęcia",
        "function": kawosze_grafik() ,
    },
    2: {
        1: {
            "name": "Karnety",
            "function": kawosze_cennik(),
        },
        2: {
            "name": "Pakiety dla firm",
            "function": kawosze_grafik(),
        },
        3: {
            "name": "Tutaj coś jeszcze dodać można",
            "function": kawosze_grafik(),
        },
        4: {
            "name": "Powrót",
        },
    },
    3: {
        "name": "FAQ",
        "function": kawosze_grafik(),
    },
    4: {
        "name": "Kontakt",
        "function": kawosze_grafik(),
    },
    5: {
        "name": "Grafik",
        "function": kawosze_grafik(),
    },
    6: {
        "name": "Loguje się",
        "function": kawosze_grafik(),
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
