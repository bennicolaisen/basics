# Week 2 — Input Validators and Games

## Purpose

Control flow is what turns a straight-line script into a program that
reacts: it checks conditions, repeats work until something is true,
and bails out of a loop early when it should. This week rebuilds that
instinct with two deliberately unglamorous tools — string validators —
and one small, satisfying application of them: a number-guessing game
that has to keep prompting a fallible human until it gets a usable
answer.

## Objectives

The code in this project concretely demonstrates:

- `if`/`elif`/`else` for branching on multiple conditions.
- `while` loops that repeat until a condition changes (re-prompting on
  bad input; the guessing game's attempt counter).
- `for` loops with early exit, including `break` on a win.
- Boundary-condition thinking: exact minimums, exact maximums, and
  one-past-each-end, applied systematically rather than by accident.
- Composing a previously-written validator (`parse_int_in_range`) into a
  new piece of control flow (the game loop) instead of rewriting it.

## Concepts Refresher

**`if`/`elif`/`else` chains.** Python checks conditions top to bottom and
runs the first branch that matches; `elif` is "otherwise, check this
next," and `else` is "nothing above matched." `is_strong_password`
doesn't actually need `elif` — it computes four independent booleans and
`and`s them together — which is itself worth noticing: a chain of
`elif`s is for *mutually exclusive* cases, not for accumulating several
independent yes/no facts. Reach for `and`/`or` on booleans before reaching
for a taller `if`/`elif` chain.

**`while` loops and the "keep asking until it's valid" pattern.** A
`while True:` loop with a `return`/`break` inside is the standard shape
for "repeat until I get something I can use":

```python
while True:
    raw = input("Guess: ")
    try:
        return parse_int_in_range(raw, lo, hi)
    except ValueError as exc:
        print(f"Invalid guess: {exc}")
```

The loop has no explicit condition that changes each iteration — it
relies entirely on `return` inside the `try` to exit. That's fine and
common: the *only* way out is success, so there's nothing to track in a
loop variable.

**`for` loops, `break`, and `continue`.** `play_game` uses
`for attempt in range(1, max_attempts + 1):` specifically because the
number of iterations is *known in advance* (the attempt limit) — that's
the signal to prefer `for` over `while`. `break` (via `return` here)
exits the loop entirely on a correct guess. `continue` skips the rest of
the current iteration and moves to the next one; it doesn't appear in
this code because `prompt_guess`'s inner `while` loop already prevents an
invalid guess from ever reaching the comparison logic — but if attempts
were tracked differently (e.g. counting invalid guesses too), `continue`
would be the tool to skip charging an attempt for bad input.

**Boundary conditions, systematically.** "3 to 20 characters" has *four*
interesting lengths to check, not one: 2 (just under), 3 (exactly the
minimum), 20 (exactly the maximum), and 21 (just over). It's tempting to
test only the "happy path" (something comfortably in range) — that
proves the function works for typical input but says nothing about
whether the boundary itself was coded correctly (`<` vs `<=` is a classic
off-by-one). `is_valid_username`, `is_strong_password`, and
`parse_int_in_range` are all tested at every one of their boundaries for
exactly this reason.

**Validators that raise vs. validators that return bool.**
`is_valid_username`/`is_strong_password` return `True`/`False` — the
caller decides what to do about it. `parse_int_in_range` instead raises
`ValueError` — because a parse failure isn't just "no," it's "no, and
here's specifically why" (not a number vs. out of range), and an
exception is what lets that detail travel to wherever it's handled
without every caller threading it through manually.

## Design & Architecture

```
Week-02-input-validators-and-games/
├── conftest.py                          - adds src/ to sys.path for pytest
├── src/
│   └── validators_and_games/
│       ├── __init__.py
│       ├── validators.py                - pure validators (tested)
│       └── game.py                      - CLI game built on validators.py
└── tests/
    └── test_validators.py
```

Same split as Week 1: `validators.py` has zero I/O and is fully unit
tested; `game.py` is the only place `input()`/`print()` appear, and its
own logic is as small as possible — a loop, an attempt counter, and
calls out to `parse_int_in_range` for anything involving actually
parsing text. `game.py` does still contain real control-flow logic (the
attempt-limit loop, the higher/lower branch) beyond pure I/O plumbing,
which is why, unlike Week 1's CLI, it exposes `play_game(...)` as a
function with injectable parameters (`rng`) rather than only a bare
`main()` — that's what would make it testable if this week's scope asked
for it.

## How to Build & Run

```bash
cd Month-1-Python-Foundations/Week-02-input-validators-and-games
PYTHONPATH=src python3 -m validators_and_games.game
```

Guess the number; the game tells you higher/lower after each valid
guess and gives up after the attempt limit.

## Testing

```bash
cd Month-1-Python-Foundations/Week-02-input-validators-and-games
python3 -m pytest -q
```

The suite hits every boundary named in the spec: `is_valid_username` at
lengths 0, 2, 3, 20, and 21, plus bad first characters and disallowed
characters; `is_strong_password` at 7 vs. 8 characters and with each of
the four required character classes individually missing;
`parse_int_in_range` at both inclusive range endpoints, one step outside
each end, an empty string, a non-numeric string, and a float-looking
string. The game itself (`game.py`) isn't unit tested, per this week's
scope — it's a thin loop over an already-tested validator.

## Try It Yourself

1. Add `is_valid_email(s)` (a deliberately simplified rule — e.g. exactly
   one `@`, at least one `.` after it, no spaces — not full RFC 5322) and
   test its boundaries the same systematic way this week's validators
   are tested.
2. Change the game so an *invalid* guess (unparseable or out of range)
   still costs an attempt, instead of re-prompting for free. Decide how
   to tell the player which kind of failure happened, and update the
   loop accordingly.
3. Add a difficulty menu (easy/medium/hard) that changes `lo`, `hi`, and
   `max_attempts` before `play_game` is called — without modifying
   `play_game` itself.
4. Write `count_valid_usernames(candidates: list[str]) -> int` using a
   `for` loop and `is_valid_username`, then rewrite it as a one-line list
   comprehension with `sum(...)` and confirm both give the same answer
   on a test list.
5. Add a "play again?" outer loop around `play_game()` that keeps a
   running win/loss tally across rounds until the player chooses to stop.
