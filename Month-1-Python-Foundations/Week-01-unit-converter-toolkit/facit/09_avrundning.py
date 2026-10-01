# Facit: Övning 1.9 – Två decimaler
#
# Utan :.2f skulle Python skriva 149.70000000000002, eftersom decimaltal
# lagras med en liten avrundning i datorn. :.2f avrundar till två
# decimaler när talet skrivs ut.

pris = 49.90
antal = 3
total = pris * antal
print(f"Att betala: {total:.2f} kr")
