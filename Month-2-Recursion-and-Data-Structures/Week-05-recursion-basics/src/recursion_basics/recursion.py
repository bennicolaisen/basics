"""Six small functions, each solved recursively — no loops anywhere in this
module. That's deliberate: the point of Week 5 isn't "get the right answer",
it's "practice spotting the base case and the recursive case" until doing so
becomes automatic. Every function below documents both explicitly.

A recursive function always needs two things:

- a **base case**: the input small/simple enough to answer directly, with no
  further recursive call. Without one, the function calls itself forever.
- a **recursive case**: how to reduce the current problem to a *smaller*
  version of the same problem, plus what to do with that smaller answer once
  you have it.
"""


def factorial(n: int) -> int:
    """Return n! = n * (n-1) * ... * 1, with 0! = 1.

    Base case: n == 0 -> return 1 (nothing left to multiply).
    Recursive case: n > 0 -> return n * factorial(n - 1).
    """
    if n < 0:
        raise ValueError(f"n must be >= 0, got {n}")

    if n == 0:
        return 1
    return n * factorial(n - 1)


def fibonacci(n: int) -> int:
    """Return the n-th Fibonacci number (0-indexed: fib(0) = 0, fib(1) = 1).

    Base cases: n == 0 -> return 0; n == 1 -> return 1 (both answered
    directly, no further call needed).
    Recursive case: n > 1 -> return fibonacci(n - 1) + fibonacci(n - 2).

    This is the classic *exponentially slow* recursive implementation
    (roughly 2^n calls) — deliberately left that way here. Week 5 is about
    the recursive pattern, not efficiency; memoization is a Try It Yourself
    exercise, not something this reference solves for you.
    """
    if n < 0:
        raise ValueError(f"n must be >= 0, got {n}")

    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


def sum_digits(n: int) -> int:
    """Return the sum of the decimal digits of a non-negative integer n.

    Base case: n < 10 -> return n itself (a single digit is its own sum).
    Recursive case: n >= 10 -> return (n % 10) + sum_digits(n // 10), i.e.
    the last digit plus the sum of everything before it.
    """
    if n < 0:
        raise ValueError(f"n must be >= 0, got {n}")

    if n < 10:
        return n
    return (n % 10) + sum_digits(n // 10)


def reverse_string(s: str) -> str:
    """Return s reversed.

    Base case: s == "" (or a single character) -> return s unchanged,
    a string of length 0 or 1 is already its own reverse.
    Recursive case: otherwise -> return reverse_string(s[1:]) + s[0], i.e.
    reverse everything after the first character, then put the first
    character on the end.
    """
    if len(s) <= 1:
        return s
    return reverse_string(s[1:]) + s[0]


def is_palindrome_recursive(s: str) -> bool:
    """Return True if s reads the same forwards and backwards.

    Base case: len(s) <= 1 -> return True (an empty or single-character
    string is trivially a palindrome).
    Recursive case: otherwise -> the first and last characters must match,
    *and* the substring with both ends stripped off must itself be a
    palindrome: s[0] == s[-1] and is_palindrome_recursive(s[1:-1]).

    Comparison is exact (case-sensitive, punctuation/spaces count) — no
    normalization is done here, that's left as a Try It Yourself exercise.
    """
    if len(s) <= 1:
        return True
    return s[0] == s[-1] and is_palindrome_recursive(s[1:-1])


def power(base: float, exp: int) -> float:
    """Return base raised to the power exp, for a non-negative integer exp.

    Base case: exp == 0 -> return 1 (anything to the power 0 is 1, by
    definition — including base == 0).
    Recursive case: exp > 0 -> return base * power(base, exp - 1).
    """
    if exp < 0:
        raise ValueError(f"exp must be >= 0, got {exp}")

    if exp == 0:
        return 1
    return base * power(base, exp - 1)
