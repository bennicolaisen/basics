# Övning 3.9 – Porto
#
# Skriv klart funktionen postage som returnerar priset i kronor för att
# skicka ett brev, utifrån vikten i gram:
#
#     upp till 50 g:    22
#     upp till 100 g:   44
#     upp till 250 g:   66
#     upp till 2000 g:  99
#
# Ett brev som väger 0 g eller mindre, eller mer än 2000 g, kan inte
# skickas: kasta då ett ValueError.
#
# postage(50) ska ge 22 och postage(51) ska ge 44. (Priserna är
# påhittade.)
#
# Kontrollera: python -m pytest kontroll -k 09

def postage(weight_grams):
    ...  # Byt ut ... mot din kod.
