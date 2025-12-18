Custom Columnar File Format :

1. Overview
-> This is my own columnar file format for storing tables in binary.
-> I made it to understand how formats like Parquet or ORC work.

Features:
-> Stores data column-wise
-> Supports INT32, FLOAT64, and UTF-8 strings
-> Column blocks are compressed with zlib
-> Allows reading specific columns without reading the whole file

2. File Structure
The file has this layout:
[Header]
[Column 1 Block (compressed)]
[Column 2 Block (compressed)]
...
[Column N Block (compressed)]

3. Header
The header has all metadata about the table.

Header Fields:
-> Field	Size (bytes)	Description
-> Magic Number	4	ASCII "CCF1"
-> Version	1	Current version = 1
-> Number of Columns	4	INT32
-> Number of Rows	8	INT64
-> Column Metadata Block Size	4	INT32, size of metadata section
-> Column Metadata	variable	See below

3.1 Column Metadata (for each column)
 ->Field	Size (bytes)	Description
-> Column Name Length	4	INT32
-> Column Name	variable	UTF-8 string
-> Data Type	1	0=INT32, 1=FLOAT64, 2=STRING
-> Compressed Block Size	4	INT32
-> Uncompressed Block Size	4	INT32
-> Data Offset	8	INT64, start of column block
-> Using offsets allows reading only the columns we need.

4. Column Blocks
Each column is stored in its own contiguous block:

-> INT32: sequence of 4-byte integers

-> FLOAT64: sequence of 8-byte floating numbers

STRING:

-> Concatenated UTF-8 strings

-> Offset array (INT32) marking end of each string

-> All blocks are compressed with zlib.

5. Endianness
All numbers are little-endian.

6. Reading Data
Read header to get column metadata

To read a column:
-> Seek to Data Offset
-> Read Compressed Block Size
-> Decompress using zlib
-> Parse according to type

To read all columns: 
repeat for each column

7. Writing Data
-> Convert each column to binary
-> Compress with zlib
-> Store in file
-> Write header with column offsets, compressed/uncompressed sizes, data types, and names

8. Example Layout

Header:
Magic: "CCF1"
Version: 1
NumCols: 3
NumRows: 4
Metadata size: ...

Column metadata:
Col1: name="order_id", type=INT32, offset=128
Col2: name="product_name", type=STRING, offset=160
Col3: name="price", type=FLOAT64, offset=216

Column blocks (compressed):
[order_id block][product_name block][price block]

9. Advantages
-> Fast selective column reads
-> Compressed storage
-> Better I/O performance than CSV
-> Simple to extend for new types

10. Additional Information
-> Strings use UTF-8
-> All sizes in bytes
-> Header is always at the start
-> Version byte can be increased for new features