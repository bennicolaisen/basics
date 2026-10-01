"""Each bundled query, run against the bundled data, checked row for row.

Every multi-row query here has an ORDER BY, so results are compared in
order: the ordering is part of each answer.
"""

from aggregates.runner import load_query, open_database, run_query


def run(name: str) -> tuple[list[str], list[tuple]]:
    return run_query(open_database(), load_query(name))


class TestWholeTableAggregates:
    def test_q01_count_star_counts_rows_but_count_column_skips_null(self):
        columns, rows = run("q01_count_observations")
        assert columns == ["observations", "wind_readings"]
        assert rows == [(49, 47)]

    def test_q02_returns_a_single_summary_row(self):
        _, rows = run("q02_week_extremes")
        assert rows == [(-4.1, 17.9, 12.8)]

    def test_q03_sums_every_observation(self):
        _, rows = run("q03_total_precipitation")
        assert rows == [(120.3,)]

    def test_aggregates_over_zero_rows(self):
        # COUNT of nothing is 0, but SUM/AVG/MAX of nothing is NULL, not 0.
        _, rows = run_query(
            open_database(),
            "SELECT COUNT(*), SUM(precipitation_mm), MAX(temp_max_c) FROM observations WHERE city_id = 8",
        )
        assert rows == [(0, None, None)]


class TestGroupBy:
    def test_q04_one_row_per_condition_most_common_first(self):
        _, rows = run("q04_days_per_condition")
        assert rows == [("sun", 17), ("rain", 16), ("cloud", 14), ("snow", 2)]

    def test_q04_group_counts_add_up_to_all_rows(self):
        _, rows = run("q04_days_per_condition")
        assert sum(days for _, days in rows) == 49

    def test_q05_totals_per_city_wettest_first(self):
        _, rows = run("q05_precipitation_per_city")
        assert rows == [(2, 31.4), (3, 21.7), (7, 21.5), (6, 12.4), (4, 11.9), (1, 11.1), (5, 10.3)]

    def test_q05_leaves_out_city_with_no_rows(self):
        # Copenhagen (8) has no observations, so no group exists for it.
        _, rows = run("q05_precipitation_per_city")
        assert 8 not in [city_id for city_id, _ in rows]

    def test_q09_groups_text_values(self):
        _, rows = run("q09_population_per_country")
        assert rows == [("Sweden", 6, 2130485), ("Norway", 1, 717710), ("Denmark", 1, 660842)]

    def test_q10_one_row_per_city_and_condition_pair(self):
        _, rows = run("q10_conditions_per_city")
        assert len(rows) == 21
        assert rows[:3] == [(1, "cloud", 2), (1, "rain", 2), (1, "sun", 3)]
        assert (5, "snow", 2) in rows
        assert (5, "rain", 0) not in rows  # a pair that never occurs gets no row at all


class TestWhereAndHaving:
    def test_q06_having_keeps_only_groups_over_20_mm(self):
        _, rows = run("q06_wet_cities")
        assert rows == [(2, 31.4), (3, 21.7), (7, 21.5)]

    def test_q07_where_filters_rows_then_having_filters_groups(self):
        _, rows = run("q07_cities_with_three_rainy_days")
        assert rows == [(2, 4), (3, 3), (7, 3)]


class TestNullAndConditionalAggregates:
    def test_q08_average_skips_missing_readings(self):
        _, rows = run("q08_average_wind_per_city")
        kiruna = next(row for row in rows if row[0] == 5)
        # 22.5 m/s over 6 known readings, not over 7 days (which would be 3.21).
        assert kiruna == (5, 7, 6, 3.75)

    def test_q08_windiest_first(self):
        _, rows = run("q08_average_wind_per_city")
        assert [row[0] for row in rows] == [6, 2, 3, 1, 7, 4, 5]

    def test_q11_counts_matching_rows_and_keeps_zero_groups(self):
        _, rows = run("q11_frost_nights_per_city")
        assert rows == [(5, 6), (4, 1), (1, 0), (2, 0), (3, 0), (6, 0), (7, 0)]
