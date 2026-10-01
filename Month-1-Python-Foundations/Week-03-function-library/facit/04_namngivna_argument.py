# Facit: Övning 3.4 – Flera standardvärden

def format_temperature(value: float, unit: str = "C", decimals: int = 1) -> str:
    return f"{round(value, decimals)} °{unit}"
