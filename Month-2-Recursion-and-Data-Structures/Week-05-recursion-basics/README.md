# Week 5 — Recursion Basics

## Purpose

Recursion is one of those topics that clicks, then un-clicks the moment
you look away for a few months — you remember "a function that calls
itself" but the actual mental model (what's on the call stack, why the
base case matters, how to trace one by hand) has gone soft. This week
rebuilds that model from first principles using small, self-contained
examples, before Week 6 asks you to use recursion to actually *search*
for something.

## Objectives

The code in `recursion.py` demonstrates:

- Identifying a **base case** and a **recursive case** for six different
  problems.
- Solving each one **without a single loop** — every repeated action here
  happens via a function calling itself, not `for`/`while`.
- Validating inputs at the boundary (`factorial`, `fibonacci`, `sum_digits`,
  `power` all reject inputs that would recurse forever or make no sense).
- Reading a recursive call by tracing it by hand, not just running it.

**No loops — this week is about the recursive pattern itself.** Every
one of `factorial`, `fibonacci`, `sum_digits`, `reverse_string`,
`is_palindrome_recursive`, and `power` is implemented purely recursively.

## Concepts Refresher

### What the call stack actually is

Every time a function is called — recursive or not — the running program
pushes a new **stack frame** onto the call stack: a small block of memory
holding that call's local variables, its parameters, and *where to resume
in the caller once this call returns*. When the function returns, its
frame is popped off and execution resumes exactly where the caller left
off, using the value that was returned.

A recursive call is not special to the call stack — it's just a function
call where the function being called happens to be the one already
running. Calling `factorial(4)` pushes a frame for `factorial(4)`; while
that frame is waiting on `factorial(3)`, it calls `factorial(3)`, which
pushes *another* frame, and so on. At any moment, the stack holds one
frame per call that has started but not yet returned — which is exactly
why deep recursion uses real memory, and why infinite recursion is a real
crash, not just a "logic bug that never returns."

### Why a missing or wrong base case blows up

If a recursive function never reaches a case that returns *without*
calling itself again, every call pushes another frame and none of them
ever pop. Python doesn't have unlimited stack space; past a depth limit
(by default, in the low thousands) it gives up and raises
`RecursionError: maximum recursion depth exceeded`. This is the recursive
equivalent of a `while True:` loop with no `break` — the difference is
just what you see when it fails: a loop hangs silently, a broken
recursion crashes loudly with a full stack trace.

Two common ways to write a base case wrong:

- **Missing it entirely** — e.g. writing `factorial` with only the
  recursive case and no `if n == 0: return 1`. There's never a call that
  answers directly, so it never stops.
- **Unreachable from some inputs** — e.g. counting down by 2 toward a
  base case of exactly `0`, called with an odd starting number. The
  base case exists, but the recursive case never actually produces the
  value that would trigger it.

### Tracing a recursive call by hand: `factorial(4)`

Tracing means writing out, step by step, every call that gets pushed
(expanding, going *deeper*) until a base case is hit, and then every
return value that gets used as each frame pops back off (collapsing,
coming back *up*):

```
Expanding (going down the stack):
  factorial(4)
  -> needs 4 * factorial(3)
      factorial(3)
      -> needs 3 * factorial(2)
          factorial(2)
          -> needs 2 * factorial(1)
              factorial(1)
              -> needs 1 * factorial(0)
                  factorial(0)
                  -> base case: return 1

Collapsing (returning back up the stack):
                  factorial(0) returns 1
              factorial(1) returns 1 * 1        = 1
          factorial(2) returns 2 * 1            = 2
      factorial(3) returns 3 * 2                = 6
  factorial(4) returns 4 * 6                    = 24
```

At the deepest point of this trace, the call stack has five frames on it
at once — `factorial(4)`, `factorial(3)`, `factorial(2)`, `factorial(1)`,
and `factorial(0)` — each one paused, waiting on the call below it to
return a value it needs before it can finish its own multiplication.
That "paused, waiting on my own subcall" state *is* what a stack frame
represents.

### Two-argument recursion branches the trace

`fibonacci(n)` calls itself *twice* per recursive case
(`fibonacci(n - 1) + fibonacci(n - 2)`), so its trace isn't a single
line going down and back up — it's a tree. `fibonacci(4)` calls
`fibonacci(3)` and `fibonacci(2)`; `fibonacci(3)` itself calls
`fibonacci(2)` and `fibonacci(1)`; note `fibonacci(2)` gets computed
*twice*, from two different branches, doing the same work both times.
That repeated work is exactly why the naive recursive Fibonacci is slow
— see Try It Yourself for fixing it.

## Design & Architecture

```
Week-05-recursion-basics/
├── README.md
├── conftest.py                       # adds src/ to sys.path for pytest
├── src/
│   └── recursion_basics/
│       ├── __init__.py
│       └── recursion.py              # all six recursive functions
└── tests/
    └── test_recursion.py
```

One module is enough here — none of the six functions depend on each
other or share state, so there's no reason to split them into separate
files. Splitting would add navigation overhead with no organizational
benefit at this size.

## How to Build & Run

No build step — pure standard library.

```bash
cd Month-2-Recursion-and-Data-Structures/Week-05-recursion-basics
python3 -c "from sys import path; path.insert(0, 'src'); from recursion_basics.recursion import factorial; print(factorial(5))"
```

Or open a REPL with `src` on the path:

```bash
PYTHONPATH=src python3
>>> from recursion_basics.recursion import fibonacci
>>> fibonacci(10)
55
```

## Testing

```bash
cd Month-2-Recursion-and-Data-Structures/Week-05-recursion-basics
python -m pytest -q
```

`conftest.py` puts `src/` on `sys.path`, so no extra flags or installed
package are needed. Tests cover, for every function: the base case
directly, a few ordinary values, and — for the four functions that
validate input — that a bad input raises `ValueError`.

## Try It Yourself

1. **Trace `fibonacci(6)` by hand before running it.** Write out, on
   paper, every call `fibonacci(6)` makes (it will branch — see the
   Concepts Refresher above), all the way down to base cases, and add up
   the return values back to the final answer. Only then run
   `fibonacci(6)` to check yourself.
2. **Count the calls.** Add a module-level counter that increments once
   per call to `fibonacci`, and print it after computing `fibonacci(20)`.
   Compare that count to `2 ** 20`. What does that tell you about how
   this implementation scales?
3. **Memoize `fibonacci`.** Rewrite it (as a new function, don't edit the
   reference) so previously-computed results are cached and reused,
   using a `dict` keyed by `n`. Re-run your counter from exercise 2 and
   compare.
4. **Tail-recursive `factorial`.** Rewrite `factorial` to take an
   accumulator parameter (`factorial_acc(n, acc=1)`) so the multiplication
   happens *before* the recursive call instead of after it returns.
   Trace `factorial_acc(4)` by hand the same way as the worked example
   above — what's different about the "collapsing" half of the trace?
5. **`count_up(n)` without a loop.** Write a recursive function that
   prints `1` through `n` in order. (Hint: what has to happen *before*
   the recursive call, versus *after* it, to get the order right?)

## Reflection

`factorial` and `power` are naturally recursive but would be at least as
easy — and more efficient — as loops (no repeated function-call overhead,
no stack depth limit to worry about). They're included here anyway
because the goal this week isn't "find the one true way to solve
`factorial`" — it's building comfort with the base-case/recursive-case
pattern on inputs simple enough that you can hold the whole trace in your
head. Week 6 is where recursion stops being optional: backtracking search
genuinely needs the call stack to hold your place across branching
choices, which a loop can't do without manually building its own stack.
