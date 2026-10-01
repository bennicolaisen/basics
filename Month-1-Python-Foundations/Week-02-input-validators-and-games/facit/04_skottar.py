# Facit: Övning 2.4 – Skottår
#
# Regeln läses: (delbart med 4 och inte med 100) eller delbart med 400.
# Parenteserna gör det tydligt vad som hör ihop, även om and redan räknas
# före or.

def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0
