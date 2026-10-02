"""Facit för Try It Yourself, kontrollerat mot veckans data. Se FACIT.md."""

from pathlib import Path

from aggregates.runner import open_database, run_query

FACIT_DIR = Path(__file__).parent.parent / "facit"


def run(prefix: str) -> tuple[list[str], list[tuple]]:
    matches = sorted(FACIT_DIR.glob(f"{prefix}_*.sql"))
    assert len(matches) == 1, f"expected one facit file for {prefix}, found {matches}"
    return run_query(open_database(), matches[0].read_text(encoding="utf-8"))


def test_u1_average_high_and_count_per_day():
    columns, rows = run("u1")
    assert columns == ["observed_on", "avg_high_c", "cities_reporting"]
    assert rows == [
        ("2026-09-21", 14.3, 7),
        ("2026-09-22", 13.2, 7),
        ("2026-09-23", 11.7, 7),
        ("2026-09-24", 11.1, 7),
        ("2026-09-25", 12.7, 7),
        ("2026-09-26", 14.4, 7),
        ("2026-09-27", 12.4, 7),
    ]


def test_u1b_coldest_day_is_the_24th():
    _, rows = run("u1b")
    assert rows == [("2026-09-24", 11.1)]


def test_u2_dry_and_wet_days_add_up_to_seven():
    columns, rows = run("u2")
    assert columns == ["city_id", "dry_days", "wet_days"]
    assert rows == [(1, 3, 4), (2, 1, 6), (3, 2, 5), (4, 3, 4), (5, 2, 5), (6, 3, 4), (7, 3, 4)]
    assert all(dry + wet == 7 for _, dry, wet in rows)


def test_u3_having_finds_the_mild_cities():
    _, rows = run("u3")
    assert rows == [(2, 13.5), (3, 14.7), (6, 13.6)]


def test_u3b_where_wrongly_adds_stockholm_and_oslo():
    _, rows = run("u3b")
    assert [row[0] for row in rows] == [1, 2, 3, 6, 7]


def test_u4_every_city_had_three_kinds():
    _, rows = run("u4")
    assert rows == [(city_id, 3) for city_id in range(1, 8)]


def test_u4_the_having_filter_really_filters():
    sql = (FACIT_DIR / "u4_kinds_of_weather.sql").read_text(encoding="utf-8")
    stricter = sql.replace(">= 3", ">= 4")
    assert stricter != sql
    assert run_query(open_database(), stricter)[1] == []


def test_u5_the_averages_differ_only_where_readings_are_missing():
    _, rows = run("u5")
    differing = [(city_id, zero, known) for city_id, zero, known in rows if zero != known]
    assert differing == [(4, 3.4, 3.97), (5, 3.21, 3.75)]
