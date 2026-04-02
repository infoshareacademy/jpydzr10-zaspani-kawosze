from prettytable import PrettyTable


def build_membership_table():
    table = PrettyTable()
    table.field_names = ["rodzaj wejścia", "ilość wejść", "cena", "sposób płatności"]
    table.add_row(["karnet", "4 wejścia/mies", "50", "gotówka"])
    table.add_row(["", "8 wejść/mies", "100", "karta/blik"])
    table.add_row(["", "open", "120", "karta podarunkowa"])
    table.add_row(["wejście pojedyńcze", "", "20", "karta typu Multisport"])
    return table


def get_membership_table_text():
    return build_membership_table().get_string()


if __name__ == "__main__":
    print(get_membership_table_text())
