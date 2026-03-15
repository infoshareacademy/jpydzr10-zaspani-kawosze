from PrettyTable import PrettyTable
table = PrettyTable()

table.field_names = ["rodzaj wejścia", "ilość wejść","cena","sposób płatności"]
table.add_row(["karnet", "4 wejścia/mies",	"6 kaw",	"gotówka"])
table.add_row(["", "8 wejść/mies",	"10 kaw","karta/blik"])
table.add_row(["", "open","12 kaw", "karta podarunkowa"])
table.add_row(["wejście pojedyńcze","", "2 kawy","karta typu Multisport"])


print(table)

