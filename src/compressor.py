# src/compressor.py

import zlib

def compress_bytes(data):
    return zlib.compress(data)

def decompress_bytes(data):
    return zlib.decompress(data)
