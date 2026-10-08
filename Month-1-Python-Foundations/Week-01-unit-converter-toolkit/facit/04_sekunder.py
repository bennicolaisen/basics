# Facit: Övning 1.4 – Sekunder. Förklaring i FACIT.md.

sekunder = int(input("Sekunder: "))
dygn = sekunder // 86400
timmar = sekunder % 86400 // 3600
minuter = sekunder % 3600 // 60
rest = sekunder % 60
print(f"{dygn} dygn, {timmar} h, {minuter} min, {rest} s")
