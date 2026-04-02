from prettytable import PrettyTable
<<<<<<< HEAD
table = PrettyTable()

table.field_names = ["rodzaj wejścia", "ilość wejść","cena","sposób płatności"]
table.add_row(["karnet", "4 wejścia/mies",	"6 kaw",	"gotówka"])
table.add_row(["", "8 wejść/mies",	"10 kaw","karta/blik"])
table.add_row(["", "open","12 kaw", "karta podarunkowa"])
table.add_row(["wejście pojedyńcze","", "2 kawy","karta typu Multisport"])
=======
>>>>>>> main


def build_membership_table():
    table = PrettyTable()
    table.field_names = ["rodzaj wejścia", "ilość wejść", "cena", "sposób płatności"]
    table.add_row(["karnet", "4 wejścia/mies", "6 kaw", "gotówka"])
    table.add_row(["", "8 wejść/mies", "10 kaw", "karta/blik"])
    table.add_row(["", "open", "12 kaw", "karta podarunkowa"])
    table.add_row(["wejście pojedyńcze", "", "2 kawy", "karta typu Multisport"])
    return table


def get_membership_table_text():
    return build_membership_table().get_string()


if __name__ == "__main__":
    print(get_membership_table_text())
