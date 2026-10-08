# Övning 1.10 – Avrunda till närmaste steg
#
# Skriv funktionen round_to_nearest(value, step), som avrundar value till
# närmaste multipel av step. Ligger value precis mitt emellan avrundas
# uppåt. value och step är heltal, value minst 0 och step minst 1. Svaret
# ska vara ett heltal.
#
#     round_to_nearest(17, 5)   ->  15
#     round_to_nearest(149, 100) -> 100
#
# Kontrollera: python -m pytest kontroll -k 10


def round_to_nearest(value, step):
    ...
