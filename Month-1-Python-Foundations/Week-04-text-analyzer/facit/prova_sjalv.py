"""Facit till "Prova själv" i vecka 4. Förklaringarna finns i FACIT.md."""

import string

from text_analyzer import analyzer


# Uppgift 1: ta bara bort skiljetecken i början och slutet av varje ord.
def tokenize_keep_inner(text: str) -> list[str]:
    words = [word.strip(string.punctuation) for word in text.lower().split()]
    return [word for word in words if word != ""]


# Uppgift 2
def bigrams(tokens: list[str]) -> list[tuple[str, str]]:
    """Alla par av ord som står efter varandra."""
    return [(tokens[i], tokens[i + 1]) for i in range(len(tokens) - 1)]


def most_common_bigram(tokens: list[str]) -> tuple[str, str]:
    pairs = bigrams(tokens)
    if len(pairs) == 0:
        raise ValueError("det behövs minst två ord för att bilda ett par")
    frequencies = analyzer.word_frequencies(pairs)
    return analyzer.top_n_words(frequencies, 1)[0][0]


# Uppgift 3
def top_n_words_without(frequencies: dict[str, int], n: int, stopwords: set[str]) -> list[tuple[str, int]]:
    kept = {word: count for word, count in frequencies.items() if word not in stopwords}
    return analyzer.top_n_words(kept, n)


# Uppgift 4: räknar på alla ord, med upprepningar (se FACIT.md).
def average_word_length(tokens: list[str]) -> float:
    if len(tokens) == 0:
        raise ValueError("det finns inga ord att räkna på")
    return sum([len(token) for token in tokens]) / len(tokens)


# Uppgift 5: samma funktioner som i analyzer.py, med kontroll av n.
def _check_n(n: int) -> None:
    if n <= 0:
        raise ValueError(f"n måste vara minst 1, fick {n}")


def top_n_words(frequencies: dict[str, int], n: int) -> list[tuple[str, int]]:
    _check_n(n)
    return analyzer.top_n_words(frequencies, n)


def longest_words(tokens: list[str], n: int) -> list[str]:
    _check_n(n)
    return analyzer.longest_words(tokens, n)
