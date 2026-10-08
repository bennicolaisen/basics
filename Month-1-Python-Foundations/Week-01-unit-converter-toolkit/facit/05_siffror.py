# Facit: Övning 1.5 – Siffror. Förklaring i FACIT.md.

tal = int(input("Tal: "))
tusental = tal // 1000
hundratal = tal // 100 % 10
tiotal = tal // 10 % 10
ental = tal % 10
print(f"Siffersumma: {tusental + hundratal + tiotal + ental}")
baklanges = ental * 1000 + tiotal * 100 + hundratal * 10 + tusental
print(f"Baklänges: {baklanges:04d}")
