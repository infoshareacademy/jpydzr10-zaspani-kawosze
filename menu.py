print("SIŁOWNIA ZASPANI")
menu_options = {
    1 : "Zajęcia",
    2 : {
        1 : 'Karnety',
        2 : 'Pakiety dla firm',
        3 : 'Tutaj coś jeszcze dodać można',
        4 : 'Powrót'
    },
    3 : "FAQ",
    4 : "Kontakt",
    5 : "Grafik",
    6 : "Loguje się",
    7 : "Wyjście"
}

current_menu = menu_options

while True:
    for key, value in current_menu.items():
        print(f"{key}.{value}")

    menu_choice = int(input("Wybierz numer z listy: \n"))
    if menu_choice not in current_menu:
        print("Podany numer nie znajduje się na liście, proszę podać poprawny numer \n")
        continue

    subvalue = current_menu[menu_choice]
    if isinstance(subvalue, dict):
        current_menu = subvalue
        continue

    elif subvalue == "Powrót":
        current_menu = menu_options

    elif subvalue == "Wyjście":
        break
print("Kończymy na dziś")































