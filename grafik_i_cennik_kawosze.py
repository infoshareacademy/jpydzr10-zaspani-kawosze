
from prettytable import from_csv

with open("cennik _zaspani_k.csv") as file:
    table = from_csv(file)
    print(table)

with open("grafik _zaspani_k.csv") as file:
    table = from_csv(file)
    print(table)

