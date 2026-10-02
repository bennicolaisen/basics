"""Tester för facit (facit/store.py, facit/cli.py, facit/schema.sql). Se FACIT.md."""

import sqlite3

import pytest

from facit import cli as facit_cli
from facit import store
from facit.store import Observation


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


def count(conn, table: str) -> int:
    return conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]


@pytest.fixture
def conn():
    conn = store.open_log()
    store.add_city(conn, "Kiruna", "Sweden", 22423)
    store.add_city(conn, "Oslo", "Norway", 717710)
    return conn


class TestRecordOrReplace:
    def test_inserts_when_new(self, conn):
        store.record_or_replace(conn, observation())
        assert count(conn, "observations") == 1

    def test_replaces_instead_of_growing(self, conn):
        store.record_or_replace(conn, observation())
        store.record_or_replace(conn, observation(temp_max_c=9.0, wind_ms=None, conditions="sun"))
        assert count(conn, "observations") == 1
        row = store.city_observations(conn, "Kiruna")[0]
        assert (row["temp_max_c"], row["wind_ms"], row["conditions"]) == (9.0, None, "sun")

    def test_other_days_and_cities_are_untouched(self, conn):
        store.record_or_replace(conn, observation())
        store.record_or_replace(conn, observation(observed_on="2026-09-22"))
        store.record_or_replace(conn, observation(city="Oslo"))
        store.record_or_replace(conn, observation(temp_max_c=8.0))
        assert count(conn, "observations") == 3

    def test_replacement_is_still_held_to_the_schema(self, conn):
        store.record_or_replace(conn, observation())
        with pytest.raises(sqlite3.IntegrityError):
            store.record_or_replace(conn, observation(precipitation_mm=-1.0))
        assert store.city_observations(conn, "Kiruna")[0]["precipitation_mm"] == 0.2

    def test_unknown_city(self, conn):
        with pytest.raises(ValueError, match="unknown city"):
            store.record_or_replace(conn, observation(city="Atlantis"))


class TestRenameCity:
    def test_renames_and_keeps_the_observations(self, conn):
        store.record(conn, observation())
        store.rename_city(conn, "Kiruna", "Giron")
        assert len(store.city_observations(conn, "Giron")) == 1
        assert store.city_observations(conn, "Kiruna") == []

    def test_taken_name_is_refused_and_nothing_changes(self, conn):
        with pytest.raises(store.CityNameTakenError, match="Oslo"):
            store.rename_city(conn, "Kiruna", "Oslo")
        names = [row["name"] for row in conn.execute("SELECT name FROM cities ORDER BY id")]
        assert names == ["Kiruna", "Oslo"]

    def test_taken_name_error_is_a_value_error(self):
        assert issubclass(store.CityNameTakenError, ValueError)

    def test_unknown_old_name(self, conn):
        with pytest.raises(ValueError, match="unknown city"):
            store.rename_city(conn, "Atlantis", "Avalon")

    def test_blank_new_name(self, conn):
        with pytest.raises(ValueError, match="blank"):
            store.rename_city(conn, "Kiruna", "  ")


class TestDeleteWithoutCascade:
    def test_city_without_observations_can_be_deleted(self, conn):
        store.delete_city(conn, "Oslo")
        assert [row["name"] for row in store.summary(conn)] == ["Kiruna"]

    def test_city_with_observations_is_refused(self, conn):
        store.import_observations(conn, [observation(), observation(observed_on="2026-09-22")])
        with pytest.raises(store.CityInUseError, match="2 observation"):
            store.delete_city(conn, "Kiruna")
        assert count(conn, "cities") == 2
        assert count(conn, "observations") == 2

    def test_a_warning_also_keeps_the_city(self, conn):
        store.add_warning(conn, "Oslo", "yellow", "Wind", "2026-09-23", "2026-09-23")
        with pytest.raises(store.CityInUseError, match="1 warning"):
            store.delete_city(conn, "Oslo")

    def test_unknown_city(self, conn):
        with pytest.raises(ValueError, match="unknown city"):
            store.delete_city(conn, "Atlantis")


class TestWarnings:
    def test_active_warnings_on_a_date(self, conn):
        store.add_warning(conn, "Kiruna", "yellow", "Snow", "2026-09-23", "2026-09-24")
        store.add_warning(conn, "Oslo", "orange", "Heavy rain", "2026-09-24", "2026-09-24")
        assert [tuple(row) for row in store.active_warnings(conn, "2026-09-24")] == [
            ("Kiruna", "yellow", "Snow", "2026-09-23", "2026-09-24"),
            ("Oslo", "orange", "Heavy rain", "2026-09-24", "2026-09-24"),
        ]
        assert [row["name"] for row in store.active_warnings(conn, "2026-09-23")] == ["Kiruna"]
        assert store.active_warnings(conn, "2026-09-25") == []

    @pytest.mark.parametrize(
        ("level", "message", "starts_on", "ends_on"),
        [
            ("purple", "Wind", "2026-09-23", "2026-09-23"),
            ("red", "Wind", "2026-09-24", "2026-09-23"),
            ("red", "  ", "2026-09-23", "2026-09-23"),
            ("red", "Wind", "23/9/2026", "2026-09-23"),
        ],
    )
    def test_schema_rejects_invalid_warnings(self, conn, level, message, starts_on, ends_on):
        with pytest.raises(sqlite3.IntegrityError):
            store.add_warning(conn, "Oslo", level, message, starts_on, ends_on)
        assert count(conn, "warnings") == 0

    def test_unknown_city(self, conn):
        with pytest.raises(ValueError, match="unknown city"):
            store.add_warning(conn, "Atlantis", "red", "Flood", "2026-09-23", "2026-09-23")

    def test_injection_in_the_date_is_just_a_date_that_matches_nothing(self, conn):
        store.add_warning(conn, "Oslo", "red", "Storm", "2026-09-23", "2026-09-23")
        assert store.active_warnings(conn, "' OR '1'='1") == []


class TestInjection:
    INJECTION = "' OR '1'='1"

    def test_an_f_string_query_returns_every_observation(self, conn):
        # Uppgift 5: den sårbara versionen finns bara här i testet, som bevis.
        def unsafe_city_observations(conn, city):
            return conn.execute(
                "SELECT o.observed_on FROM observations AS o "
                f"JOIN cities AS c ON c.id = o.city_id WHERE c.name = '{city}'"
            ).fetchall()

        store.import_observations(conn, [observation(), observation(city="Oslo")])
        assert len(unsafe_city_observations(conn, self.INJECTION)) == 2

    def test_the_real_function_treats_it_as_a_name(self, conn):
        store.import_observations(conn, [observation(), observation(city="Oslo")])
        assert store.city_observations(conn, self.INJECTION) == []


class TestCli:
    def test_rename_city(self, tmp_path, capsys):
        db = tmp_path / "weather.db"
        facit_cli.main([str(db), "init"])
        facit_cli.main([str(db), "rename-city", "Visby", "Gotland"])
        assert "Renamed Visby to Gotland." in capsys.readouterr().out
        facit_cli.main([str(db), "show", "Gotland"])
        assert "2026-09-21" in capsys.readouterr().out

    def test_rename_to_a_taken_name_explains_why(self, tmp_path):
        db = tmp_path / "weather.db"
        facit_cli.main([str(db), "init"])
        with pytest.raises(SystemExit) as exit_info:
            facit_cli.main([str(db), "rename-city", "Visby", "Oslo"])
        assert str(exit_info.value) == "cannot rename: there is already a city called 'Oslo'"

    def test_delete_city_with_observations_explains_why(self, tmp_path):
        db = tmp_path / "weather.db"
        facit_cli.main([str(db), "init"])
        with pytest.raises(SystemExit) as exit_info:
            facit_cli.main([str(db), "delete-city", "Kiruna"])
        assert str(exit_info.value).startswith("cannot delete: Kiruna still has 7 observation(s)")

    def test_delete_city_without_observations(self, tmp_path, capsys):
        db = tmp_path / "weather.db"
        facit_cli.main([str(db), "init"])
        facit_cli.main([str(db), "delete-city", "Copenhagen"])
        assert "Deleted Copenhagen." in capsys.readouterr().out
