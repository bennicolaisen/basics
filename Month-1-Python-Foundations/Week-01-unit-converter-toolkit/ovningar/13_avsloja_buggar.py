# Övning 1.13 – Avslöja buggarna
#
# Funktionen seconds_to_hms(total) gör om ett antal sekunder (0 eller fler)
# till texten "H:MM:SS": timmar utan inledande nolla och utan övre gräns,
# minuter och sekunder alltid med två siffror.
#
#     seconds_to_hms(3665)  ->  "1:01:05"
#
# Skriv funktionen check(seconds_to_hms), som testar en sådan funktion med
# assert. Kontrollen anropar check med sju olika versioner av
# seconds_to_hms. En är rätt och sex har buggar. Din check ska godkänna
# den rätta och avslöja alla sex buggiga, utan att du får se dem.
#
# Kontrollera: python -m pytest kontroll -k 13


def check(seconds_to_hms):
    ...
