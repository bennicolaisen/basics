"""Every read and write the weather log does, as small functions over a connection.

All SQL in the program lives in this module, and every value that comes
from outside (a city name, a CSV field) reaches SQLite as a *parameter*,
never pasted into the SQL text. Functions that write wrap their work in
`with conn:`, which commits if the block finishes and rolls back if it
raises, so a failed call never leaves half its changes behind.
"""

import sqlite3
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path

SCHEMA_SQL = Path(__file__).parent / "schema.sql"


@dataclass(frozen=True)
class Observation:
    """One city's weather on one day, identified by city *name* rather than id."""

    city: str
    observed_on: str
    temp_max_c: float
    temp_min_c: float
    precipitation_mm: float
    wind_ms: float | None
    conditions: str


def open_log(path: str | Path = ":memory:") -> sqlite3.Connection:
    """Open (or create) a weather log database and make sure its tables exist."""
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    # SQLite ignores REFERENCES unless this is switched on, per connection.
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA_SQL.read_text(encoding="utf-8"))
    return conn


def add_city(conn: sqlite3.Connection, name: str, country: str, population: int) -> int:
    """Insert a city and return its new id."""
    with conn:
        cursor = conn.execute(
            "INSERT INTO cities (name, country, population) VALUES (?, ?, ?)",
            (name, country, population),
        )
    return cursor.lastrowid


def _insert_observation(conn: sqlite3.Connection, observation: Observation) -> int:
    # INSERT ... SELECT looks the city id up and inserts in one statement;
    # if no city has that name, the SELECT yields no row and nothing is inserted.
    cursor = conn.execute(
        """
        INSERT INTO observations
            (city_id, observed_on, temp_max_c, temp_min_c, precipitation_mm, wind_ms, conditions)
        SELECT id, :observed_on, :temp_max_c, :temp_min_c, :precipitation_mm, :wind_ms, :conditions
        FROM cities
        WHERE name = :city
        """,
        asdict(observation),
    )
    if cursor.rowcount == 0:
        raise ValueError(f"unknown city: {observation.city!r}")
    return cursor.lastrowid


def record(conn: sqlite3.Connection, observation: Observation) -> int:
    """Insert one observation and return its new id."""
    with conn:
        return _insert_observation(conn, observation)


def import_observations(conn: sqlite3.Connection, observations: Iterable[Observation]) -> int:
    """Insert every observation, or none of them if any one fails.

    Returns how many were inserted. The whole loop runs inside a single
    transaction, so an invalid row halfway through a file rolls back the
    rows before it too, and the file can be fixed and imported again
    without creating duplicates.
    """
    count = 0
    with conn:
        for observation in observations:
            _insert_observation(conn, observation)
            count += 1
    return count


def correct_precipitation(conn: sqlite3.Connection, city: str, observed_on: str, precipitation_mm: float) -> None:
    """Replace the precipitation reading of one existing observation."""
    with conn:
        cursor = conn.execute(
            """
            UPDATE observations
            SET precipitation_mm = :precipitation_mm
            WHERE observed_on = :observed_on
              AND city_id = (SELECT id FROM cities WHERE name = :city)
            """,
            {"city": city, "observed_on": observed_on, "precipitation_mm": precipitation_mm},
        )
        if cursor.rowcount == 0:
            raise ValueError(f"no observation for {city!r} on {observed_on}")


def delete_city(conn: sqlite3.Connection, name: str) -> None:
    """Delete a city; ON DELETE CASCADE removes its observations with it."""
    with conn:
        cursor = conn.execute("DELETE FROM cities WHERE name = ?", (name,))
        if cursor.rowcount == 0:
            raise ValueError(f"unknown city: {name!r}")


def city_observations(conn: sqlite3.Connection, city: str) -> list[sqlite3.Row]:
    """One city's observations in date order (empty if the city is unknown)."""
    return conn.execute(
        """
        SELECT o.observed_on, o.temp_max_c, o.temp_min_c, o.precipitation_mm, o.wind_ms, o.conditions
        FROM observations AS o
        JOIN cities AS c ON c.id = o.city_id
        WHERE c.name = ?
        ORDER BY o.observed_on
        """,
        (city,),
    ).fetchall()


def summary(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    """Per-city totals over everything logged, including cities with no observations yet."""
    return conn.execute(
        """
        SELECT c.name,
               COUNT(o.id)                       AS observations,
               MIN(o.observed_on)                AS first_day,
               MAX(o.observed_on)                AS last_day,
               ROUND(AVG(o.temp_max_c), 1)       AS average_high_c,
               ROUND(SUM(o.precipitation_mm), 1) AS total_precipitation_mm
        FROM cities AS c
        LEFT JOIN observations AS o ON o.city_id = c.id
        GROUP BY c.id, c.name
        ORDER BY c.name
        """
    ).fetchall()
