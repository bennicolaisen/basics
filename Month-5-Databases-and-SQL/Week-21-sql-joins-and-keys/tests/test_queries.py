"""Each bundled query, run against the bundled data, checked row for row."""

import sqlite3

import pytest

from joins.runner import load_query, open_database, run_query


def run(name: str) -> tuple[list[str], list[tuple]]:
    return run_query(open_database(), load_query(name))


class TestInnerJoin:
    def test_q01_every_observation_gets_its_city_name(self):
        _, rows = run("q01_observations_with_city_names")
        assert len(rows) == 49
        assert rows[0] == ("Gothenburg", "2026-09-21", 15.8, "cloud")
        assert rows[-1] == ("Visby", "2026-09-27", 14.8, "cloud")

    def test_q01_has_no_row_for_a_city_without_observations(self):
        _, rows = run("q01_observations_with_city_names")
        assert "Copenhagen" not in {name for name, *_ in rows}

    def test_q02_filters_on_the_observations_side(self):
        _, rows = run("q02_snow_days")
        assert rows == [
            ("Kiruna", "2026-09-23", 3.2, -2.6),
            ("Kiruna", "2026-09-24", 2.7, -3.8),
        ]

    def test_q03_matches_week_20_totals_but_with_names(self):
        _, rows = run("q03_precipitation_by_city_name")
        assert rows == [
            ("Gothenburg", 31.4),
            ("Malmö", 21.7),
            ("Oslo", 21.5),
            ("Visby", 12.4),
            ("Umeå", 11.9),
            ("Stockholm", 11.1),
            ("Kiruna", 10.3),
        ]

    def test_q04_groups_by_a_column_from_the_other_table(self):
        _, rows = run("q04_precipitation_by_country")
        # Denmark is missing: its only city has no observations to join to.
        assert rows == [("Norway", 7, 3.07), ("Sweden", 42, 2.35)]


class TestLeftJoin:
    def test_q05_finds_the_city_with_no_matches(self):
        _, rows = run("q05_cities_without_observations")
        assert rows == [("Copenhagen",)]

    def test_q06_includes_zero_for_the_unmatched_city(self):
        _, rows = run("q06_observation_count_per_city")
        assert len(rows) == 8
        assert rows[-1] == ("Copenhagen", 0)
        assert all(count == 7 for _, count in rows[:-1])

    def test_count_star_would_count_the_null_padded_row(self):
        # The mistake q06 avoids: after a LEFT JOIN, Copenhagen still has
        # one (all-NULL) row on the observations side, and COUNT(*) counts it.
        _, rows = run_query(
            open_database(),
            """
            SELECT COUNT(*) FROM cities AS c
            LEFT JOIN observations AS o ON o.city_id = c.id
            WHERE c.name = 'Copenhagen'
            """,
        )
        assert rows == [(1,)]

    def test_inner_join_would_drop_the_unmatched_city(self):
        inner = load_query("q06_observation_count_per_city").replace("LEFT JOIN", "JOIN")
        _, rows = run_query(open_database(), inner)
        assert "Copenhagen" not in {name for name, _ in rows}


class TestSubqueriesAndSelfJoins:
    def test_q07_one_warmest_day_per_city(self):
        _, rows = run("q07_warmest_day_per_city")
        assert rows == [
            ("Malmö", "2026-09-26", 17.9),
            ("Stockholm", "2026-09-26", 17.4),
            ("Gothenburg", "2026-09-26", 16.4),
            ("Visby", "2026-09-26", 16.1),
            ("Oslo", "2026-09-21", 14.9),
            ("Umeå", "2026-09-21", 12.4),
            ("Kiruna", "2026-09-21", 7.8),
        ]

    def test_q08_compares_each_row_with_stockholm_on_the_same_day(self):
        _, rows = run("q08_warmer_than_stockholm")
        assert len(rows) == 14
        assert all(temp > stockholm for _, _, temp, stockholm in rows)
        assert ("2026-09-26", "Malmö", 17.9, 17.4) in rows

    def test_q08_never_compares_stockholm_with_itself(self):
        _, rows = run("q08_warmer_than_stockholm")
        assert "Stockholm" not in {name for _, name, _, _ in rows}


class TestKeys:
    def test_city_names_are_unique(self):
        with pytest.raises(sqlite3.IntegrityError, match="UNIQUE"):
            open_database().execute("INSERT INTO cities (name, country, population) VALUES ('Oslo', 'Norway', 1)")

    def test_primary_key_is_assigned_automatically(self):
        conn = open_database()
        cursor = conn.execute("INSERT INTO cities (name, country, population) VALUES ('Bergen', 'Norway', 291940)")
        assert cursor.lastrowid == 9
