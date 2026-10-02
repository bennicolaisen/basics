"""Facit för Try It Yourself, kontrollerat mot veckans data. Se FACIT.md."""

from analytics.runner import open_database, run_query
from facit.kor import FACIT_DIR, run_file


def run(prefix: str) -> tuple[list[str], list[tuple]]:
    matches = sorted(FACIT_DIR.glob(f"{prefix}_*.sql"))
    assert len(matches) == 1, f"expected one facit file for {prefix}, found {matches}"
    return run_file(matches[0])


def test_u1_top_two_stores_per_product():
    columns, rows = run("u1")
    assert columns == ["product", "city", "units", "units_rank"]
    assert rows == [
        ("Umbrella", "Gothenburg", 61, 1),
        ("Umbrella", "Oslo", 47, 2),
        ("Rain jacket", "Stockholm", 18, 1),
        ("Rain jacket", "Gothenburg", 17, 2),
        ("Wool socks", "Kiruna", 32, 1),
        ("Wool socks", "Umeå", 19, 2),
        ("Thermos", "Kiruna", 32, 1),
        ("Thermos", "Umeå", 4, 2),
        ("Sunglasses", "Stockholm", 23, 1),
        ("Sunglasses", "Oslo", 18, 2),
    ]


def test_u1_the_only_tie_is_further_down_the_rain_jacket_list():
    sql = (FACIT_DIR / "u1_top_two_stores_per_product.sql").read_text(encoding="utf-8")
    everyone = sql.replace("WHERE r.units_rank <= 2\n", "")
    assert everyone != sql
    _, rows = run_query(open_database(), everyone)
    ranks = [(product, rank) for product, _, _, rank in rows]
    ties = sorted((product, city, units) for product, city, units, rank in rows
                  if ranks.count((product, rank)) > 1)
    assert ties == [("Rain jacket", "Kiruna", 4), ("Rain jacket", "Umeå", 4)]


def test_u2_two_rises_in_a_row():
    _, rows = run("u2")
    assert [(city, day) for city, day, *_ in rows] == [
        ("Gothenburg", "2026-09-23"),
        ("Gothenburg", "2026-09-27"),
        ("Kiruna", "2026-09-23"),
        ("Malmö", "2026-09-24"),
        ("Malmö", "2026-09-27"),
        ("Oslo", "2026-09-23"),
        ("Umeå", "2026-09-24"),
        ("Visby", "2026-09-24"),
    ]
    assert all(before_2 < before_1 < today for _, _, before_2, before_1, today in rows)


def test_u2_every_store_sold_something_every_day():
    # LAG läser föregående RAD. Det är föregående DAG bara om ingen dag saknas.
    count = open_database().execute(
        "SELECT COUNT(*) FROM (SELECT DISTINCT store_id, sold_on FROM daily_sales)"
    ).fetchone()[0]
    assert count == 7 * 7


def test_u3_per_inhabitant_ranking_turns_the_total_ranking_around():
    columns, rows = run("u3")
    assert columns[-2:] == ["per_inhabitant_rank", "total_revenue_rank"]
    assert [(city, per_inhabitant, total) for city, _, _, _, per_inhabitant, total in rows] == [
        ("Kiruna", 1, 5),
        ("Visby", 2, 7),
        ("Umeå", 3, 6),
        ("Malmö", 4, 4),
        ("Gothenburg", 5, 2),
        ("Oslo", 6, 3),
        ("Stockholm", 7, 1),
    ]
    assert rows[0][3] == 927.5


def test_u4_sunday_against_comparable_days():
    columns, rows = run("u4")
    assert columns == [
        "city",
        "sunday_weather",
        "sunday_units",
        "other_days_avg_units",
        "same_weather_days_avg_units",
        "same_weather_days",
    ]
    assert rows == [
        ("Gothenburg", "rain", 9, 8.67, 14.0, 3),
        ("Kiruna", "cloud", 2, 1.5, 1.5, 2),
        ("Malmö", "rain", 11, 4.83, 11.0, 2),
        ("Oslo", "cloud", 5, 7.0, None, 0),
        ("Stockholm", "cloud", 4, 6.17, 5.0, 1),
        ("Umeå", "cloud", 3, 4.0, 4.0, 1),
        ("Visby", "cloud", 3, 2.83, 1.0, 1),
    ]


def test_u4_sunday_umbrellas_were_sold_at_20_percent_off():
    prices = open_database().execute(
        """
        SELECT DISTINCT ROUND(ds.revenue_sek / ds.units, 2)
        FROM daily_sales ds JOIN products p ON p.id = ds.product_id
        WHERE p.name = 'Umbrella' AND ds.sold_on = '2026-09-27'
        """
    ).fetchall()
    assert prices == [(159.2,)]


def test_u5_matches_the_week_20_precipitation():
    _, rows = run("u5")
    simple = dict(
        open_database().execute(
            """
            SELECT c.name, ROUND(SUM(o.precipitation_mm), 1)
            FROM observations o JOIN cities c ON c.id = o.city_id
            GROUP BY c.name
            """
        ).fetchall()
    )
    assert len(rows) == 7
    assert {city: mm for city, mm, _ in rows} == simple
    assert dict((city, revenue) for city, _, revenue in rows)["Gothenburg"] == 27063.8


def test_u5b_joining_before_summing_inflates_both_columns():
    _, right = run("u5")
    _, wrong = run("u5b")
    for (city, mm, revenue), (wrong_city, wrong_mm, wrong_revenue) in zip(right, wrong):
        assert city == wrong_city
        assert wrong_mm > mm
        assert wrong_revenue > revenue
