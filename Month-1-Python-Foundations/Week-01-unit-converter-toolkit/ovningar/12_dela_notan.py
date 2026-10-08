# Övning 1.12 – Dela notan
#
# Skriv funktionen split_bill(total, people, tip_percent). total är notan
# i kronor, med högst två decimaler. people är antalet personer och
# tip_percent dricksen i procent; båda är heltal.
#
# Funktionen returnerar hur många hela kronor varje person ska betala: det
# minsta heltal som gör att alla tillsammans betalar minst notan plus
# dricks.
#
#     split_bill(1000, 3, 10)  ->  367
#     split_bill(900, 3, 0)    ->  300
#
# Kontrollera: python -m pytest kontroll -k 12


def split_bill(total, people, tip_percent):
    ...
