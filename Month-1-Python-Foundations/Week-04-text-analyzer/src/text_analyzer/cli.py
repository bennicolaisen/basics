"""Läser en textfil och skriver ut statistik om orden.

    python starta.py                  # analysera den medföljande exempeltexten
    python starta.py min_text.txt     # analysera en egen fil
"""

import sys
from pathlib import Path

from text_analyzer.analyzer import longest_words, tokenize, top_n_words, unique_words, word_frequencies

SAMPLE_PATH = Path(__file__).parent / "data" / "sample.txt"
TOP_N = 5


def read_text(path: Path) -> str:
    """Läs hela filen som text."""
    with open(path, encoding="utf-8") as file:
        return file.read()


def print_report(text: str, top_n: int = TOP_N) -> None:
    tokens = tokenize(text)
    frequencies = word_frequencies(tokens)

    print(f"Antal ord: {len(tokens)}")
    print(f"Olika ord: {len(unique_words(tokens))}")

    print(f"\nDe {top_n} vanligaste orden:")
    for word, count in top_n_words(frequencies, top_n):
        print(f"  {word:<15} {count}")

    print(f"\nDe {top_n} längsta orden:")
    for word in longest_words(tokens, top_n):
        print(f"  {word} ({len(word)} tecken)")


def main() -> None:
    # sys.argv är listan med ord som skrevs i terminalen: sys.argv[0] är
    # programmets namn, sys.argv[1] det första argumentet efter det.
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
    else:
        path = SAMPLE_PATH
    print_report(read_text(path))


if __name__ == "__main__":
    main()
