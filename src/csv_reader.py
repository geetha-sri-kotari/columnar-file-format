# src/csv_reader.py

import csv

def read_csv_file(csv_path):
    with open(csv_path, newline="") as file:
        reader = csv.reader(file)
        headers = next(reader)
        rows = list(reader)

    column_data = {}
    for name in headers:
        column_data[name] = []

    for row in rows:
        for i in range(len(row)):
            column_data[headers[i]].append(row[i])

    return column_data, len(rows)
