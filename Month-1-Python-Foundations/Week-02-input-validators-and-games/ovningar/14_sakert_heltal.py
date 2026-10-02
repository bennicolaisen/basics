# Övning 2.14 – Fånga ett fel
#
# Skriv klart funktionen to_int_or_none. Den ska försöka göra om texten
# till ett heltal och returnera det. Om det inte går ska den returnera
# None i stället för att krascha.
#
# to_int_or_none("42") ska ge 42, to_int_or_none(" 7 ") ska ge 7 och
# to_int_or_none("sju") ska ge None.
#
# Använd try och except ValueError.
#
# Kontrollera: python -m pytest kontroll -k 14

def to_int_or_none(text):
    ...  # Byt ut ... mot din kod.
