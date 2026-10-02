"""Funktioner som kontrollerar text: användarnamn, lösenord och heltal.

Varje funktion svarar på en fråga om en text. Inga av dem använder
input() eller print(), så de går att testa automatiskt.
"""


def is_valid_username(text):
    """Är text ett giltigt användarnamn?

    Regler: 3–20 tecken långt, första tecknet är en bokstav, och alla
    tecken är bokstäver, siffror eller understreck (_).
    """
    if len(text) < 3 or len(text) > 20:
        return False
    if not text[0].isalpha():
        return False
    for character in text:
        if not (character.isalnum() or character == "_"):
            return False
    return True


def is_strong_password(text):
    """Är text ett starkt lösenord?

    Regler: minst 8 tecken, och minst en stor bokstav, en liten bokstav,
    en siffra och ett annat tecken (som ! eller #).
    """
    if len(text) < 8:
        return False

    has_upper = False
    has_lower = False
    has_digit = False
    has_symbol = False
    for character in text:
        if character.isupper():
            has_upper = True
        elif character.islower():
            has_lower = True
        elif character.isdigit():
            has_digit = True
        else:
            has_symbol = True
    return has_upper and has_lower and has_digit and has_symbol


def parse_int_in_range(text, low, high):
    """Gör om text till ett heltal mellan low och high (båda inräknade).

    Om texten inte är ett heltal, eller om talet ligger utanför
    intervallet, kastas ett ValueError med ett meddelande som säger vad
    som var fel.
    """
    try:
        value = int(text)
    except ValueError:
        # "from None" gör att bara vårt meddelande visas, inte int():s.
        raise ValueError(f"'{text}' är inte ett heltal") from None

    if value < low or value > high:
        raise ValueError(f"{value} ligger utanför {low}–{high}")
    return value
