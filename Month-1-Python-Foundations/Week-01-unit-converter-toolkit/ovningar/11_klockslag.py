# Övning 1.11 – Klockslag
#
# Skriv funktionen minutes_between(start, end). start och end är klockslag
# som text, "HH:MM" (24-timmarsklocka, alltid två siffror). Funktionen
# returnerar hur många minuter det är från start till end. Är end tidigare
# på dygnet än start menas end nästa dygn.
#
#     minutes_between("08:15", "09:00")  ->  45
#     minutes_between("22:30", "01:15")  ->  165
#
# Kontrollera: python -m pytest kontroll -k 11


def minutes_between(start, end):
    ...
