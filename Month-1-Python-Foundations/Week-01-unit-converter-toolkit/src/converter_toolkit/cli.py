"""Enhetsomvandlaren som program: frågar efter tal och skriver ut svaren.

All räkning görs av funktionerna i converters.py. Den här filen pratar
bara med användaren.
"""

from converter_toolkit.converters import celsius_to_fahrenheit, km_to_miles, seconds_to_hms


def main():
    print("Enhetsomvandlaren")
    print("-----------------")

    celsius = float(input("Temperatur i grader Celsius: "))
    print(f"{celsius} °C är {celsius_to_fahrenheit(celsius):.1f} °F")

    km = float(input("Sträcka i kilometer: "))
    print(f"{km} km är {km_to_miles(km):.2f} engelska mil")

    seconds = int(input("Tid i sekunder: "))
    print(f"{seconds} sekunder är {seconds_to_hms(seconds)} (h:mm:ss)")


# Raden nedan betyder "kör main() om den här filen startas som ett program".
# Om filen i stället importeras av en annan fil (som testerna gör) körs
# ingenting automatiskt.
if __name__ == "__main__":
    main()
