# Facit: Övning 4.7 – Vänd på en dictionary

def invert(mapping: dict) -> dict:
    result = {}
    for key, value in mapping.items():
        result[value] = key
    return result
