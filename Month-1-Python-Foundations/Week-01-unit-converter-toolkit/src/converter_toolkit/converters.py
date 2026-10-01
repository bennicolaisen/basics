"""Omvandlingsfunktioner för temperatur, avstånd och tid.

Varje funktion tar emot ett tal och lämnar tillbaka (returnerar) ett
svar. Ingen av dem använder input() eller print(): det sköter cli.py.
Den uppdelningen gör att funktionerna kan testas automatiskt, utan att
någon behöver sitta och skriva in tal.
"""

# En konstant: ett värde som aldrig ändras. Stora bokstäver i namnet är
# Pythons sätt att signalera "ändra inte på mig".
KM_PER_MILE = 1.609344


def celsius_to_fahrenheit(celsius):
    """Omvandla en temperatur från Celsius till Fahrenheit."""
    return celsius * 9 / 5 + 32


def fahrenheit_to_celsius(fahrenheit):
    """Omvandla en temperatur från Fahrenheit till Celsius."""
    return (fahrenheit - 32) * 5 / 9


def km_to_miles(km):
    """Omvandla kilometer till engelska mil (miles)."""
    return km / KM_PER_MILE


def miles_to_km(miles):
    """Omvandla engelska mil (miles) till kilometer."""
    return miles * KM_PER_MILE


def seconds_to_hms(total_seconds):
    """Skriv ett antal sekunder som timmar:minuter:sekunder, till exempel "1:01:05".

    // är heltalsdivision (hur många hela gånger) och % är resten.
    3665 sekunder: 3665 // 3600 = 1 timme, resten 65 sekunder,
    65 // 60 = 1 minut och 65 % 60 = 5 sekunder.
    """
    hours = total_seconds // 3600
    minutes = total_seconds % 3600 // 60
    seconds = total_seconds % 60
    return f"{hours}:{minutes:02d}:{seconds:02d}"
