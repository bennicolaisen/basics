"""Facit till "Prova själv" i vecka 2. Förklaringarna finns i FACIT.md."""

import random

from validators_and_games.game import HIGH, LOW, MAX_ATTEMPTS, play_game
from validators_and_games.validators import is_valid_username, parse_int_in_range


# Uppgift 1
def is_valid_email(text):
    """En förenklad kontroll av en e-postadress (inte den fullständiga standarden).

    Regler: inga mellanslag, exakt ett @, något före @, och efter @ en
    punkt som varken står först eller sist.
    """
    if " " in text or text.count("@") != 1:
        return False
    at = text.index("@")
    local = text[:at]
    domain = text[at + 1:]
    if local == "":
        return False
    if "." not in domain:
        return False
    if domain.startswith(".") or domain.endswith("."):
        return False
    return True


# Uppgift 2
def play_game_strict(secret, low, high, max_attempts):
    """Som play_game, men en ogiltig gissning kostar ett försök."""
    print(f"Jag tänker på ett tal mellan {low} och {high}.")
    print(f"Du har {max_attempts} försök.")

    for attempt in range(1, max_attempts + 1):
        remaining = max_attempts - attempt
        text = input(f"Gissa ett tal mellan {low} och {high}: ")
        try:
            guess = parse_int_in_range(text, low, high)
        except ValueError as error:
            print(f"Ogiltig gissning ({error}). Det kostade ett försök. {remaining} försök kvar.")
            continue

        if guess == secret:
            print(f"Rätt! Talet var {secret}. Du klarade det på {attempt} försök.")
            return True
        if guess < secret:
            print(f"För lågt. {remaining} försök kvar.")
        else:
            print(f"För högt. {remaining} försök kvar.")

    print(f"Slut på försök. Talet var {secret}.")
    return False


# Uppgift 3
def main_with_difficulty():
    """Låt spelaren välja svårighet, och starta play_game med rätt inställningar."""
    while True:
        level = input("Välj svårighet (lätt/medel/svår): ").strip().lower()
        if level == "lätt":
            high = 10
            attempts = 5
            break
        elif level == "medel":
            high = 100
            attempts = 7
            break
        elif level == "svår":
            high = 1000
            attempts = 10
            break
        print("Skriv lätt, medel eller svår.")

    secret = random.randint(1, high)
    return play_game(secret, 1, high, attempts)


# Uppgift 4
def count_valid_usernames(candidates):
    count = 0
    for candidate in candidates:
        if is_valid_username(candidate):
            count = count + 1
    return count


# Uppgift 5
def main_with_tally():
    """Spela omgång efter omgång och håll räkningen tills spelaren vill sluta."""
    wins = 0
    losses = 0
    while True:
        if play_game(random.randint(LOW, HIGH), LOW, HIGH, MAX_ATTEMPTS):
            wins = wins + 1
        else:
            losses = losses + 1
        print(f"Vinster: {wins}, förluster: {losses}")
        again = input("Spela igen? (j/n) ").strip().lower()
        if again != "j":
            break
    return wins, losses
