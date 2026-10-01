"""Funktioner för text."""


def word_count(text: str) -> int:
    """Antalet ord i texten.

    text.split() utan argument delar vid alla mellanslag, tabbar och
    radbrytningar, och ignorerar mellanslag i början och slutet. Därför
    räknas "  a  b " som två ord.
    """
    return len(text.split())


def is_palindrome(text: str, ignore_case: bool = True, ignore_spaces: bool = True) -> bool:
    """Är texten densamma framlänges och baklänges?

    Som standard bortser funktionen från stora och små bokstäver och från
    mellanslag, eftersom det är så man brukar mena ("Ni talar bra latin").
    Skicka in ignore_case=False eller ignore_spaces=False för att kräva
    exakt likhet tecken för tecken.
    """
    if ignore_spaces:
        text = text.replace(" ", "")
    if ignore_case:
        text = text.lower()
    return text == text[::-1]
