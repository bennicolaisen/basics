"""Facit för Try It Yourself, kontrollerat mot veckans data. Se FACIT.md."""

import sqlite3

import pytest

from facit.kor import FACIT_DIR, run_file
from joins.runner import open_database


def run(prefix: str) -> tuple[list[str], list[tuple]]:
    matches = sorted(FACIT_DIR.glob(f"{prefix}_*.sql"))
    assert len(matches) == 1, f"expected one facit file for {prefix}, found {matches}"
    return run_file(matches[0])


def test_u1_counts_cities_and_observations_per_country():
    columns, rows = run("u1")
    assert columns == ["country", "cities", "observations"]
    assert rows == [("Denmark", 1, 0), ("Norway", 1, 7), ("Sweden", 6, 42)]


def test_u1_plain_count_would_give_42_swedish_cities():
    conn = open_database()
    wrong = conn.execute(
        "SELECT COUNT(c.id) FROM cities c LEFT JOIN observations o ON o.city_id = c.id"
        " WHERE c.country = 'Sweden'"
    ).fetchone()[0]
    assert wrong == 42


def test_u2_snow_days_with_zero_for_everyone_else():
    _, rows = run("u2")
    assert dict(rows) == {
        "Copenhagen": 0,
        "Gothenburg": 0,
        "Kiruna": 2,
        "Malmö": 0,
        "Oslo": 0,
        "Stockholm": 0,
        "Umeå": 0,
        "Visby": 0,
    }


def test_u3_condition_in_on_keeps_every_city():
    _, rows = run("u3a")
    assert len(rows) == 9
    assert sorted(row for row in rows if row[1] is not None) == [
        ("Kiruna", "2026-09-23"),
        ("Kiruna", "2026-09-24"),
    ]
    assert {row[0] for row in rows} == {
        "Copenhagen", "Gothenburg", "Kiruna", "Malmö", "Oslo", "Stockholm", "Umeå", "Visby",
    }


def test_u3_condition_in_where_drops_the_null_rows():
    _, rows = run("u3b")
    assert sorted(rows) == [("Kiruna", "2026-09-23"), ("Kiruna", "2026-09-24")]


def test_u4_two_days_were_at_least_two_degrees_warmer():
    columns, rows = run("u4")
    assert columns == ["name", "observed_on", "high_day_before_c", "high_c", "rise_c"]
    assert rows == [
        ("Kiruna", "2026-09-25", 2.7, 5.4, 2.7),
        ("Stockholm", "2026-09-26", 14.6, 17.4, 2.8),
    ]


def test_u4_first_day_has_no_day_before():
    conn = open_database()
    previous = conn.execute("SELECT date('2026-09-21', '-1 day')").fetchone()[0]
    assert previous == "2026-09-20"
    count = conn.execute(
        "SELECT COUNT(*) FROM observations WHERE observed_on = ?", (previous,)
    ).fetchone()[0]
    assert count == 0


def test_u5_active_warnings_on_the_23rd():
    _, rows = run("u5")
    assert rows == [
        ("Gothenburg", "orange", "Heavy rain, risk of flooding"),
        ("Kiruna", "yellow", "Snow and slippery roads"),
        ("Visby", "yellow", "Strong wind"),
    ]


def test_u5_schema_rejects_bad_warnings():
    conn = open_database()
    sql = (FACIT_DIR / "u5_active_warnings.sql").read_text(encoding="utf-8")
    create = sql[sql.index("CREATE TABLE") : sql.index(";", sql.index("CREATE TABLE")) + 1]
    conn.execute(create)
    insert = (
        "INSERT INTO warnings (city_id, level, message, starts_on, ends_on)"
        " VALUES (?, ?, 'x', ?, ?)"
    )
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(insert, (1, "purple", "2026-09-23", "2026-09-23"))
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(insert, (1, "red", "2026-09-24", "2026-09-23"))
    conn.execute(insert, (1, "red", "2026-09-23", "2026-09-23"))
