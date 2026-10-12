# Experiment 2: the `csv` module — read comma-separated files.
#
# csv.reader(file) returns an ITERATOR over the rows. Convert it to a
# list to get a usable list-of-lists.
#
# Assumes a `temperatures.csv` next to this file like:
#   "Station","Temperature"
#   "Kuala Lumpur","32"
#   "New York","18"
#   ...

import csv


with open("temperatures.csv", "r") as file:
    data = list(csv.reader(file))

print(data)
# -> [['Station', 'Temperature'], ['Kuala Lumpur', '32'], ['New York', '18'], ...]

# Look up the temperature of a city the user asks for.
city = input("Enter a city: ")
for row in data:
    if row[0] == city:
        print(row[1])
