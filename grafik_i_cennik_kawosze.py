from prettytable import from_csv, PrettyTable


with open("cennik _zaspani_k.csv") as csvfile:
    table = from_csv(csvfile)

print(table)

with open("grafik _zaspani_k.csv") as csvfile:
    table = from_csv(csvfile)

print(table)