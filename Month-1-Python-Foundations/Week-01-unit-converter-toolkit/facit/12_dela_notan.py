# Facit: Övning 1.12 – Dela notan. Förklaring i FACIT.md.

import math


def split_bill(total, people, tip_percent):
    total_ore = round(total * 100)               # notan i hela ören, ett exakt heltal
    with_tip = total_ore * (100 + tip_percent)   # fortfarande ett exakt heltal (öre * 100)
    return math.ceil(with_tip / (100 * 100 * people))
