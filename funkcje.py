from cennik import table


def show_workout_schedule():
    with open('grafik.csv', mode='r', encoding='utf-8') as file:
        content = file.read()
        print(content)


def show_membership():
    print("Wypisuje membership")
    print("===================")

def show_cennik():
    print(table)

