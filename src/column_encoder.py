# src/column_encoder.py

import struct
from format_constants import *

def encode_column_data(values, col_type):
    raw_bytes = b""

    if col_type == TYPE_INT:
        for v in values:
            raw_bytes += struct.pack("<i", int(v))

    elif col_type == TYPE_FLOAT:
        for v in values:
            raw_bytes += struct.pack("<d", float(v))

    else:
        encoded_strings = []
        offsets = []
        position = 0

        for v in values:
            b = v.encode("utf-8")
            encoded_strings.append(b)
            position += len(b)
            offsets.append(position)

        raw_bytes += struct.pack("<i", len(values))
        for off in offsets:
            raw_bytes += struct.pack("<i", off)

        for s in encoded_strings:
            raw_bytes += s

    return raw_bytes
