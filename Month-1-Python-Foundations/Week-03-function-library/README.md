# Week 3 — Function Library

## Purpose

Functions aren't just "a way to avoid retyping code" — they're the unit
of *decomposition*: the tool for breaking a problem too big to hold in
your head all at once into pieces small enough to write, name, test, and
reuse individually. This week builds a small library of statistics and
text-processing functions the proper way, and then, deliberately, next
to it, builds the *same* functionality the wrong way — one giant
tangled function — so the difference isn't abstract.

## Objectives

The code in this project concretely demonstrates:

- Functions with typed parameters and return values, each with a single
  clear responsibility.
- Default parameter values (`is_palindrome`'s `ignore_case`/
  `ignore_spaces`) and how they let a function serve both a common case
  (no arguments) and less common ones (explicit `False`) from one
  definition.
- Local scope: every variable inside a function body (`avg`, `counts`,
  `ordered`, ...) exists only for that call and can't leak out or collide
  with a same-named variable elsewhere.
- Raising `ValueError` at a function's boundary when its precondition
  (non-empty input) isn't met, instead of returning a misleading
  placeholder value.
- Why decomposing a monolith into small, named, single-purpose functions
  makes code more testable, more reusable, and easier to read — using
  `legacy_report.py` as the concrete counterexample.

## Concepts Refresher

**Parameters, arguments, and return values.** A parameter is a name in a
function's definition (`def mean(nums):` — `nums` is the parameter); an
argument is the actual value passed at the call site (`mean([1, 2, 3])`
— `[1, 2, 3]` is the argument). `return` sends a value back to the
caller and immediately exits the function — nothing after a `return` in
the same branch runs.

**Default parameter values.** `def is_palindrome(s, ignore_case=True,
ignore_spaces=True):` means calling `is_palindrome("Racecar")` is exactly
equivalent to `is_palindrome("Racecar", ignore_case=True,
ignore_spaces=True)` — the default just fills in when the caller doesn't
specify. This is what lets one function serve the common case (ignore
case and spacing, which is what "palindrome" usually means colloquially)
and the strict case (`is_palindrome(s, ignore_case=False,
ignore_spaces=False)`) without being two functions.

**Scope.** A variable assigned inside a function body only exists while
that call is running, and is invisible outside it. Call `mean([1,2,3])`
and then `mean([4,5,6])` — the second call's `nums` and the arithmetic
inside it have no memory of the first call at all; every call starts
clean. This is *why* pure functions (no shared mutable state, same
input always gives same output) are so much easier to reason about and
test than code that reads or writes some variable declared outside the
function.

**Why `ValueError` on empty input, specifically.** `mean([])` doing
`sum([]) / len([])` is `0 / 0`, a `ZeroDivisionError` — a real error, but
one that reports the *symptom* (division by zero) rather than the actual
*problem* (there's no data to average). Checking `if not nums: raise
ValueError(...)` up front turns an accidental, confusing failure into a
deliberate, clearly-worded one. This is the same "validate at the
boundary" idea from Weeks 1-2, now applied to a function's own
precondition rather than to user-typed text.

**Decomposition: why `legacy_report.py` is bad, concretely.** Open
`legacy_report.py` and look at `handle_data(d, t)`. It:

- Does at least six unrelated things in one function body: mean,
  median, mode, standard deviation, word count, and palindrome check —
  none of which depend on each other.
- Names nothing meaningfully (`d`, `t`, `sd_list`, `vs`, `bestc`) — the
  names carry no information about what the value *is*, only vague
  hints about its type or role.
- Can't be tested piece-by-piece. Want to check that the median logic
  is right? You must also supply valid text for the palindrome check and
  read the median back out of a dict that also contains five other
  answers — there's no way to test "just the median part" because there
  is no "just the median part," only the whole function.
- Can't be reused. Need just the mode of a different list elsewhere in
  a program? The only option is to copy-paste the mode-finding loop out
  of the middle of `handle_data`, because it was never its own function.

Compare that to `stats.mode(nums)`: it does one thing, its name says
what that thing is, it can be called and checked in isolation (see
`tests/test_stats.py`), and it can be reused anywhere a mode is needed —
including from inside a rewritten, decomposed version of
`handle_data` itself. That gap — same behavior, wildly different
testability/reusability/readability — is the entire argument for
decomposing code into functions, and it's the "Try It Yourself" exercise
below.

## Design & Architecture

```
Week-03-function-library/
├── conftest.py                          - adds src/ to sys.path for pytest
├── src/
│   └── function_library/
│       ├── __init__.py
│       ├── stats.py                      - mean/median/mode/stddev (tested)
│       ├── text_utils.py                 - word_count/is_palindrome (tested)
│       └── legacy_report.py              - BAD example, not tested, for refactoring
└── tests/
    ├── test_stats.py
    └── test_text_utils.py
```

`stats.py` and `text_utils.py` are independent of each other — neither
imports the other — because they're genuinely unrelated concerns
(numbers vs. text) that only happen to get combined into one report by
*calling* code, not by being tangled together in their own
implementations. `legacy_report.py` is kept separate from both,
excluded from the test suite on purpose, and documented in its own
module docstring as a teaching artifact rather than part of the real
library.

## How to Build & Run

This week's library has no CLI of its own — import the functions where
you need them:

```bash
cd Month-1-Python-Foundations/Week-03-function-library
PYTHONPATH=src python3 -c "
from function_library.stats import mean, stddev
print(mean([1, 2, 3, 4, 5]))
print(stddev([1, 2, 3, 4, 5]))
"
```

## Testing

```bash
cd Month-1-Python-Foundations/Week-03-function-library
python3 -m pytest -q
```

`test_stats.py` covers a typical case, a single-element list (the edge
case that makes population vs. sample stddev diverge in behavior), a
tie in `mode` (checked to resolve to the smaller value), and the empty-
list `ValueError` for all four functions, plus a known textbook value
for `stddev` to catch an arithmetic mistake that a random-looking
example wouldn't. `test_text_utils.py` covers typical input, empty
input, internal/leading/trailing whitespace for `word_count`, and both
default and disabled behavior of each `is_palindrome` flag.
`legacy_report.py` has no tests — it's a teaching artifact, not part of
the tested API (see its own module docstring).

## Try It Yourself

1. **The main exercise**: refactor `legacy_report.py`'s `handle_data`
   into a new, cleanly decomposed function (e.g. `build_report(data,
   text)`) that calls `stats.mean`, `stats.median`, `stats.mode`,
   `stats.stddev`, `text_utils.word_count`, and `text_utils.is_palindrome`
   instead of recomputing each of them inline. It should return the same
   dict shape `handle_data` does. Then write tests for *your* version —
   something `handle_data` could never get, since testing it means
   testing six behaviors at once.
2. Add `range_(nums)` (note the trailing underscore — `range` is a
   builtin) returning `max(nums) - min(nums)`, raising `ValueError` on
   empty input like the rest of `stats.py`.
3. Add `most_common_word(text: str) -> str` to `text_utils.py`, reusing
   `word_count`'s tokenizing approach (`text.split()`) rather than
   inventing a new one, and decide/document what it should do with a
   tie.
4. `mode`'s tie-break rule (smallest value wins) is one reasonable
   choice among several (most-recently-seen, all tied values as a list,
   ...). Change it to return *all* tied values as a sorted list instead
   of just one, update its docstring and tests to match, and consider
   what that changes about `mode`'s return type.
5. Write a `**kwargs`-based function `describe(nums, **flags)` that
   calls only the stats functions whose name is a key in `flags` set to
   `True` (e.g. `describe([1,2,3], mean=True, mode=True)` returns just
   `{"mean": ..., "mode": ...}`), to get hands-on practice with
   `**kwargs` beyond what this week's reference code uses.
