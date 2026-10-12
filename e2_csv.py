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

# 147. Code Experiments - Experiment 2 (Section 15)
# Experiment 2: the `csv` module — read comma-separated files.
#
# csv.reader(file) returns an ITERATOR over the rows. Convert it to a
# list to get a usable list-of-lists.
#
# SECTION 15 FIX: opens "weather.csv" (the file in this project).
# "temperatures.csv" doesn't exist -> FileNotFoundError.
# weather.csv looks like:
#   "Station","Temperature"
#   "Kuala Lumpur","45"
#   "New York","20"

import csv      # standard module


with open("weather.csv", "r") as file:
    data = list(csv.reader(file))   # list() turns the iterator into a list

print(data)
# -> [['Station', 'Temperature'], ['Kuala Lumpur', '45'], ['New York', '20']]
# 1 inner list = 1 row. row[0] = station, row[1] = temperature.

# Look up the temperature of a city the user asks for.
# data[1:] skips the header row (index 0).
# The city must match exactly, e.g. "New York".
city = input("Enter a city: ")
for row in data[1:]:
    if row[0] == city:
        print(row[1])
