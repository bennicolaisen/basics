# Facit: Övning 3.16 – Variationsbredd

def spread(numbers: list[float]) -> float:
    if len(numbers) == 0:
        raise ValueError("spread() behöver minst ett tal")
    return max(numbers) - min(numbers)
