from funkcje import show_workout_schedule, show_membership, show_faq, show_contact

MENU_OPTIONS = {
    1: {
        "name": "Grafik",
        "function": show_workout_schedule,
    },
    2: {
        "name": "Cennik",
        "function": show_membership,
    },
    3: {
        "name": "FAQ",
        "function": show_faq,
    },
    4: {
        "name": "Kontakt",
        "function": show_contact,
    },
    5: {
        1: {
            "name": "Dodaj usera",
            "function": show_membership,
        },
        2: {
            "name": "Usuń usera",
            "function": show_workout_schedule,
        },
        3: {
            "name": "Wyświetl naszych klubowiczów",
            "function": show_workout_schedule,
        },
        4: {
            "name": "Powrót",
        },
    },
    6: {
        "name": "Wyjście",
    },
}

def print_separator(char="—", length=40):
    """Pomocnicza funkcja do rysowania linii oddzielających sekcje."""
    print(char * length)

def display_menu(menu_options):
    print_separator("=")
    for key, value in menu_options.items():
        if "name" in value:
            print(f"{key}. {value['name']}")
        else:
            print(f"{key}. Klubowicze")
            for subkey, submenu_option in value.items():
                print(f"    {subkey}. {submenu_option['name']}")
    print_separator("=")

def get_menu_choice():
    try:
        return int(input("Wybierz numer z listy: "))
    except ValueError:
        print("\n[!] Błąd: Wprowadź liczbę z zakresu menu.")
        return None

def main():
    print_separator("#")
    print("        SIŁOWNIA ZASPANI")
    print_separator("#")
    
    current_menu = MENU_OPTIONS

    while True:
        display_menu(current_menu)
        menu_choice = get_menu_choice()

        if menu_choice is None:
            continue

        if menu_choice not in current_menu:
            print("\n[!] Podany numer nie znajduje się na liście.\n")
            continue

        selected_option = current_menu[menu_choice]

        if selected_option.get("name") == "Wyjście":
            break

        if selected_option.get("name") == "Powrót":
            current_menu = MENU_OPTIONS
            continue

        if "name" not in selected_option:
            current_menu = selected_option
            continue

        if "function" in selected_option:
            print("\n") # Odstęp przed treścią funkcji
            selected_option["function"]()
            print("\n") # Odstęp po treści funkcji
            
            current_menu = {
                1: {"name": "Powrót"}
            }

    print_separator("-")
    print("Kończymy na dziś. Do zobaczenia na treningu!")
    print_separator("-")

if __name__ == "__main__":
    main()
