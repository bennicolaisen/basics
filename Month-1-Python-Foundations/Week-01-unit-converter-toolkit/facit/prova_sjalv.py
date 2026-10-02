"""Facit till "Prova själv" i vecka 1. Förklaringarna finns i FACIT.md.

Funktionerna skulle i verkligheten läggas direkt i converters.py. Här
ligger de i en egen fil, så att veckans referenskod står kvar orörd.
"""

from converter_toolkit.converters import celsius_to_fahrenheit, km_to_miles, miles_to_km, seconds_to_hms

# Uppgift 1: Kelvin. 0 °C är 273.15 K, och ett steg på skalorna är lika stort.
KELVIN_AT_ZERO_CELSIUS = 273.15


def celsius_to_kelvin(celsius):
    return celsius + KELVIN_AT_ZERO_CELSIUS


def kelvin_to_celsius(kelvin):
    return kelvin - KELVIN_AT_ZERO_CELSIUS


# Uppgift 2: tillbaka från timmar, minuter och sekunder till bara sekunder.
def hms_to_seconds(hours, minutes, seconds):
    return hours * 3600 + minutes * 60 + seconds


# Uppgift 3: hastigheter. En hastighet är en sträcka per timme, så samma
# omvandling som för sträckor fungerar. Vi återanvänder den i stället för
# att skriva in 1.609344 en gång till.
def mph_to_kmh(mph):
    return miles_to_km(mph)


def kmh_to_mph(kmh):
    return km_to_miles(kmh)


# Uppgift 4: cli.py:s main() med en fråga om hastighet tillagd sist.
def main():
    print("Enhetsomvandlaren")
    print("-----------------")

    celsius = float(input("Temperatur i grader Celsius: "))
    print(f"{celsius} °C är {celsius_to_fahrenheit(celsius):.1f} °F")

    km = float(input("Sträcka i kilometer: "))
    print(f"{km} km är {km_to_miles(km):.2f} engelska mil")

    seconds = int(input("Tid i sekunder: "))
    print(f"{seconds} sekunder är {seconds_to_hms(seconds)} (h:mm:ss)")

    kmh = float(input("Hastighet i km/h: "))
    print(f"{kmh} km/h är {kmh_to_mph(kmh):.1f} mph")
