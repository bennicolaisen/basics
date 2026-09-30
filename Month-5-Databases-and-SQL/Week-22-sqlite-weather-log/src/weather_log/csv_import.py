"""Turn CSV files into plain Python values for `store.py` to insert.

This is the boundary where text from outside becomes typed data, so it's
where malformed *text* is caught (a temperature that isn't a number).
Whether a well-formed value is *allowed* (no negative rain, a known kind
of weather) is the database schema's job, not this module's.
"""

import csv
from pathlib import Path

from weather_log.store import Observation


def _number(text: str, field: str, line: int) -> float:
    try:
        return float(text)
    except ValueError:
        raise ValueError(f"line {line}: {field} must be a number, got {text!r}") from None


def read_cities(path: Path) -> list[tuple[str, str, int]]:
    """Read `name,country,population` rows."""
    with path.open(newline="", encoding="utf-8") as file:
        return [(row["name"], row["country"], int(row["population"])) for row in csv.DictReader(file)]


def read_observations(path: Path) -> list[Observation]:
    """Read observation rows; an empty `wind_ms` field means the reading is missing."""
    observations = []
    with path.open(newline="", encoding="utf-8") as file:
        # Line 1 is the header, so data starts on line 2.
        for line, row in enumerate(csv.DictReader(file), start=2):
            observations.append(
                Observation(
                    city=row["city"],
                    observed_on=row["observed_on"],
                    temp_max_c=_number(row["temp_max_c"], "temp_max_c", line),
                    temp_min_c=_number(row["temp_min_c"], "temp_min_c", line),
                    precipitation_mm=_number(row["precipitation_mm"], "precipitation_mm", line),
                    wind_ms=_number(row["wind_ms"], "wind_ms", line) if row["wind_ms"] else None,
                    conditions=row["conditions"],
                )
            )
    return observations
