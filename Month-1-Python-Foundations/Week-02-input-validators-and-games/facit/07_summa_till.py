# Facit: Övning 2.7 – Summera med en loop
#
# range(1, n + 1) slutar strax före n + 1, alltså på n. Det är det
# vanligaste stället att räkna fel med ett: range(1, n) skulle missa sista
# talet.

def sum_to(n):
    total = 0
    for number in range(1, n + 1):
        total = total + number
    return total
