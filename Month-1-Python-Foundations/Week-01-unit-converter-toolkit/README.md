# Week 1 — Unit Converter Toolkit

## Purpose

Every program, no matter how large, is built out of the same small moves:
hold a value in a name, do arithmetic on it, and show the result to a
human in a form they can read. Before control flow, functions, or data
structures can matter, those moves have to be automatic. This week is
about making them automatic again using a problem simple enough that the
*syntax* can't hide behind the *problem*: converting between units.

## Objectives

The code in this project concretely demonstrates:

- Declaring and using variables of `int`, `float`, and `str` types.
- Writing arithmetic expressions that correctly encode a real-world
  formula (temperature, distance, and time conversions).
- Formatted output with f-strings, including fixed decimal precision and
  zero-padding.
- Turning user-typed text into numbers safely, with `try`/`except`
  instead of trusting the input.
- Keeping "does math" and "talks to the user" in separate functions/files
  so the math can be tested without a human typing anything.

## Concepts Refresher

**Variables and types.** A variable is a name bound to a value; Python
figures out the value's type from what's assigned (`x = 3` makes `x` an
`int`, `x = 3.0` makes it a `float`). This module leans on exactly three
types: `int` (whole numbers — used for seconds and for hours/minutes/
seconds in the result), `float` (numbers with a fractional part —
temperatures and distances), and `str` (the raw text a user types before
it's been parsed into a number).

**Expressions vs. statements.** `c * 9 / 5 + 32` is an *expression* — it
computes a value but doesn't, by itself, do anything with it. `f =
celsius_to_fahrenheit(c)` is a *statement* — it runs the expression and
binds the result to a name. Every function body in `converters.py` is a
single expression being `return`ed; there's no hidden state, which is
exactly why they're easy to test: same input, same output, always.

**Integer division and `divmod`.** `seconds_to_hms` needs to split a
count of seconds into hours, minutes, and leftover seconds. `//` is
floor (whole-number) division and `%` is the remainder; `divmod(a, b)`
returns `(a // b, a % b)` in one call, which is exactly "how many whole
`b`s fit in `a`, and what's left over." Applying it twice —
`divmod(total, 3600)` then `divmod(remainder, 60)` — peels off hours,
then minutes, leaving seconds:

```python
hours, remainder = divmod(total_seconds, 3600)
minutes, seconds = divmod(remainder, 60)
```

**Formatted strings (f-strings).** `f"{value:.2f}"` embeds `value` in the
string, formatted as fixed-point with 2 digits after the decimal point.
`f"{h:02d}"` formats an integer, zero-padded to width 2 — that's what
turns `h=1, m=1, s=1` into the readable `"01:01:01"` instead of `"1:1:1"`.

**Input validation at the boundary.** A user can type literally anything.
`float("banana")` raises `ValueError` — that's not a bug to avoid, it's
the mechanism used here: wrap the parse in `try`/`except ValueError`,
and on failure, print a message and prompt again instead of letting the
program crash. This validation only happens once, right where text
enters the program (`cli.py`); once a value is a `float` or `int`, the
rest of the code never has to wonder if it's "really" a number.

**Why negative seconds is an error but negative Celsius isn't.**
`celsius_to_fahrenheit(-40)` is a perfectly meaningful physical
temperature. But `seconds_to_hms(-10)` is being asked "what wall-clock
time is -10 seconds after midnight?" — there's no sensible answer, so
the function raises `ValueError` immediately rather than returning
something like `(0, 0, -10)` that looks plausible but is wrong. This is
the general principle: reject nonsense at the boundary, don't let it
quietly propagate.

## Design & Architecture

```
Week-01-unit-converter-toolkit/
├── conftest.py                       - adds src/ to sys.path for pytest
├── src/
│   └── converter_toolkit/
│       ├── __init__.py
│       ├── converters.py             - pure conversion functions (tested)
│       └── cli.py                    - menu loop, input parsing (not tested)
└── tests/
    └── test_converters.py
```

`converters.py` and `cli.py` are split deliberately: `converters.py` has
no `input()`/`print()` anywhere in it, so every function in it is a pure
calculation that pytest can call directly and check against a known
answer. `cli.py` imports those functions and is *only* responsible for
the menu loop, prompting, and re-prompting on bad input — there's no math
in it to get wrong, and nothing in it needs its own test suite because it
has (almost) no independent logic. This split — pure logic in one place,
I/O in another — is the single most reusable idea in this whole project;
it comes back in every later week.

## How to Build & Run

No build step — it's plain Python 3.10+ with no third-party dependencies.
Because `converter_toolkit` lives under `src/`, put `src` on the path
when running it directly:

```bash
cd Month-1-Python-Foundations/Week-01-unit-converter-toolkit
PYTHONPATH=src python3 -m converter_toolkit.cli
```

Then follow the on-screen menu.

## Testing

```bash
cd Month-1-Python-Foundations/Week-01-unit-converter-toolkit
python3 -m pytest -q
```

`conftest.py` puts `src/` on `sys.path` automatically, so no flags or
environment variables are needed. The suite covers, for every converter:
a normal value, zero, a negative value (where meaningful), a round-trip
(converting there and back should return the original number), and the
boundary cases for `seconds_to_hms` (exactly one minute, exactly one
hour, just under an hour, and a value spanning more than 24 hours).
`seconds_to_hms(-1)` is checked to raise `ValueError`.

## Try It Yourself

1. Add `fahrenheit_to_kelvin(f)` and `kelvin_to_fahrenheit(k)`, including
   a check that rejects a Kelvin value below absolute zero (0 K).
2. Add `hms_to_seconds(h, m, s)`, the inverse of `seconds_to_hms`, and
   decide (and test) what it should do with a negative `m` or `s` even
   when `h` is positive.
3. Add a "convert a whole batch" CLI option that reads a comma-separated
   list of numbers on one line (e.g. `12,50,100`) and prints every
   conversion — without changing any function in `converters.py`.
4. `celsius_to_fahrenheit` and `fahrenheit_to_celsius` are exact inverses
   in real-number math but floating-point rounding can make a round trip
   land a tiny bit off. Write a test that deliberately picks a value
   where this shows up, and explain in a comment why `pytest.approx` is
   the right tool rather than `==`.
5. Add `mph_to_kmh(mph)` and `kmh_to_mph(kmh)` reusing `km_to_miles`/
   `miles_to_km` rather than duplicating the conversion factor.
