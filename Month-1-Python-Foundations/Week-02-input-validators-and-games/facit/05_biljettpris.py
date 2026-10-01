# Facit: Övning 2.5 – Biljettpris

def ticket_price(age):
    if age < 12:
        return 20
    elif age < 18:
        return 30
    elif age >= 65:
        return 25
    else:
        return 40
