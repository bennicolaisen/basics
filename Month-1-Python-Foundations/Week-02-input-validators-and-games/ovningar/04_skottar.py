# Övning 2.4 – Skottår
#
# Skriv klart funktionen is_leap_year. Ett år är ett skottår om det går
# jämnt att dela med 4, utom om det går jämnt att dela med 100. Men år som
# går jämnt att dela med 400 är ändå skottår.
#
# is_leap_year(2024) ska ge True, is_leap_year(1900) ska ge False och
# is_leap_year(2000) ska ge True.
#
# Tips: "går jämnt att dela med 4" skrivs year % 4 == 0. Använd and, or
# och not.
#
# Kontrollera: python -m pytest kontroll -k 04

def is_leap_year(year):
    ...  # Byt ut ... mot din kod.
