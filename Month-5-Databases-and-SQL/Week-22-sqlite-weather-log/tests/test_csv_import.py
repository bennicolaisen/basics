import sqlite3

import pytest

from weather_log import store
from weather_log.cli import DATA_DIR
from weather_log.csv_import import read_cities, read_observations

HEADER = "city,observed_on,temp_max_c,temp_min_c,precipitation_mm,wind_ms,conditions\n"


def write_csv(tmp_path, body: str):
    path = tmp_path / "observations.csv"
    path.write_text(HEADER + body, encoding="utf-8")
    return path


class TestReadObservations:
    def test_converts_numbers_and_keeps_text(self, tmp_path):
        path = write_csv(tmp_path, "Umeå,2026-09-21,12.4,4.1,0.0,3.1,sun\n")
        (obs,) = read_observations(path)
        assert obs.city == "Umeå"
        assert obs.temp_min_c == 4.1
        assert obs.conditions == "sun"

    def test_empty_wind_field_means_missing(self, tmp_path):
        path = write_csv(tmp_path, "Umeå,2026-09-22,11.2,5.3,2.4,,cloud\n")
        assert read_observations(path)[0].wind_ms is None

    def test_non_numeric_value_names_the_line_and_field(self, tmp_path):
        path = write_csv(tmp_path, "Umeå,2026-09-21,12.4,4.1,0.0,3.1,sun\nUmeå,2026-09-22,warm,5.3,2.4,,cloud\n")
        with pytest.raises(ValueError, match="line 3: temp_max_c"):
            read_observations(path)


class TestBundledData:
    def test_sample_week_matches_weeks_19_to_21(self):
        observations = read_observations(DATA_DIR / "sample_week.csv")
        assert len(observations) == 49
        assert sum(obs.wind_ms is None for obs in observations) == 2

    def test_cities(self):
        cities = read_cities(DATA_DIR / "cities.csv")
        assert len(cities) == 8
        assert cities[0] == ("Stockholm", "Sweden", 984748)

    def test_file_with_error_imports_nothing_and_fixed_file_imports_all(self):
        conn = store.open_log()
        for name, country, population in read_cities(DATA_DIR / "cities.csv"):
            store.add_city(conn, name, country, population)
        with pytest.raises(sqlite3.IntegrityError, match="CHECK"):
            store.import_observations(conn, read_observations(DATA_DIR / "2026-09-29-with-error.csv"))
        assert store.import_observations(conn, read_observations(DATA_DIR / "2026-09-28.csv")) == 8
        assert conn.execute("SELECT COUNT(*) FROM observations").fetchone()[0] == 8
