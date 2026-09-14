"""Pure text-analysis functions built on list, dict, set, and tuple.

Nothing here reads a file or touches `input()`/`print()` — see `cli.py`
for the thin layer that turns these into a runnable report.
"""

import string

_PUNCTUATION_TABLE = str.maketrans("", "", string.punctuation)


def tokenize(text: str) -> list[str]:
    """Lowercase `text`, strip punctuation, and split on whitespace.

    Punctuation is removed outright (not just at word edges), so
    `"don't"` becomes `"dont"` and `"well-known"` becomes `"wellknown"` —
    a single word each, rather than being split into fragments around
    the punctuation. That's a deliberate simplification for this week's
    scope, not the only reasonable choice (see "Try It Yourself").
    """
    lowered = text.lower()
    stripped = lowered.translate(_PUNCTUATION_TABLE)
    return stripped.split()


def word_frequencies(tokens: list[str]) -> dict[str, int]:
    """Count occurrences of each token, as a dict of token -> count."""
    freqs: dict[str, int] = {}
    for token in tokens:
        freqs[token] = freqs.get(token, 0) + 1
    return freqs


def top_n_words(freqs: dict[str, int], n: int) -> list[tuple[str, int]]:
    """The `n` most frequent (word, count) pairs from `freqs`.

    Sorted by count descending; ties are broken alphabetically (ascending)
    so the result is deterministic regardless of dict insertion order.
    """
    ordered = sorted(freqs.items(), key=lambda pair: (-pair[1], pair[0]))
    return ordered[:n]


def unique_words(tokens: list[str]) -> set[str]:
    """The distinct words in `tokens`, with duplicates collapsed."""
    return set(tokens)


def longest_words(tokens: list[str], n: int) -> list[str]:
    """The `n` longest distinct words in `tokens`.

    Operates on the *unique* words (a repeated long word only counts
    once), sorted by length descending; ties are broken alphabetically
    (ascending) for a deterministic result.
    """
    ordered = sorted(unique_words(tokens), key=lambda word: (-len(word), word))
    return ordered[:n]
