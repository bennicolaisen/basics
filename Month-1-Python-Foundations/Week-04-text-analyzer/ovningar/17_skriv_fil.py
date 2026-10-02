# Övning 4.17 – Skriv en fil
#
# Skriv klart funktionen save_lines som skriver varje text i listan på en
# egen rad i filen path. Om filen redan finns ska den skrivas över.
#
# Efter save_lines(path, ["sol", "regn"]) ska filen innehålla
# "sol\nregn\n" (\n är en radbrytning).
#
# Tips: open(path, "w", encoding="utf-8") öppnar för skrivning, och
# file.write(text) skriver text (utan radbrytning).
#
# Kontrollera: python -m pytest kontroll -k 17

def save_lines(path, lines):
    ...  # Byt ut ... mot din kod.
