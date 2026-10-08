# Facit: Övning 1.7 – Ruta. Förklaring i FACIT.md.

bredd = int(input("Bredd: "))
hojd = int(input("Höjd: "))
kant = "+" + "-" * (bredd - 2) + "+\n"
mitt = "|" + " " * (bredd - 2) + "|\n"
print(kant + mitt * (hojd - 2) + kant, end="")
