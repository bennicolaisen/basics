# Facit: Övning 1.11 – Klockslag. Förklaring i FACIT.md.

MINUTES_PER_DAY = 24 * 60


def to_minutes(clock):
    return int(clock[:2]) * 60 + int(clock[3:])


def minutes_between(start, end):
    return (to_minutes(end) - to_minutes(start)) % MINUTES_PER_DAY
