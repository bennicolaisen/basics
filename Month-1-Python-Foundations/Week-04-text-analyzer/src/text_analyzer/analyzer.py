"""Funktioner som analyserar en text: ord, ordfrekvenser och de längsta orden.

Ingen av funktionerna läser filer eller skriver ut något; det gör cli.py.
Varje funktion använder den samlingstyp som passar uppgiften:
listor för ord i ordning, en dictionary för "ord -> antal", en mängd för
unika ord och tupler för par av (ord, antal).
"""

import string


def tokenize(text: str) -> list[str]:
    """Dela upp texten i ord: små bokstäver, utan skiljetecken.

    Skiljetecken tas bort helt, även inne i ord, så "don't" blir "dont".
    Det är en förenkling (se "Prova själv").
    """
    cleaned = ""
    for character in text.lower():
        if character not in string.punctuation:
            cleaned = cleaned + character
    return cleaned.split()


def word_frequencies(tokens: list[str]) -> dict[str, int]:
    """Räkna hur många gånger varje ord förekommer: {ord: antal}."""
    frequencies: dict[str, int] = {}
    for token in tokens:
        frequencies[token] = frequencies.get(token, 0) + 1
    return frequencies


def by_count_then_word(pair: tuple[str, int]) -> tuple[int, str]:
    """Sorteringsnyckel för (ord, antal): högst antal först, sedan bokstavsordning.

    Minustecknet vänder ordningen för antalet utan att vända
    bokstavsordningen.
    """
    word, count = pair
    return (-count, word)


def top_n_words(frequencies: dict[str, int], n: int) -> list[tuple[str, int]]:
    """De n vanligaste orden som (ord, antal), vanligast först.

    Vid lika antal sorteras orden i bokstavsordning, så att svaret blir
    detsamma varje gång.
    """
    ordered = sorted(frequencies.items(), key=by_count_then_word)
    return ordered[:n]


def unique_words(tokens: list[str]) -> set[str]:
    """De olika orden, utan dubbletter."""
    return set(tokens)


def by_length_then_word(word: str) -> tuple[int, str]:
    """Sorteringsnyckel: längst först, sedan bokstavsordning."""
    return (-len(word), word)


def longest_words(tokens: list[str], n: int) -> list[str]:
    """De n längsta olika orden, längst först.

    Dubbletter tas bort först, så att ett långt ord som förekommer fem
    gånger bara tar en av platserna.
    """
    ordered = sorted(unique_words(tokens), key=by_length_then_word)
    return ordered[:n]
