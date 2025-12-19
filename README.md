Custom Columnar File Format Project

1. Project Overview
This project implements a simplified columnar file format in Python. The goal is to understand how modern analytical file formats like Parquet and ORC work.
Features:
Columnar storage for efficient reads
Supports INT32, FLOAT64, and UTF-8 strings
Zlib compression for each column block
Selective column reads (column pruning)
Conversion tools between CSV and custom format
This project demonstrates low-level data representation, binary I/O, compression, and metadata management.


2. Repository Structure
   columnar-file-format/
│
├── samples/
│   ├── test_small.csv           # Small test CSV
│   └── test_big_20.csv          # 20-row test CSV
│
├── src/
│   ├── csv_reader.py            # Reads CSV into column-wise dict
│   ├── writer.py                # Writes custom binary format
│   ├── reader.py                # Reads custom binary format
│   ├── csv_to_custom.py         # CLI: CSV -> custom format
│   └── custom_to_csv.py         # CLI: custom format -> CSV
│
├── tests/
│   ├── test_round_trip.py       # Small CSV round-trip test
│   └── test_big20_round_trip.py # 20-row CSV round-trip test
│
├── SPEC.md                      # Binary layout specification
└── README.md


3. Setup Instructions
3.1 Clone the repository
    git clone <your-repo-url>
    cd columnar-file-format
3.2 Install dependencies
    pip install -r requirements.txt


4. Usage Examples
4.1 Convert CSV → Custom Format
   python src/csv_to_custom.py samples/test_big_20.csv temp_big20.ccf
4.2 Convert Custom Format → CSV
   python src/custom_to_csv.py temp_big20.ccf recovered_big20.csv
   This will reconstruct the original CSV.
4.3 Selective Column Read (Column Pruning)
   python src/custom_to_csv.py temp_big20.ccf selected_columns.csv order_id total_amount
Only reads the columns order_id and total_amount
Saves time and memory for large files

5. Running Tests
5.1 Small CSV round-trip test
   python tests/test_round_trip.py
5.2 20-row CSV round-trip test
   python tests/test_big20_round_trip.py
Expected output:
Starting 20-row CSV round-trip test...
round-trip PASSED


6. Project Highlights
Binary columnar layout for faster analytics
Compressed storage using zlib
Metadata header for column offsets and types
Round-trip CSV conversion ensures correctness
Demonstrates low-level data engineering concepts


7. Notes
Strings are encoded in UTF-8
All numeric types are little-endian
Header is always at the start of the file
This format can be extended to support new data types or nested structures
