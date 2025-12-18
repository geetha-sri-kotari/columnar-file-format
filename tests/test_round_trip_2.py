import csv
import os
import sys

BASE_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(BASE_DIR, "..", "src"))

from csv_reader import read_csv_file
from writer import write_custom_file
from reader import read_custom_file

# File paths
INPUT_CSV = os.path.join(BASE_DIR, "..", "samples", "online_orders.csv")
TEMP_BINARY = os.path.join(BASE_DIR, "online_orders.ccf")
OUTPUT_CSV = os.path.join(BASE_DIR, "online_orders_out.csv")


def read_csv(path):
    """Read CSV and strip spaces from each cell"""
    with open(path, newline="", encoding="utf-8") as file:
        return [[cell.strip() for cell in row] for row in csv.reader(file)]


def write_csv(path, headers, data, row_count):
    """Write data dict back to CSV preserving column order"""
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for i in range(row_count):
            row = [data[col][i] for col in headers]
            writer.writerow(row)


def compare_csv(orig, out):
    """Compare two CSVs with rounding for floats"""
    for row1, row2 in zip(orig, out):
        if len(row1) != len(row2):
            return False
        for a, b in zip(row1, row2):
            try:
                # Try to compare as float
                if round(float(a), 2) != round(float(b), 2):
                    print("Mismatch:", row1, row2)
                    return False
            except ValueError:
                # Compare as string
                if a != b:
                    print("Mismatch:", row1, row2)
                    return False
    return True


def round_trip_test():
    print("Starting 20-row CSV round-trip test...")

    # Step 1: Read original CSV
    original_data = read_csv(INPUT_CSV)
    headers = original_data[0]

    # Step 2: CSV → Custom binary format
    column_data, row_count = read_csv_file(INPUT_CSV)
    write_custom_file(column_data, row_count, TEMP_BINARY)

    # Step 3: Custom binary format → CSV
    read_data, rows = read_custom_file(TEMP_BINARY)
    write_csv(OUTPUT_CSV, headers, read_data, rows)

    # Step 4: Compare CSVs
    output_data = read_csv(OUTPUT_CSV)
    if compare_csv(original_data, output_data):
        print("round-trip PASSED")
    else:
        print("round-trip FAILED")

    # Cleanup temporary files
    os.remove(TEMP_BINARY)
    os.remove(OUTPUT_CSV)


if __name__ == "__main__":
    round_trip_test()
