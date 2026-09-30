"""The rules in schema.sql, tested by writing raw SQL straight at the database.

These deliberately bypass `store.py`: the point of putting rules in the
schema is that they hold no matter which program does the writing.
"""

import sqlite3

import pytest

from weather_log.store import SCHEMA_SQL, open_log

INSERT_OBSERVATION = """
    INSERT INTO observations
        (city_id, observed_on, temp_max_c, temp_min_c, precipitation_mm, wind_ms, conditions)
    VALUES (:city_id, :observed_on, :temp_max_c, :temp_min_c, :precipitation_mm, :wind_ms, :conditions)
"""

VALID = {
    "city_id": 1,
    "observed_on": "2026-09-21",
    "temp_max_c": 16.2,
    "temp_min_c": 9.1,
    "precipitation_mm": 0.0,
    "wind_ms": 4.2,
    "conditions": "sun",
}


@pytest.fixture
def conn():
    conn = open_log()
    conn.execute("INSERT INTO cities (id, name, country, population) VALUES (1, 'Stockholm', 'Sweden', 984748)")
    return conn


def insert(conn, **changes):
    conn.execute(INSERT_OBSERVATION, {**VALID, **changes})


def test_valid_row_is_accepted(conn):
    insert(conn)
    assert conn.execute("SELECT COUNT(*) FROM observations").fetchone()[0] == 1


def test_missing_wind_reading_is_allowed(conn):
    insert(conn, wind_ms=None)


class TestForeignKey:
    def test_observation_for_nonexistent_city_is_rejected(self, conn):
        with pytest.raises(sqlite3.IntegrityError, match="FOREIGN KEY"):
            insert(conn, city_id=99)

    def test_sqlite_does_not_enforce_it_unless_asked(self):
        # Why open_log runs PRAGMA foreign_keys = ON: without it, the same
        # insert silently creates an observation that points at nothing.
        plain = sqlite3.connect(":memory:")
        plain.executescript(SCHEMA_SQL.read_text(encoding="utf-8"))
        plain.execute(INSERT_OBSERVATION, {**VALID, "city_id": 99})
        assert plain.execute("SELECT COUNT(*) FROM observations").fetchone()[0] == 1

    def test_deleting_a_city_deletes_its_observations(self, conn):
        insert(conn)
        conn.execute("DELETE FROM cities WHERE id = 1")
        assert conn.execute("SELECT COUNT(*) FROM observations").fetchone()[0] == 0


class TestCheckConstraints:
    @pytest.mark.parametrize(
        "changes",
        [
            {"precipitation_mm": -0.1},
            {"wind_ms": -1.0},
            {"conditions": "hail"},
            {"conditions": "Sun"},
            {"temp_min_c": 20.0},  # low above the high
        ],
    )
    def test_impossible_values_are_rejected(self, conn, changes):
        with pytest.raises(sqlite3.IntegrityError, match="CHECK"):
            insert(conn, **changes)

    @pytest.mark.parametrize("bad_date", ["2026-9-21", "21/09/2026", "2026-02-30", "yesterday", ""])
    def test_only_real_iso_dates_are_accepted(self, conn, bad_date):
        with pytest.raises(sqlite3.IntegrityError, match="CHECK"):
            insert(conn, observed_on=bad_date)

    def test_negative_population_is_rejected(self, conn):
        with pytest.raises(sqlite3.IntegrityError, match="CHECK"):
            conn.execute("INSERT INTO cities (name, country, population) VALUES ('Nowhere', 'Sweden', -1)")


class TestUniqueness:
    def test_two_cities_cannot_share_a_name(self, conn):
        with pytest.raises(sqlite3.IntegrityError, match="UNIQUE"):
            conn.execute("INSERT INTO cities (name, country, population) VALUES ('Stockholm', 'Sweden', 1)")

    def test_one_observation_per_city_per_day(self, conn):
        insert(conn)
        with pytest.raises(sqlite3.IntegrityError, match="UNIQUE"):
            insert(conn, temp_max_c=17.0)


def test_reopening_a_log_file_keeps_its_data(tmp_path):
    path = tmp_path / "weather.db"
    first = open_log(path)
    with first:
        first.execute("INSERT INTO cities (name, country, population) VALUES ('Oslo', 'Norway', 717710)")
    first.close()

    second = open_log(path)  # runs the schema again: IF NOT EXISTS makes that harmless
    assert second.execute("SELECT name FROM cities").fetchall()[0]["name"] == "Oslo"
