# Facit: Övning 3.2 – Använd en modul
#
# import math hämtar in Pythons matematikmodul. math.pi är pi med ungefär
# 15 decimaler, mycket noggrannare än 3.14. Importer skrivs överst i
# filen.

import math


def circle_area(radius: float) -> float:
    return math.pi * radius ** 2
