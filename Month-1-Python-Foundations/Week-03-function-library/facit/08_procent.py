# Facit: Övning 3.8 – Procent och ogiltiga värden

def percent(part: float, whole: float) -> float:
    if whole == 0:
        raise ValueError("det hela (whole) får inte vara 0")
    return round(part / whole * 100, 1)
