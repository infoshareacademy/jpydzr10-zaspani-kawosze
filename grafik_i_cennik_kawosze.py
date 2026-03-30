import csv
with open("grafik _zaspani_k.csv", mode='r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader, None)
    for row in csv_reader:
        print(row)

with open("cennik _zaspani_k.csv", mode='r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader, None)
    for row in csv_reader:
        print(row)