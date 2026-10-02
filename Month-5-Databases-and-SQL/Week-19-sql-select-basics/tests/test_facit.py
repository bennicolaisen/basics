"""Facit för Try It Yourself, kontrollerat mot veckans data. Se FACIT.md."""

from pathlib import Path

from select_basics.runner import open_database, run_query

FACIT_DIR = Path(__file__).parent.parent / "facit"


def run(prefix: str) -> tuple[list[str], list[tuple]]:
    matches = sorted(FACIT_DIR.glob(f"{prefix}_*.sql"))
    assert len(matches) == 1, f"expected one facit file for {prefix}, found {matches}"
    return run_query(open_database(), matches[0].read_text(encoding="utf-8"))


def test_u1_small_swedish_cities_largest_first():
    columns, rows = run("u1")
    assert columns == ["name", "population"]
    assert rows == [("Umeå", 132235), ("Visby", 24330), ("Kiruna", 22423)]


def test_u2a_rainy_but_mild_in_gothenburg():
    _, rows = run("u2a")
    assert sorted(row[0] for row in rows) == [9, 14]


def test_u2b_parentheses_give_kiruna_but_not_oslo():
    _, rows = run("u2b")
    assert sorted(row[0] for row in rows) == [24, 25, 31, 32]
    city_ids = {row[1] for row in rows}
    assert 5 in city_ids  # Kiruna
    assert 7 not in city_ids  # Oslo


def test_u2c_without_parentheses_lets_every_rainy_day_in():
    _, rows = run("u2c")
    assert len(rows) == 18
    assert 7 in {row[1] for row in rows}  # Oslo kommer med, fast det var över 10 grader
    assert all(row[4] == "rain" or row[3] < 10 for row in rows)


def test_u3a_only_kiruna_ends_in_a():
    # Umeå slutar på å, inte a.
    _, rows = run("u3a")
    assert rows == [("Kiruna",)]


def test_u3b_like_ignores_case_only_for_ascii_letters():
    columns, rows = run("u3b")
    assert columns == ["name", "lower_case_pattern", "upper_case_pattern"]
    assert rows == [("Malmö", 1, 0)]


def test_u4_three_smallest_ranges_with_a_predictable_tie_break():
    columns, rows = run("u4")
    assert columns == ["observed_on", "city_id", "range_c"]
    assert rows == [
        ("2026-09-22", 6, 3.1),
        ("2026-09-23", 6, 3.1),
        ("2026-09-22", 2, 3.3),
    ]


def test_u4_there_really_is_a_tie_for_third_place():
    conn = open_database()
    _, rows = run_query(
        conn,
        "SELECT id FROM observations WHERE ROUND(temp_max_c - temp_min_c, 1) = 3.3",
    )
    assert sorted(row[0] for row in rows) == [9, 39]


def test_u5_calm_weekend_days_with_known_wind():
    _, rows = run("u5")
    assert rows == [
        (27, "2026-09-26", 4, 2.2),
        (34, "2026-09-26", 5, 1.8),
        (48, "2026-09-26", 7, 2.4),
    ]


def test_u5_is_the_same_without_is_not_null():
    _, with_check = run("u5")
    sql = (FACIT_DIR / "u5_calm_weekend.sql").read_text(encoding="utf-8")
    without_check = sql.replace("  AND wind_ms IS NOT NULL\n", "")
    assert without_check != sql
    assert run_query(open_database(), without_check)[1] == with_check


def test_u5_coalesce_would_let_missing_readings_in():
    # Om NULL byts mot 0 räknas en okänd vind som stiltje: då gör det skillnad.
    _, rows = run_query(
        open_database(),
        "SELECT id FROM observations WHERE COALESCE(wind_ms, 0) < 3 ORDER BY id",
    )
    assert {23, 32} <= {row[0] for row in rows}
