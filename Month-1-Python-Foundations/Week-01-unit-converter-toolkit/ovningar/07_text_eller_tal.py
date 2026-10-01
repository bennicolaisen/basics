# Övning 1.7 – Text eller tal?
#
# Kör programmet. Det skriver ut 105, men vi vill att det ska räkna ut 10
# + 5 och skriva ut 15.
#
# Varför blir det 105? Rätta programmet så att det skriver ut 15, utan att
# ändra de två första raderna.
#
# Tips: int("10") gör om texten "10" till talet 10.
#
# Kör:         python ovningar/07_text_eller_tal.py
# Kontrollera: python -m pytest kontroll -k 07

a = "10"
b = "5"
print(a + b)
