"""Ett gissningsspel: datorn tänker på ett tal och du gissar.

Spelet återanvänder parse_int_in_range från validators.py för att
kontrollera varje gissning, i stället för att skriva den koden en gång
till.
"""

import random

from validators_and_games.validators import parse_int_in_range

LOW = 1
HIGH = 100
MAX_ATTEMPTS = 7


def ask_for_guess(low, high):
    """Fråga tills användaren skriver ett heltal mellan low och high."""
    while True:
        text = input(f"Gissa ett tal mellan {low} och {high}: ")
        try:
            return parse_int_in_range(text, low, high)
        except ValueError as error:
            print(f"Ogiltig gissning: {error}")


def play_game(secret, low, high, max_attempts):
    """Spela en omgång där svaret är secret. Returnerar True om man vann.

    En ogiltig gissning kostar inget försök: ask_for_guess frågar igen.
    """
    print(f"Jag tänker på ett tal mellan {low} och {high}.")
    print(f"Du har {max_attempts} försök.")

    for attempt in range(1, max_attempts + 1):
        guess = ask_for_guess(low, high)
        if guess == secret:
            print(f"Rätt! Talet var {secret}. Du klarade det på {attempt} försök.")
            return True

        remaining = max_attempts - attempt
        if guess < secret:
            print(f"För lågt. {remaining} försök kvar.")
        else:
            print(f"För högt. {remaining} försök kvar.")

    print(f"Slut på försök. Talet var {secret}.")
    return False


def main():
    secret = random.randint(LOW, HIGH)
    play_game(secret, LOW, HIGH, MAX_ATTEMPTS)


if __name__ == "__main__":
    main()
