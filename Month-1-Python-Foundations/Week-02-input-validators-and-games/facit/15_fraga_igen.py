# Facit: Övning 2.15 – Fråga tills svaret är rätt
#
# Om int() lyckas når programmet break och lämnar loopen. Om int() kastar
# ValueError hoppar programmet direkt till except, skriver meddelandet,
# och loopen börjar om.

while True:
    try:
        alder = int(input("Hur gammal är du? "))
        break
    except ValueError:
        print("Skriv ålder med siffror.")
print(f"Du är {alder} år.")
