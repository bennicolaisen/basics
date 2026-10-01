"""Each bundled query, run against the bundled data, checked row for row.

Queries without ORDER BY promise no particular row order, so their
results are compared sorted; queries with ORDER BY are compared exactly,
because the order *is* part of their answer.
"""

from select_basics.runner import load_query, open_database, run_query


def run(name: str) -> tuple[list[str], list[tuple]]:
    return run_query(open_database(), load_query(name))


class TestChoosingColumns:
    def test_q01_returns_every_column_of_every_city(self):
        columns, rows = run("q01_all_cities")
        assert columns == ["id", "name", "country", "population"]
        assert len(rows) == 8
        assert (1, "Stockholm", "Sweden", 984748) in rows

    def test_q02_returns_only_name_and_country(self):
        columns, rows = run("q02_city_names_and_countries")
        assert columns == ["name", "country"]
        assert ("Copenhagen", "Denmark") in rows
        assert len(rows) == 8

    def test_q03_names_the_computed_column(self):
        columns, _ = run("q03_daily_temperature_range")
        assert columns == ["observed_on", "city_id", "range_c"]

    def test_q03_rounds_away_floating_point_noise(self):
        # 16.2 - 9.1 is 7.099999999999999 in floating point; ROUND fixes the display.
        _, rows = run("q03_daily_temperature_range")
        assert ("2026-09-21", 1, 7.1) in rows
        assert len(rows) == 49


class TestFiltering:
    def test_q04_keeps_only_days_above_5_mm(self):
        _, rows = run("q04_wet_days")
        ids = sorted(row[0] for row in rows)
        assert ids == [3, 9, 10, 17, 18, 21, 39, 45, 46]

    def test_q04_returns_whole_rows(self):
        columns, rows = run("q04_wet_days")
        assert len(columns) == 8
        assert all(row[columns.index("precipitation_mm")] > 5 for row in rows)

    def test_q05_requires_both_conditions(self):
        _, rows = run("q05_sunny_and_warm")
        assert sorted(rows) == [
            ("2026-09-21", 1, 16.2),
            ("2026-09-21", 3, 17.3),
            ("2026-09-21", 6, 15.6),
            ("2026-09-26", 1, 17.4),
            ("2026-09-26", 2, 16.4),
            ("2026-09-26", 3, 17.9),
            ("2026-09-26", 6, 16.1),
        ]

    def test_q06_accepts_either_condition(self):
        _, rows = run("q06_frost_or_strong_wind")
        assert len(rows) == 12
        assert all(temp_min < 0 or (wind is not None and wind > 10) for _, _, temp_min, wind in rows)

    def test_q06_keeps_frost_day_whose_wind_is_null(self):
        # Kiruna 2026-09-24: `wind_ms > 10` is NULL (unknown), but
        # `TRUE OR NULL` is TRUE, so the frost alone is enough.
        _, rows = run("q06_frost_or_strong_wind")
        assert ("2026-09-24", 5, -3.8, None) in rows

    def test_q07_finds_both_missing_readings(self):
        _, rows = run("q07_missing_wind_readings")
        assert sorted(rows) == [(23, 4, "2026-09-22"), (32, 5, "2026-09-24")]

    def test_equals_null_matches_nothing(self):
        # The mistake Q07 avoids: NULL = NULL is NULL, never TRUE.
        _, rows = run_query(open_database(), "SELECT id FROM observations WHERE wind_ms = NULL")
        assert rows == []

    def test_q08_matches_any_listed_name(self):
        _, rows = run("q08_capital_cities")
        assert sorted(name for name, _, _ in rows) == ["Copenhagen", "Oslo", "Stockholm"]

    def test_q09_between_includes_both_ends(self):
        _, rows = run("q09_midweek_in_stockholm")
        assert [row[0] for row in rows] == ["2026-09-23", "2026-09-24", "2026-09-25"]


class TestSortingAndLimiting:
    def test_q10_is_warmest_first_and_stops_at_three(self):
        _, rows = run("q10_three_warmest_days")
        assert rows == [
            ("2026-09-26", 3, 17.9),
            ("2026-09-26", 1, 17.4),
            ("2026-09-21", 3, 17.3),
        ]

    def test_q11_lists_each_condition_once_alphabetically(self):
        _, rows = run("q11_distinct_conditions")
        assert rows == [("cloud",), ("rain",), ("snow",), ("sun",)]

