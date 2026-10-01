import pytest

from aggregates.runner import format_table, load_query, open_database, query_names, run_query


class TestOpenDatabase:
    def test_loads_both_tables(self):
        conn = open_database()
        assert conn.execute("SELECT COUNT(*) FROM cities").fetchone() == (8,)
        assert conn.execute("SELECT COUNT(*) FROM observations").fetchone() == (49,)

    def test_each_call_starts_from_the_original_data(self):
        open_database().execute("DELETE FROM cities")
        assert open_database().execute("SELECT COUNT(*) FROM cities").fetchone() == (8,)


class TestLoadQuery:
    def test_reads_the_named_file(self):
        assert "FROM observations" in load_query("q01_count_observations")

    def test_unknown_name_lists_the_valid_ones(self):
        with pytest.raises(ValueError, match="q01_count_observations"):
            load_query("q99_does_not_exist")

    def test_query_names_are_sorted_file_stems(self):
        names = query_names()
        assert names[0] == "q01_count_observations"
        assert names == sorted(names)


class TestRunQuery:
    def test_returns_column_names_and_rows(self):
        columns, rows = run_query(open_database(), "SELECT name FROM cities WHERE id = 7")
        assert columns == ["name"]
        assert rows == [("Oslo",)]

    def test_statement_without_rows_returns_empty_result(self):
        assert run_query(open_database(), "UPDATE cities SET population = 0") == ([], [])


class TestFormatTable:
    def test_pads_columns_to_widest_value(self):
        table = format_table(["name", "n"], [("Oslo", 1), ("Stockholm", 22)])
        assert table.splitlines() == [
            "name       n",
            "---------  --",
            "Oslo       1",
            "Stockholm  22",
            "(2 rows)",
        ]

    def test_shows_null_for_none(self):
        assert "NULL" in format_table(["wind_ms"], [(None,)])

    def test_singular_row_count(self):
        assert format_table(["x"], [(1,)]).endswith("(1 row)")

    def test_empty_result_still_shows_header(self):
        assert format_table(["name"], []).splitlines() == ["name", "----", "(0 rows)"]
