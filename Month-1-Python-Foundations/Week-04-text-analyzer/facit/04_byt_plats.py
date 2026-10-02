# Facit: Övning 4.4 – Byt plats på två variabler
#
# Till höger skapas först tupeln (b, a), alltså (2, 1). Sedan packas den
# upp till vänster: a får 2 och b får 1. Eftersom hela högra sidan räknas
# ut först skrivs inget värde över för tidigt.

a = 1
b = 2

a, b = b, a

print(f"a = {a}, b = {b}")
