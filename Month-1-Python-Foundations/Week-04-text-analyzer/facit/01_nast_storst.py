# Facit: Övning 4.1 – Näst störst
#
# sorted ger en ny lista och lämnar originalet orört. numbers.sort()
# skulle i stället sortera den lista som skickades in, och då ändras
# listan även för den som anropade funktionen.

def second_largest(numbers: list[float]) -> float:
    if len(numbers) < 2:
        raise ValueError("listan behöver minst två tal")
    return sorted(numbers)[-2]
