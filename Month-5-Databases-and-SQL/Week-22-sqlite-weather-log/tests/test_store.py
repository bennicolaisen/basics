import sqlite3

import pytest

from weather_log import store
from weather_log.store import Observation


def observation(**changes) -> Observation:
    values = {
        "city": "Kiruna",
        "observed_on": "2026-09-21",
        "temp_max_c": 7.8,
        "temp_min_c": 0.9,
        "precipitation_mm": 0.2,
        "wind_ms": 3.4,
        "conditions": "cloud",
    }
    return Observation(**{**values, **changes})


def count_observations(conn) -> int:
    return conn.execute("SELECT COUNT(*) FROM observations").fetchone()[0]


@pytest.fixture
def conn():
    conn = store.open_log()
    store.add_city(conn, "Kiruna", "Sweden", 22423)
    store.add_city(conn, "Oslo", "Norway", 717710)
    return conn


class TestAddCity:
    def test_returns_the_new_id(self, conn):
        assert store.add_city(conn, "Bergen", "Norway", 291940) == 3

    def test_text_with_quotes_is_stored_as_is(self, conn):
        # With parameters, an apostrophe is just a character, not the end of a string.
        store.add_city(conn, "Val d'Isère", "France", 1600)
        assert conn.execute("SELECT name FROM cities WHERE id = 3").fetchone()["name"] == "Val d'Isère"


class TestRecord:
    def test_stores_every_field_against_the_right_city(self, conn):
        store.record(conn, observation(city="Oslo", wind_ms=None))
        row = conn.execute(
            "SELECT c.name, o.* FROM observations o JOIN cities c ON c.id = o.city_id"
        ).fetchone()
        assert row["name"] == "Oslo"
        assert row["observed_on"] == "2026-09-21"
        assert row["wind_ms"] is None

    def test_unknown_city_is_rejected_and_nothing_is_stored(self, conn):
        with pytest.raises(ValueError, match="unknown city: 'Atlantis'"):
            store.record(conn, observation(city="Atlantis"))
        assert count_observations(conn) == 0

    def test_schema_violation_surfaces_as_integrity_error(self, conn):
        with pytest.raises(sqlite3.IntegrityError):
            store.record(conn, observation(precipitation_mm=-3))


class TestImportObservations:
    def test_inserts_all_and_returns_the_count(self, conn):
        batch = [observation(observed_on=f"2026-09-2{day}") for day in range(1, 8)]
        assert store.import_observations(conn, batch) == 7
        assert count_observations(conn) == 7

    def test_invalid_row_rolls_back_the_rows_before_it(self, conn):
        batch = [
            observation(observed_on="2026-09-21"),
            observation(observed_on="2026-09-22"),
            observation(observed_on="2026-09-23", conditions="hail"),
        ]
        with pytest.raises(sqlite3.IntegrityError):
            store.import_observations(conn, batch)
        assert count_observations(conn) == 0

    def test_unknown_city_mid_batch_rolls_back_too(self, conn):
        batch = [observation(), observation(city="Atlantis", observed_on="2026-09-22")]
        with pytest.raises(ValueError):
            store.import_observations(conn, batch)
        assert count_observations(conn) == 0

    def test_earlier_committed_data_survives_a_failed_import(self, conn):
        store.record(conn, observation(observed_on="2026-09-20"))
        with pytest.raises(sqlite3.IntegrityError):
            store.import_observations(conn, [observation(), observation()])  # duplicate day
        assert count_observations(conn) == 1

    def test_changes_are_committed_and_visible_to_other_connections(self, tmp_path):
        path = tmp_path / "weather.db"
        writer = store.open_log(path)
        store.add_city(writer, "Kiruna", "Sweden", 22423)
        store.import_observations(writer, [observation()])
        reader = store.open_log(path)
        assert count_observations(reader) == 1


class TestCorrectPrecipitation:
    def test_updates_only_the_matching_observation(self, conn):
        store.import_observations(conn, [observation(), observation(observed_on="2026-09-22")])
        store.correct_precipitation(conn, "Kiruna", "2026-09-22", 4.5)
        values = [row[0] for row in conn.execute("SELECT precipitation_mm FROM observations ORDER BY observed_on")]
        assert values == [0.2, 4.5]

    def test_missing_observation_is_reported(self, conn):
        with pytest.raises(ValueError, match="no observation"):
            store.correct_precipitation(conn, "Kiruna", "2026-12-24", 1.0)

    def test_correction_is_still_held_to_the_schema(self, conn):
        store.record(conn, observation())
        with pytest.raises(sqlite3.IntegrityError):
            store.correct_precipitation(conn, "Kiruna", "2026-09-21", -1.0)


class TestDeleteCity:
    def test_removes_the_city_and_cascades_to_its_observations(self, conn):
        store.import_observations(conn, [observation(), observation(city="Oslo")])
        store.delete_city(conn, "Kiruna")
        assert [row["name"] for row in store.summary(conn)] == ["Oslo"]
        assert count_observations(conn) == 1

    def test_unknown_city_is_reported(self, conn):
        with pytest.raises(ValueError, match="unknown city"):
            store.delete_city(conn, "Atlantis")


class TestReading:
    def test_city_observations_are_in_date_order_and_readable_by_name(self, conn):
        store.import_observations(conn, [observation(observed_on="2026-09-23"), observation(observed_on="2026-09-21")])
        rows = store.city_observations(conn, "Kiruna")
        assert [row["observed_on"] for row in rows] == ["2026-09-21", "2026-09-23"]

    def test_injection_attempt_is_treated_as_an_ordinary_name(self, conn):
        # Pasted into the SQL text, this would make the WHERE clause
        # `c.name = '' OR '1'='1'`, which is true for every row.
        store.record(conn, observation())
        assert store.city_observations(conn, "' OR '1'='1") == []

    def test_summary_includes_cities_without_observations(self, conn):
        store.import_observations(conn, [observation(), observation(observed_on="2026-09-22", temp_max_c=6.2)])
        kiruna, oslo = store.summary(conn)
        assert tuple(kiruna) == ("Kiruna", 2, "2026-09-21", "2026-09-22", 7.0, 0.4)
        assert tuple(oslo) == ("Oslo", 0, None, None, None, None)
