"""Each bundled query, run against the bundled data, checked row for row.

The expected numbers were cross-checked against a plain-Python
recomputation of the same data, not just copied from SQLite's output.
"""

import pytest

from analytics.runner import load_query, open_database, run_query


def run(name: str) -> tuple[list[str], list[tuple]]:
    return run_query(open_database(), load_query(name))


def by_city(rows: list[tuple]) -> dict:
    return {row[0]: row[1:] for row in rows}


class TestCommonTableExpressions:
    def test_q01_totals_per_store_highest_first(self):
        _, rows = run("q01_revenue_per_store")
        assert rows == [
            ("Stockholm", 90, 33400.8),
            ("Gothenburg", 91, 30200.8),
            ("Oslo", 90, 28911.0),
            ("Malmö", 64, 23598.2),
            ("Kiruna", 83, 20797.4),
            ("Umeå", 63, 15937.6),
            ("Visby", 33, 11697.6),
        ]

    def test_q01_matches_the_raw_table_total(self):
        _, rows = run("q01_revenue_per_store")
        _, total = run_query(open_database(), "SELECT ROUND(SUM(revenue_sek), 2) FROM daily_sales")
        assert round(sum(revenue for _, _, revenue in rows), 2) == total[0][0]


class TestRankingAndShares:
    def test_q02_keeps_one_row_per_store_with_rank_and_share(self):
        _, rows = run("q02_store_rank_and_share")
        assert [(city, rank) for city, _, rank, _ in rows] == [
            ("Stockholm", 1), ("Gothenburg", 2), ("Oslo", 3), ("Malmö", 4),
            ("Kiruna", 5), ("Umeå", 6), ("Visby", 7),
        ]
        assert rows[0][3] == 20.3

    def test_q02_shares_add_up_to_100_percent(self):
        _, rows = run("q02_store_rank_and_share")
        assert sum(share for *_, share in rows) == pytest.approx(100, abs=0.2)

    def test_q03_one_top_product_per_store(self):
        _, rows = run("q03_best_product_per_store")
        assert rows == [
            ("Gothenburg", "Rain jacket", 15283.0),
            ("Kiruna", "Thermos", 8928.0),
            ("Malmö", "Rain jacket", 12586.0),
            ("Oslo", "Rain jacket", 11687.0),
            ("Stockholm", "Rain jacket", 16182.0),
            ("Umeå", "Umbrella", 5253.6),
            ("Visby", "Rain jacket", 5394.0),
        ]


class TestRowToRowCalculations:
    def test_q04_running_total_ends_at_the_week_total(self):
        _, rows = run("q04_running_revenue")
        assert [row[0] for row in rows] == [f"2026-09-2{day}" for day in range(1, 8)]
        assert rows[0][1] == rows[0][2]  # first day: running total is just that day
        assert rows[-1][2] == 33400.8  # Stockholm's week total from q01

    def test_q04_each_running_total_adds_that_days_revenue(self):
        _, rows = run("q04_running_revenue")
        for previous, current in zip(rows, rows[1:]):
            assert current[2] == pytest.approx(previous[2] + current[1])

    def test_q05_first_day_has_no_previous_day(self):
        _, rows = run("q05_day_over_day_change")
        first_days = [row for row in rows if row[1] == "2026-09-21"]
        assert len(first_days) == 7
        assert all(change is None for *_, change in first_days)

    def test_q05_change_is_relative_to_the_same_store_only(self):
        _, rows = run("q05_day_over_day_change")
        assert ("Gothenburg", "2026-09-22", 6531.0, 4488.0) in rows
        assert ("Kiruna", "2026-09-21", 1911.0, None) in rows  # not compared with Gothenburg's last day

    def test_q06_moving_average_uses_at_most_three_days(self):
        _, rows = run("q06_three_day_average_high")
        kiruna = [row for row in rows if row[0] == "Kiruna"]
        assert kiruna[0][3] == 7.8  # one day available
        assert kiruna[1][3] == 6.9  # (7.8 + 6.1) / 2
        assert kiruna[3][3] == 4.0  # (6.1 + 3.2 + 2.7) / 3, the 21st has left the window


class TestAnalysisAcrossTables:
    def test_q07_umbrellas_sell_five_times_better_in_rain(self):
        _, rows = run("q07_umbrellas_on_rainy_days")
        assert rows == [("rain", 16, 11.0), ("no rain", 33, 2.15)]

    def test_q07_counts_every_store_day_including_zero_sales(self):
        # 7 stores x 7 days; an inner join would silently drop the zero days.
        _, rows = run("q07_umbrellas_on_rainy_days")
        assert sum(days for _, days, _ in rows) == 49

    def test_joining_before_aggregating_double_counts(self):
        # The fan-out trap q07 avoids: after joining to daily_sales, each
        # day's weather row repeats once per product sold that day.
        _, rows = run_query(
            open_database(),
            """
            SELECT ROUND(SUM(o.precipitation_mm), 1)
            FROM observations AS o
            JOIN stores AS s ON s.city_id = o.city_id
            JOIN daily_sales AS ds ON ds.store_id = s.id AND ds.sold_on = o.observed_on
            """,
        )
        assert rows[0][0] > 120.3  # the true total from Week 20

    def test_q08_window_values_filtered_in_outer_query(self):
        _, rows = run("q08_days_above_store_average")
        assert len(rows) == 20
        assert all(revenue > average for _, _, revenue, average in rows)
        assert [day for city, day, *_ in rows if city == "Visby"] == ["2026-09-23", "2026-09-24"]

    def test_q09_categories_add_up_to_store_totals(self):
        _, pivot = run("q09_revenue_by_category")
        _, totals = run("q01_revenue_per_store")
        for city, (_, revenue) in by_city(totals).items():
            assert sum(by_city(pivot)[city]) == pytest.approx(revenue)

    def test_q09_zero_for_a_category_never_sold(self):
        _, rows = run("q09_revenue_by_category")
        assert by_city(rows)["Malmö"] == (20108.2, 0.0, 3490.0)

    def test_q10_lists_missing_store_product_pairs(self):
        _, rows = run("q10_products_never_sold")
        assert rows == [
            ("Gothenburg", "Thermos"),
            ("Malmö", "Thermos"),
            ("Malmö", "Wool socks"),
            ("Oslo", "Thermos"),
            ("Stockholm", "Thermos"),
            ("Visby", "Thermos"),
            ("Visby", "Wool socks"),
        ]
