# Övning 4.5 – Slå upp i en dictionary
#
# Skriv klart funktionen lookup. Den får en dictionary där nycklarna är
# namn och värdena telefonnummer, och ett namn. Den ska returnera numret,
# eller texten "okänt" om namnet inte finns.
#
# lookup({"Alva": "070-123"}, "Alva") ska ge "070-123" och lookup({"Alva":
# "070-123"}, "Bo") ska ge "okänt".
#
# Tips: dictionary.get(nyckel, standard) returnerar standard om nyckeln
# saknas.
#
# Kontrollera: python -m pytest kontroll -k 05

def lookup(phone_book, name):
    ...  # Byt ut ... mot din kod.
