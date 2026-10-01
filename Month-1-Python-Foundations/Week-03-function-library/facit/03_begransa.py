# Facit: Övning 3.3 – Håll ett värde inom gränser
#
# Två return i början hanterar specialfallen. Det som återstår efter dem
# är det vanliga fallet. Ett kortare men svårare att läsa alternativ är
# max(low, min(value, high)).

def clamp(value: float, low: float, high: float) -> float:
    if value < low:
        return low
    if value > high:
        return high
    return value
