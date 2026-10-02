# Facit: Övning 3.12 – Dela upp i små funktioner
#
# Varje funktion gör en enda sak och har ett namn som säger vad.
# total_price blir då en läsbar mening: avrunda (rabatt på (summan av
# priserna)). Var och en av de små funktionerna kan testas för sig.

def subtotal(prices: list[float]) -> float:
    return sum(prices)


def apply_discount(amount: float, percent: float) -> float:
    return amount - amount * percent / 100


def total_price(prices: list[float], discount_percent: float = 0) -> float:
    return round(apply_discount(subtotal(prices), discount_percent), 2)
