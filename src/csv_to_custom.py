# src/csv_to_custom.py

import sys
from csv_reader import read_csv_file
from writer import write_custom_file

data, rows = read_csv_file(sys.argv[1])
write_custom_file(data, rows, sys.argv[2])
