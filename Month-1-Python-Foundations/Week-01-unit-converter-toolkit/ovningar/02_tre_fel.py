# Övning 1.2 – Tre fel
#
# Programmet nedan ska skriva ut:
#
#     Totalt: 147 kr
#     Med 10 % rabatt: 132.30 kr
#
# Det innehåller tre fel av tre olika sorter. Python visar bara ett fel i
# taget. Rätta dem ett efter ett.
#
# Skriv dessutom, som kommentarer allra överst i filen, namnen på de tre
# feltyperna i den ordning Python visade dem.
#
# Regel: utskriften ska räknas fram från pris och antal. Kontrollen kör
# programmet med andra värden på pris och antal också.
#
# Kör:         python ovningar/02_tre_fel.py
# Kontrollera: python -m pytest kontroll -k 02

pris = 49
antal = 3
summa = pris * antal
print("Totalt: " + summa + " kr"
print(f"Med 10 % rabatt: {sumna * 0.9:.2f} kr")
