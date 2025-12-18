# src/custom_to_csv.py

import sys, csv
from reader import read_custom_file

columns = None
if len(sys.argv) > 3:
    columns = sys.argv[3].split(",")

data, rows = read_custom_file(sys.argv[1], columns)

with open(sys.argv[2], "w", newline="") as file:
    writer = csv.writer(file)
    headers = list(data.keys())
    writer.writerow(headers)

    for i in range(rows):
        writer.writerow([data[h][i] for h in headers])
