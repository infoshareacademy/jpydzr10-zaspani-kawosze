
from prettytable import from_csv

def kawosze_cennik():
    with open("cennik _zaspani_k.csv") as file:
        table = from_csv(file)
        return table

def kawosze_grafik():
    with open("grafik _zaspani_k.csv") as file:
        table = from_csv(file)
        return table

