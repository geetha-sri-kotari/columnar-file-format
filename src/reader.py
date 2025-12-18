# src/reader.py

import struct
from format_constants import *
from compressor import decompress_bytes

def read_custom_file(file_path, needed_columns=None):
    with open(file_path, "rb") as file:
        if file.read(4) != MAGIC_BYTES:
            raise Exception("Invalid file format")

        column_count = struct.unpack("<i", file.read(4))[0]
        row_count = struct.unpack("<q", file.read(8))[0]

        metadata = {}

        for _ in range(column_count):
            name_len = struct.unpack("<H", file.read(2))[0]
            name = file.read(name_len).decode()
            col_type = struct.unpack("<B", file.read(1))[0]
            offset = struct.unpack("<q", file.read(8))[0]
            comp_size = struct.unpack("<q", file.read(8))[0]
            raw_size = struct.unpack("<q", file.read(8))[0]

            metadata[name] = (col_type, offset, comp_size)

        result = {}

        for name, (col_type, offset, size) in metadata.items():
            if needed_columns and name not in needed_columns:
                continue

            file.seek(offset)
            compressed = file.read(size)
            raw = decompress_bytes(compressed)

            if col_type == TYPE_INT:
                values = struct.iter_unpack("<i", raw)
                result[name] = [v[0] for v in values]

            elif col_type == TYPE_FLOAT:
                values = struct.iter_unpack("<d", raw)
                result[name] = [v[0] for v in values]

            else:
                count = struct.unpack("<i", raw[:4])[0]
                offsets = []
                for i in range(count):
                    offsets.append(struct.unpack("<i", raw[4+i*4:8+i*4])[0])

                data = raw[4 + 4*count:]
                start = 0
                values = []

                for off in offsets:
                    values.append(data[start:off].decode())
                    start = off

                result[name] = values

        return result, row_count
