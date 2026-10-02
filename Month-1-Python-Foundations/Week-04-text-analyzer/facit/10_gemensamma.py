# Facit: Övning 4.10 – Gemensamma värden

def common(first: list, second: list) -> list:
    return sorted(set(first) & set(second))
