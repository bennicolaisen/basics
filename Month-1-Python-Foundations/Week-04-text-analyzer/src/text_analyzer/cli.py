"""CLI report: reads a text file (from argv, or a bundled sample) and
prints word-count statistics computed entirely by `analyzer.py`.
"""

import sys
from pathlib import Path

from text_analyzer.analyzer import (
    longest_words,
    tokenize,
    top_n_words,
    unique_words,
    word_frequencies,
)

SAMPLE_PATH = Path(__file__).parent / "data" / "sample.txt"
TOP_N = 5


def load_text(argv: list[str]) -> str:
    """Read the file named in argv[1], or fall back to the bundled sample."""
    path = Path(argv[1]) if len(argv) > 1 else SAMPLE_PATH
    return path.read_text(encoding="utf-8")


def print_report(text: str, top_n: int = TOP_N) -> None:
    tokens = tokenize(text)
    freqs = word_frequencies(tokens)
    top = top_n_words(freqs, top_n)
    longest = longest_words(tokens, top_n)

    print(f"Total words: {len(tokens)}")
    print(f"Unique words: {len(unique_words(tokens))}")

    print(f"\nTop {top_n} most frequent words:")
    for word, count in top:
        print(f"  {word:<15} {count}")

    print(f"\n{top_n} longest distinct words:")
    for word in longest:
        print(f"  {word} ({len(word)} chars)")


def main() -> None:
    text = load_text(sys.argv)
    print_report(text)


if __name__ == "__main__":
    main()
