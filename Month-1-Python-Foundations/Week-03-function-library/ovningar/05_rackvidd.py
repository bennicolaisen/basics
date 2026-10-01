# Övning 3.5 – Lokala variabler
#
# Kör programmet. Det skriver ut 0, men det ska skriva ut 1.
#
# Variabeln count inne i add_one är en annan variabel än count utanför,
# även om de heter samma sak: den finns bara inne i funktionen. Rätta
# programmet så att det skriver ut 1, genom att låta add_one returnera det
# nya värdet och spara svaret.
#
# Kör:         python ovningar/05_rackvidd.py
# Kontrollera: python -m pytest kontroll -k 05

count = 0


def add_one(count):
    count = count + 1


add_one(count)
print(count)
