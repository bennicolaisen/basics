"""Open-Meteo is tested offline, with a response in the shape the real API returns."""

from urllib.parse import parse_qs, urlsplit

from api_client.open_meteo import DailyForecast, forecast_url, parse_daily

SAMPLE_RESPONSE = {
    "latitude": 67.86,
    "longitude": 20.23,
    "timezone": "Europe/Stockholm",
    "daily_units": {
        "time": "iso8601",
        "temperature_2m_max": "°C",
        "temperature_2m_min": "°C",
        "precipitation_sum": "mm",
    },
    "daily": {
        "time": ["2026-10-01", "2026-10-02", "2026-10-03"],
        "temperature_2m_max": [4.1, 2.8, 5.0],
        "temperature_2m_min": [-1.2, -3.4, 0.3],
        "precipitation_sum": [0.0, 1.6, 0.4],
    },
}


def test_url_asks_for_the_daily_variables_we_parse():
    query = parse_qs(urlsplit(forecast_url(67.86, 20.23)).query)
    assert query["latitude"] == ["67.86"]
    assert query["longitude"] == ["20.23"]
    assert query["daily"] == ["temperature_2m_max,temperature_2m_min,precipitation_sum"]
    assert query["forecast_days"] == ["3"]


def test_url_uses_https():
    assert forecast_url(0, 0).startswith("https://api.open-meteo.com/v1/forecast?")


def test_parse_daily_turns_columns_into_one_record_per_day():
    assert parse_daily(SAMPLE_RESPONSE) == [
        DailyForecast("2026-10-01", 4.1, -1.2, 0.0),
        DailyForecast("2026-10-02", 2.8, -3.4, 1.6),
        DailyForecast("2026-10-03", 5.0, 0.3, 0.4),
    ]


def test_parse_daily_ignores_extra_fields():
    payload = {**SAMPLE_RESPONSE, "elevation": 452.0, "generationtime_ms": 0.1}
    assert len(parse_daily(payload)) == 3
