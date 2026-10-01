"""All of the API's SQL. Nothing here knows about HTTP.

Same approach as Week 22: values reach SQLite as parameters, writes run
inside `with conn:` so they commit or roll back as a whole, and the
schema's constraints are the final word on what data is valid.
"""

import sqlite3
from pathlib import Path

PACKAGE_DIR = Path(__file__).parent
SCHEMA_SQL = PACKAGE_DIR / "schema.sql"
SAMPLE_SQL = PACKAGE_DIR / "data" / "sample_data.sql"

OBSERVATION_FIELDS = ["observed_on", "temp_max_c", "temp_min_c", "precipitation_mm", "wind_ms", "conditions"]
_OBSERVATION_COLUMNS = ", ".join(f"o.{field}" for field in OBSERVATION_FIELDS)


def open_log(path: str | Path = ":memory:") -> sqlite3.Connection:
    # The HTTP server answers requests on a different thread from the one
    # that opened the connection. It handles one request at a time, so
    # sharing a single connection is safe; sqlite3 just needs to be told.
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA_SQL.read_text(encoding="utf-8"))
    return conn


def load_sample(conn: sqlite3.Connection) -> bool:
    """Fill an empty log with the sample week. Returns False if it already had data."""
    if conn.execute("SELECT COUNT(*) FROM cities").fetchone()[0]:
        return False
    conn.executescript(SAMPLE_SQL.read_text(encoding="utf-8"))
    return True


def cities(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute("SELECT name, country, population FROM cities ORDER BY name").fetchall()


def city(conn: sqlite3.Connection, name: str) -> sqlite3.Row | None:
    return conn.execute("SELECT name, country, population FROM cities WHERE name = ?", (name,)).fetchone()


def add_city(conn: sqlite3.Connection, name: str, country: str, population: int) -> None:
    with conn:
        conn.execute(
            "INSERT INTO cities (name, country, population) VALUES (?, ?, ?)",
            (name, country, population),
        )


def observations(conn: sqlite3.Connection, city_name: str, start: str, end: str) -> list[sqlite3.Row]:
    return conn.execute(
        f"""
        SELECT {_OBSERVATION_COLUMNS}
        FROM observations AS o
        JOIN cities AS c ON c.id = o.city_id
        WHERE c.name = ? AND o.observed_on BETWEEN ? AND ?
        ORDER BY o.observed_on
        """,
        (city_name, start, end),
    ).fetchall()


def observation(conn: sqlite3.Connection, city_name: str, day: str) -> sqlite3.Row | None:
    return conn.execute(
        f"""
        SELECT {_OBSERVATION_COLUMNS}
        FROM observations AS o
        JOIN cities AS c ON c.id = o.city_id
        WHERE c.name = ? AND o.observed_on = ?
        """,
        (city_name, day),
    ).fetchone()


def add_observation(conn: sqlite3.Connection, city_name: str, values: dict) -> bool:
    """Insert an observation; returns False if the city doesn't exist."""
    with conn:
        cursor = conn.execute(
            """
            INSERT INTO observations
                (city_id, observed_on, temp_max_c, temp_min_c, precipitation_mm, wind_ms, conditions)
            SELECT id, :observed_on, :temp_max_c, :temp_min_c, :precipitation_mm, :wind_ms, :conditions
            FROM cities
            WHERE name = :city
            """,
            {**values, "city": city_name},
        )
    return cursor.rowcount == 1


def delete_observation(conn: sqlite3.Connection, city_name: str, day: str) -> bool:
    """Delete one observation; returns False if there was none to delete."""
    with conn:
        cursor = conn.execute(
            """
            DELETE FROM observations
            WHERE observed_on = ?
              AND city_id = (SELECT id FROM cities WHERE name = ?)
            """,
            (day, city_name),
        )
    return cursor.rowcount == 1
