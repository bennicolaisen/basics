# Övning 2.5 – Biljettpris
#
# Skriv klart funktionen ticket_price som returnerar priset för en
# bussbiljett i kronor:
#
#     under 12 år:        20
#     12–17 år:           30
#     65 år eller äldre:  25
#     alla andra:         40
#
# ticket_price(8) ska ge 20, ticket_price(16) ska ge 30, ticket_price(70)
# ska ge 25 och ticket_price(30) ska ge 40.
#
# Kontrollera: python -m pytest kontroll -k 05

def ticket_price(age):
    ...  # Byt ut ... mot din kod.
