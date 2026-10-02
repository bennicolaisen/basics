# Övning 3.4 – Flera standardvärden
#
# Skriv klart funktionen format_temperature. Den ska returnera
# temperaturen som text, med enheten och antalet decimaler som parametrar
# med standardvärden: unit="C" och decimals=1.
#
# format_temperature(21.46) ska ge "21.5 °C". format_temperature(70.7,
# unit="F") ska ge "70.7 °F". format_temperature(21.46, decimals=2) ska ge
# "21.46 °C".
#
# Tips: round(value, decimals) avrundar. Lägg märke till hur anropen ovan
# namnger argumenten (unit="F"), så att man kan hoppa över de man inte
# vill ändra.
#
# Kontrollera: python -m pytest kontroll -k 04

def format_temperature(value, unit, decimals):
    ...  # Byt ut ... mot din kod.
