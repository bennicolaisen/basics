"""Facit vecka 22: veckans store.py med uppgift 1-4 gjorda. Se FACIT.md.

Allt som inte ändras importeras från weather_log.store, så den här filen
innehåller bara det som är nytt eller annorlunda.
"""

import sqlite3
from dataclasses import asdict
from pathlib import Path

from weather_log.store import (  # noqa: F401  (importeras för att användas härifrån)
    Observation,
    add_city,
    city_observations,
    correct_precipitation,
    import_observations,
    record,
    summary,
)

SCHEMA_SQL = Path(__file__).parent / "schema.sql"


class CityNameTakenError(ValueError):
    """Uppgift 2: det nya namnet används redan av en annan stad."""


class CityInUseError(ValueError):
    """Uppgift 3: staden har fortfarande observationer eller varningar."""


def open_log(path: str | Path = ":memory:") -> sqlite3.Connection:
    """Som veckans open_log, men med facit-schemat."""
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA_SQL.read_text(encoding="utf-8"))
    return conn


# Uppgift 1 --------------------------------------------------------------


def record_or_replace(conn: sqlite3.Connection, observation: Observation) -> None:
    """Lägg till en observation, eller ersätt den som redan finns för samma stad och dag.

    Allt sker i EN sats. Med SELECT först och sedan INSERT eller UPDATE
    finns ett ögonblick där ett annat program hinner skriva emellan.
    """
    with conn:
        cursor = conn.execute(
            """
            INSERT INTO observations
                (city_id, observed_on, temp_max_c, temp_min_c, precipitation_mm, wind_ms, conditions)
            SELECT id, :observed_on, :temp_max_c, :temp_min_c, :precipitation_mm, :wind_ms, :conditions
            FROM cities
            WHERE name = :city
            ON CONFLICT (city_id, observed_on) DO UPDATE SET
                temp_max_c       = excluded.temp_max_c,
                temp_min_c       = excluded.temp_min_c,
                precipitation_mm = excluded.precipitation_mm,
                wind_ms          = excluded.wind_ms,
                conditions       = excluded.conditions
            """,
            asdict(observation),
        )
        if cursor.rowcount == 0:
            raise ValueError(f"unknown city: {observation.city!r}")


# Uppgift 2 --------------------------------------------------------------


def rename_city(conn: sqlite3.Connection, old: str, new: str) -> None:
    """Byt namn på en stad. Om det nya namnet är upptaget ändras ingenting.

    Det är databasens UNIQUE-regel som avgör om namnet är upptaget; den här
    funktionen översätter bara databasens fel till ett begripligt fel.
    """
    if not new or not new.strip():
        raise ValueError("the new name must not be blank")
    try:
        with conn:
            cursor = conn.execute("UPDATE cities SET name = ? WHERE name = ?", (new, old))
    except sqlite3.IntegrityError:
        raise CityNameTakenError(f"there is already a city called {new!r}") from None
    if cursor.rowcount == 0:
        raise ValueError(f"unknown city: {old!r}")


# Uppgift 3 --------------------------------------------------------------


def delete_city(conn: sqlite3.Connection, name: str) -> None:
    """Ta bort en stad som inte har några observationer eller varningar kvar."""
    try:
        with conn:
            cursor = conn.execute("DELETE FROM cities WHERE name = ?", (name,))
    except sqlite3.IntegrityError:
        observations, warnings = conn.execute(
            """
            SELECT (SELECT COUNT(*) FROM observations WHERE city_id = c.id),
                   (SELECT COUNT(*) FROM warnings     WHERE city_id = c.id)
            FROM cities AS c
            WHERE c.name = ?
            """,
            (name,),
        ).fetchone()
        raise CityInUseError(
            f"{name} still has {observations} observation(s) and {warnings} warning(s); "
            "delete those first if the city really should go"
        ) from None
    if cursor.rowcount == 0:
        raise ValueError(f"unknown city: {name!r}")


# Uppgift 4 --------------------------------------------------------------


def add_warning(
    conn: sqlite3.Connection,
    city: str,
    level: str,
    message: str,
    starts_on: str,
    ends_on: str,
) -> int:
    """Lägg till en varning för en stad och returnera dess id."""
    with conn:
        cursor = conn.execute(
            """
            INSERT INTO warnings (city_id, level, message, starts_on, ends_on)
            SELECT id, :level, :message, :starts_on, :ends_on
            FROM cities
            WHERE name = :city
            """,
            {"city": city, "level": level, "message": message, "starts_on": starts_on, "ends_on": ends_on},
        )
        if cursor.rowcount == 0:
            raise ValueError(f"unknown city: {city!r}")
    return cursor.lastrowid


def active_warnings(conn: sqlite3.Connection, on_date: str) -> list[sqlite3.Row]:
    """Varningar som gäller ett visst datum, med stadens namn. Första och sista dagen räknas."""
    return conn.execute(
        """
        SELECT c.name, w.level, w.message, w.starts_on, w.ends_on
        FROM warnings AS w
        JOIN cities AS c ON c.id = w.city_id
        WHERE ? BETWEEN w.starts_on AND w.ends_on
        ORDER BY c.name, w.starts_on
        """,
        (on_date,),
    ).fetchall()
