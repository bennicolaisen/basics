"""Pure conversion functions: temperature, distance, and duration.

Every function here takes plain numbers in, returns plain numbers (or a
tuple) out, and raises no exceptions except where the input is genuinely
meaningless (negative elapsed time). No `input()`/`print()` belongs in
this module — that separation is what lets the CLI stay thin and these
functions stay trivially testable.
"""

KM_PER_MILE = 1.609344


def celsius_to_fahrenheit(c: float) -> float:
    """Convert a Celsius temperature to Fahrenheit."""
    return c * 9 / 5 + 32


def fahrenheit_to_celsius(f: float) -> float:
    """Convert a Fahrenheit temperature to Celsius."""
    return (f - 32) * 5 / 9


def km_to_miles(km: float) -> float:
    """Convert a distance in kilometres to miles."""
    return km / KM_PER_MILE


def miles_to_km(mi: float) -> float:
    """Convert a distance in miles to kilometres."""
    return mi * KM_PER_MILE


def seconds_to_hms(total_seconds: int) -> tuple[int, int, int]:
    """Break a non-negative whole number of seconds into (hours, minutes, seconds).

    Raises ValueError for negative input — "negative elapsed time" isn't a
    value this function can meaningfully produce an answer for, so it
    rejects it at the boundary rather than returning nonsense (like negative
    hours with positive minutes).
    """
    if total_seconds < 0:
        raise ValueError(f"total_seconds must be >= 0, got {total_seconds}")

    total_seconds = int(total_seconds)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return (hours, minutes, seconds)
