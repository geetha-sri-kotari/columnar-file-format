# src/type_detector.py

from format_constants import *

def detect_type(values):
    try:
        for v in values:
            int(v)
        return TYPE_INT
    except:
        try:
            for v in values:
                float(v)
            return TYPE_FLOAT
        except:
            return TYPE_STRING
