# src/writer.py

import struct
from format_constants import *
from type_detector import detect_type
from column_encoder import encode_column_data
from compressor import compress_bytes

def write_custom_file(column_data, row_count, output_path):
    column_blocks = []
    column_meta = []

    for name, values in column_data.items():
        col_type = detect_type(values)
        raw_data = encode_column_data(values, col_type)
        compressed = compress_bytes(raw_data)

        column_blocks.append(compressed)
        column_meta.append({
            "name": name,
            "type": col_type,
            "compressed_size": len(compressed),
            "raw_size": len(raw_data)
        })

    with open(output_path, "wb") as file:
        file.write(MAGIC_BYTES)
        file.write(struct.pack("<i", len(column_meta)))
        file.write(struct.pack("<q", row_count))

        header_size = 4 + 4 + 8
        for meta in column_meta:
            header_size += 2 + len(meta["name"].encode()) + 1 + 8 + 8 + 8

        offset = header_size

        for meta in column_meta:
            name_bytes = meta["name"].encode()
            file.write(struct.pack("<H", len(name_bytes)))
            file.write(name_bytes)
            file.write(struct.pack("<B", meta["type"]))
            file.write(struct.pack("<q", offset))
            file.write(struct.pack("<q", meta["compressed_size"]))
            file.write(struct.pack("<q", meta["raw_size"]))
            offset += meta["compressed_size"]

        for block in column_blocks:
            file.write(block)
