# Facit: Övning 1.6 – Svenskt belopp. Förklaring i FACIT.md.

belopp = float(input("Belopp: "))
text = f"{belopp:,.2f}"                        # 1234567.891 -> "1,234,567.89"
text = text.replace(",", " ").replace(".", ",")  # ordningen spelar roll
print(f"{text} kr")
