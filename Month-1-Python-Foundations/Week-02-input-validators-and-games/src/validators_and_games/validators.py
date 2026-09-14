"""Pure string/int validators with no I/O.

Each function here answers one yes/no or parse question about a string,
with every edge case (empty string, boundary lengths, off-by-one) decided
explicitly rather than left to whatever Python's default behaviour
happens to be.
"""


def is_valid_username(s: str) -> bool:
    """A valid username is 3-20 characters, starts with a letter, and
    contains only letters, digits, and underscores thereafter (and, in
    fact, throughout — the first-character rule is a subset of that)."""
    if not (3 <= len(s) <= 20):
        return False
    if not s[0].isalpha():
        return False
    return all(ch.isalnum() or ch == "_" for ch in s)


def is_strong_password(s: str) -> bool:
    """A strong password is at least 8 characters and contains at least
    one uppercase letter, one lowercase letter, one digit, and one
    non-alphanumeric symbol."""
    if len(s) < 8:
        return False
    has_upper = any(ch.isupper() for ch in s)
    has_lower = any(ch.islower() for ch in s)
    has_digit = any(ch.isdigit() for ch in s)
    has_symbol = any(not ch.isalnum() for ch in s)
    return has_upper and has_lower and has_digit and has_symbol


def parse_int_in_range(s: str, lo: int, hi: int) -> int:
    """Parse `s` as an int and check it falls within [lo, hi] (inclusive).

    Raises ValueError with a message naming the actual problem — not an
    integer, or an integer but out of range — rather than letting a bare
    `int(s)` failure or a silently-wrong comparison propagate.
    """
    try:
        value = int(s)
    except ValueError:
        raise ValueError(f"{s!r} is not a valid integer") from None

    if value < lo or value > hi:
        raise ValueError(f"{value} is out of range [{lo}, {hi}]")

    return value
