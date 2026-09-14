# Week 4 — Text Analyzer

## Purpose

This is the Month 1 capstone: a small but real program that reads a
whole text file and reports on it, built entirely out of the four core
collection types — `list`, `dict`, `set`, and `tuple` — plus the
comprehension/generator syntax that makes working with them concise
instead of verbose. Everything from Weeks 1-3 (pure functions, control
flow, decomposition) gets exercised again here, but the *new* material
is choosing the right collection for each sub-problem.

## Objectives

The code in this project concretely demonstrates:

- `list` for an ordered, possibly-repeating sequence (tokens, in the
  order they appeared).
- `dict` for a mapping from a key to derived data (word -> how many
  times it appeared).
- `set` for "the distinct values, order and duplicates don't matter"
  (unique words).
- `tuple` for a small, fixed, heterogeneous bundle of values returned
  together (`(word, count)` pairs).
- Sorting with a custom key function, including a composite key for
  primary-sort-then-tiebreak (`top_n_words`, `longest_words`).
- Reading a file path from `sys.argv`, with a sensible fallback when
  none is given.

## Concepts Refresher

**Why four different collection types, and not just `list` for
everything.** Each collection type encodes a *guarantee* about what you
can assume when you use it, and picking the wrong one either throws
away information or makes you do extra work to get information the
right type would have given you for free:

- `list` — ordered, allows duplicates, indexable by position. Right for
  `tokenize`'s output: word order and repetition both matter (that's
  exactly what `word_frequencies` counts).
- `dict` — a key maps to a value, keys are unique. Right for "how many
  times did each word appear" — the word *is* the natural key, and a
  `list` of `(word, count)` pairs would make "what's the count for
  'fox'?" an O(n) search instead of an O(1) lookup.
- `set` — unique values, unordered, fast membership testing. Right for
  "the distinct words," where order is meaningless and duplicates would
  just be wrong (a word either appeared or it didn't).
- `tuple` — an ordered, fixed-size, typically-immutable bundle. Right
  for `(word, count)`: it's exactly two related values that travel
  together and are never mutated after creation, unlike a `list`, which
  signals "this might grow, shrink, or be reordered."

**Comprehensions.** A comprehension is a compact way to build a
collection from another one. `tokenize` doesn't use one (there's no
per-token transform beyond what `.translate()`/`.split()` already do),
but the same shape recurs constantly in this style of code:

```python
[word for word in tokens if len(word) > 5]        # list comprehension
{word for word in tokens}                          # set comprehension  (≈ set(tokens))
{word: len(word) for word in tokens}                # dict comprehension
```

Each reads as "for every `word` in `tokens`, keep/transform it like
*this*" — the same logic as a `for` loop appending to an empty
collection, just without the three lines of setup/append/return
boilerplate. Reach for one when the loop body is "compute one value (or
filter) per item and collect the results" — reach for a plain loop when
the body does something else too (printing, raising, mutating multiple
things).

**Sorting with a key function, including tie-breaking.**
`sorted(iterable, key=...)` doesn't compare items directly — it computes
`key(item)` for each item and sorts by *that*. `top_n_words` uses:

```python
sorted(freqs.items(), key=lambda pair: (-pair[1], pair[0]))
```

The key for each `(word, count)` pair is the tuple `(-count, word)`.
Python compares tuples element-by-element, so this sorts primarily by
`-count` (negating turns "sort ascending" into "highest count first"
without a separate `reverse=True`, which would also reverse the
alphabetical tiebreak) and, only when two counts are equal, falls
through to comparing `word` alphabetically. That's the general pattern
for "sort by X, and when X ties, break the tie by Y."

**`set` for uniqueness, before sorting by length.** `longest_words`
calls `unique_words(tokens)` before sorting — sorting a `list` with
repeats by length would let one very long word that appears five times
crowd out four other distinct words from the top-`n` results. Converting
to a `set` first ensures each *distinct* word is only considered once.

## Design & Architecture

```
Week-04-text-analyzer/
├── conftest.py                       - adds src/ to sys.path for pytest
├── src/
│   └── text_analyzer/
│       ├── __init__.py
│       ├── analyzer.py                - pure collection-based functions (tested)
│       ├── cli.py                     - reads a file, prints a report
│       └── data/
│           └── sample.txt             - bundled fallback text
└── tests/
    └── test_analyzer.py
```

Same pure-logic/thin-CLI split as every earlier week: `analyzer.py`
never touches a file or the terminal, so every function in it takes
plain data in and returns plain data out. `cli.py` is the only place
that knows about `sys.argv` or the filesystem — it reads a path (or
falls back to the bundled `data/sample.txt`), calls the `analyzer.py`
functions, and formats their results for a human to read.

## How to Build & Run

```bash
cd Month-1-Python-Foundations/Week-04-text-analyzer

# Analyze the bundled sample:
PYTHONPATH=src python3 -m text_analyzer.cli

# Analyze your own file:
PYTHONPATH=src python3 -m text_analyzer.cli path/to/some.txt
```

## Testing

```bash
cd Month-1-Python-Foundations/Week-04-text-analyzer
python3 -m pytest -q
```

`test_analyzer.py` covers: punctuation stripping in the middle of a word
(`"it's"` -> `"its"`) and at sentence boundaries, case-insensitivity,
text that's whitespace/punctuation-only (both should tokenize to an
empty list, not crash), and — the trickiest part of this week's logic —
the tie-break rule in both `top_n_words` (equal counts fall back to
alphabetical order) and `longest_words` (equal lengths fall back to
alphabetical order, and duplicate tokens must be deduplicated before
ranking).

## Try It Yourself

1. `tokenize` currently strips punctuation from inside words too
   (`"don't"` -> `"dont"`). Change it to instead strip punctuation only
   from the *edges* of each whitespace-separated token, so `"don't"`
   stays `"don't"` but `"(great)"` becomes `"great"`. Update/add tests
   for the new behavior before checking it against the old tests — some
   of the existing expectations will need to change, and figuring out
   *which ones* and *why* is part of the exercise.
2. Add `bigrams(tokens: list[str]) -> list[tuple[str, str]]`, returning
   every consecutive pair of words (e.g. `["a","b","c"]` ->
   `[("a","b"), ("b","c")]`), and `most_common_bigram(tokens)` built on
   top of it, reusing `word_frequencies`'s counting approach rather than
   rewriting it for tuples.
3. Add a `--stopwords` CLI flag (or a `stopwords: set[str] | None = None`
   parameter threaded through the relevant `analyzer.py` functions) that
   excludes common words like "the", "a", "is" from `top_n_words`.
4. Add `average_word_length(tokens: list[str]) -> float`, raising
   `ValueError` on an empty token list (consistent with Week 3's
   stats functions), and decide whether it should operate on `tokens`
   (counting repeats) or `unique_words(tokens)` (not) — write a test
   that pins down which you chose and why.
5. Right now `top_n_words` and `longest_words` both take a plain `n:
   int`. Make them reject `n <= 0` with a `ValueError` instead of
   silently returning an empty or truncated list, and add tests for
   `n == 0` and negative `n`.
