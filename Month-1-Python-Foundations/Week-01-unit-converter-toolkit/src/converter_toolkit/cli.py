"""Interactive menu-driven CLI for the unit converters.

This module is deliberately thin: every conversion is delegated straight
to `converters.py`. The only things that live here are the menu loop,
prompting, and re-prompting on bad input — none of that needs (or gets)
automated tests, but keeping it thin means the part that *does* have real
logic (the math) is fully covered anyway.
"""

from converter_toolkit.converters import (
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
    km_to_miles,
    miles_to_km,
    seconds_to_hms,
)

MENU = """
Unit Converter Toolkit
-----------------------
1) Celsius -> Fahrenheit
2) Fahrenheit -> Celsius
3) Kilometres -> Miles
4) Miles -> Kilometres
5) Seconds -> hh:mm:ss
6) Quit
"""


def prompt_float(message: str) -> float:
    """Prompt until the user enters something parseable as a float."""
    while True:
        raw = input(message)
        try:
            return float(raw)
        except ValueError:
            print(f"'{raw}' isn't a number. Try again.")


def prompt_nonnegative_int(message: str) -> int:
    """Prompt until the user enters a non-negative whole number."""
    while True:
        raw = input(message)
        try:
            value = int(raw)
        except ValueError:
            print(f"'{raw}' isn't a whole number. Try again.")
            continue
        if value < 0:
            print("Value must be zero or positive. Try again.")
            continue
        return value


def run_choice(choice: str) -> None:
    if choice == "1":
        c = prompt_float("Celsius: ")
        print(f"{c}C = {celsius_to_fahrenheit(c):.2f}F")
    elif choice == "2":
        f = prompt_float("Fahrenheit: ")
        print(f"{f}F = {fahrenheit_to_celsius(f):.2f}C")
    elif choice == "3":
        km = prompt_float("Kilometres: ")
        print(f"{km}km = {km_to_miles(km):.2f}mi")
    elif choice == "4":
        mi = prompt_float("Miles: ")
        print(f"{mi}mi = {miles_to_km(mi):.2f}km")
    elif choice == "5":
        total = prompt_nonnegative_int("Total seconds: ")
        h, m, s = seconds_to_hms(total)
        print(f"{total}s = {h:02d}:{m:02d}:{s:02d}")
    else:
        print(f"Unknown option '{choice}'.")


def main() -> None:
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "6":
            print("Goodbye.")
            return
        run_choice(choice)


if __name__ == "__main__":
    main()
