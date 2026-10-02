"""Facit vecka 26: de nya SQL-funktionerna. Resten finns i weather_api.store."""

import sqlite3

from weather_api.store import OBSERVATION_FIELDS

# Uppgift 1: fälten som får ändras. observed_on ingår inte: datumet är en del
# av adressen (/observations/{date}), och adressen till en sak ska inte ändras.
PATCHABLE_FIELDS = [name for name in OBSERVATION_FIELDS if name != "observed_on"]


def update_observation(conn: sqlite3.Connection, city_name: str, day: str, changes: dict) -> bool:
    """Uppgift 1: ändra bara de fält som finns i `changes`. False om observationen saknas.

    Kolumnnamnen i SET kommer från PATCHABLE_FIELDS, en fast lista i
    programmet, aldrig från klienten. Värdena skickas som parametrar.
    """
    columns = [name for name in PATCHABLE_FIELDS if name in changes]
    if not columns or set(changes) - set(columns):
        raise ValueError("changes must be a non-empty subset of PATCHABLE_FIELDS")
    assignments = ", ".join(f"{name} = :{name}" for name in columns)
    with conn:
        cursor = conn.execute(
            f"""
            UPDATE observations
            SET {assignments}
            WHERE observed_on = :day
              AND city_id = (SELECT id FROM cities WHERE name = :city)
            """,
            {**changes, "day": day, "city": city_name},
        )
    return cursor.rowcount == 1


def delete_city(conn: sqlite3.Connection, name: str) -> bool:
    """Uppgift 2: ta bort en stad. Schemats ON DELETE CASCADE tar bort dess observationer."""
    with conn:
        cursor = conn.execute("DELETE FROM cities WHERE name = ?", (name,))
    return cursor.rowcount == 1


def summary(conn: sqlite3.Connection, city_name: str, start: str, end: str) -> sqlite3.Row | None:
    """Uppgift 3: antal, medelvärde av dagens högsta och total nederbörd. None om staden saknas.

    Datumvillkoret står i ON, inte i WHERE (vecka 21): då ger ett intervall
    utan observationer ändå en rad, med antalet 0.
    """
    return conn.execute(
        """
        SELECT c.name                                      AS city,
               COUNT(o.id)                                 AS observations,
               ROUND(AVG(o.temp_max_c), 1)                 AS average_high_c,
               ROUND(COALESCE(SUM(o.precipitation_mm), 0), 1) AS total_precipitation_mm
        FROM cities AS c
        LEFT JOIN observations AS o
               ON o.city_id = c.id
              AND o.observed_on BETWEEN :start AND :end
        WHERE c.name = :city
        GROUP BY c.id, c.name
        """,
        {"city": city_name, "start": start, "end": end},
    ).fetchone()
