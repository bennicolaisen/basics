# Övning 2.3 – Betyg
#
# Skriv klart funktionen grade som gör om poäng (0–100) till ett betyg:
#
#     90 eller mer: "A"
#     80–89:        "B"
#     70–79:        "C"
#     60–69:        "D"
#     50–59:        "E"
#     under 50:     "F"
#
# grade(95) ska ge "A", grade(80) ska ge "B" och grade(49) ska ge "F".
#
# Tips: kontrollera från högsta gränsen och nedåt. Den första if/elif som
# är sann vinner.
#
# Kontrollera: python -m pytest kontroll -k 03

def grade(points):
    ...  # Byt ut ... mot din kod.
