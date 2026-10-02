"""Tester för facit/ (uppgift 1-5). Se FACIT.md."""

import json
import threading
import urllib.error
import urllib.request
from datetime import date
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlsplit

import pytest

import api_client.client
from api_client.client import ApiError
from facit import cli, open_meteo
from facit.client import FacitWeatherClient, get_json


# Uppgift 1 ---------------------------------------------------------------


def test_warmest_day(base_url):
    client = FacitWeatherClient(base_url)
    assert client.warmest_day("Kiruna")["observed_on"] == "2026-09-21"
    stockholm = client.warmest_day("Stockholm")
    assert (stockholm["observed_on"], stockholm["temp_max_c"]) == ("2026-09-26", 17.4)


def test_warmest_day_makes_exactly_one_request(base_url, monkeypatch):
    urls = []
    real_get_json = api_client.client.get_json

    def counting_get_json(url, *args, **kwargs):
        urls.append(url)
        return real_get_json(url, *args, **kwargs)

    monkeypatch.setattr(api_client.client, "get_json", counting_get_json)
    FacitWeatherClient(base_url).warmest_day("Malmö")
    assert len(urls) == 1


def test_warmest_day_of_unknown_city_is_a_404(base_url):
    with pytest.raises(ApiError) as error_info:
        FacitWeatherClient(base_url).warmest_day("Atlantis")
    assert error_info.value.status == 404


def test_warmest_day_of_city_without_observations(base_url):
    with pytest.raises(ValueError, match="no observations"):
        FacitWeatherClient(base_url).warmest_day("Copenhagen")


# Uppgift 2 ---------------------------------------------------------------


class ScriptedServer:
    """En server som svarar med en förbestämd lista statuskoder, en per förfrågan."""

    def __init__(self, statuses: list[int]):
        self.statuses = list(statuses)
        self.requests = 0
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                outer.requests += 1
                status = outer.statuses.pop(0) if outer.statuses else 200
                body = json.dumps({"ok": True} if status == 200 else {"error": "scripted"}).encode()
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args):
                pass

        self.server = HTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        host, port = self.server.server_address[:2]
        self.url = f"http://{host}:{port}/"

    def close(self):
        self.server.shutdown()
        self.server.server_close()


@pytest.fixture
def scripted():
    servers = []

    def make(statuses):
        server = ScriptedServer(statuses)
        servers.append(server)
        return server

    yield make
    for server in servers:
        server.close()


def test_5xx_is_retried_until_it_works(scripted):
    server = scripted([503, 500])
    waits = []
    assert get_json(server.url, retries=2, sleep=waits.append) == {"ok": True}
    assert server.requests == 3
    assert waits == [1.0, 1.0]


def test_5xx_gives_up_after_the_last_retry(scripted):
    server = scripted([503, 503, 503])
    with pytest.raises(ApiError) as error_info:
        get_json(server.url, retries=2, sleep=lambda seconds: None)
    assert error_info.value.status == 503
    assert server.requests == 3


def test_4xx_is_never_retried(scripted):
    server = scripted([404])
    with pytest.raises(ApiError) as error_info:
        get_json(server.url, retries=5, sleep=lambda seconds: None)
    assert error_info.value.status == 404
    assert server.requests == 1


def test_no_retries_by_default(scripted):
    server = scripted([500])
    with pytest.raises(ApiError):
        get_json(server.url, sleep=lambda seconds: None)
    assert server.requests == 1


def test_connection_error_is_retried(closed_port_url):
    waits = []
    with pytest.raises(ConnectionError):
        get_json(closed_port_url, retries=3, retry_delay=0.5, sleep=waits.append)
    assert waits == [0.5, 0.5, 0.5]


def test_negative_retries_is_a_mistake():
    with pytest.raises(ValueError):
        get_json("http://127.0.0.1:1/", retries=-1)


# Uppgift 3 ---------------------------------------------------------------


def sample(wind_unit: str, winds: list) -> dict:
    return {
        "daily_units": {"time": "iso8601", "wind_speed_10m_max": wind_unit},
        "daily": {
            "time": ["2026-10-01", "2026-10-02"],
            "temperature_2m_max": [4.1, 2.8],
            "temperature_2m_min": [-1.2, -3.4],
            "precipitation_sum": [0.0, 1.6],
            "wind_speed_10m_max": winds,
        },
    }


def test_url_asks_for_wind_in_metres_per_second():
    query = parse_qs(urlsplit(open_meteo.forecast_url(67.86, 20.23)).query)
    assert query["daily"] == ["temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max"]
    assert query["wind_speed_unit"] == ["ms"]
    assert "past_days" not in query


def test_wind_in_metres_per_second_is_kept():
    days = open_meteo.parse_daily(sample("m/s", [5.2, 11.0]))
    assert days[0] == open_meteo.DailyForecast("2026-10-01", 4.1, -1.2, 0.0, 5.2)
    assert days[1].wind_max_ms == 11.0


def test_wind_in_kilometres_per_hour_is_converted():
    days = open_meteo.parse_daily(sample("km/h", [36.0, 18.7]))
    assert [day.wind_max_ms for day in days] == [10.0, 5.2]


def test_unknown_wind_unit_is_refused():
    with pytest.raises(ValueError, match="unit"):
        open_meteo.parse_daily(sample("kn", [10.0, 12.0]))


def test_missing_wind_stays_missing():
    assert open_meteo.parse_daily(sample("m/s", [None, 3.0]))[0].wind_max_ms is None


def test_fetch_day_in_the_past_asks_for_past_days(monkeypatch):
    urls = []

    def fake_get_json(url):
        urls.append(url)
        payload = sample("m/s", [4.0, 6.0])
        payload["daily"]["time"] = ["2026-09-23", "2026-09-24"]
        return payload

    monkeypatch.setattr(open_meteo, "get_json", fake_get_json)
    forecast = open_meteo.fetch_day(67.86, 20.23, "2026-09-24", today=date(2026, 10, 2))
    assert forecast.wind_max_ms == 6.0
    query = parse_qs(urlsplit(urls[0]).query)
    assert query["past_days"] == ["8"]
    assert query["forecast_days"] == ["1"]


def test_fetch_day_too_far_away_is_refused():
    with pytest.raises(ValueError, match="outside"):
        open_meteo.fetch_day(67.86, 20.23, "2026-01-01", today=date(2026, 10, 2))


# Uppgift 4 ---------------------------------------------------------------


def fake_fetch_day(latitude, longitude, day):
    assert (latitude, longitude) == cli.CITY_COORDINATES["Kiruna"]
    return open_meteo.DailyForecast(day, 3.5, -2.0, 4.0, 9.3)


def test_compare_puts_both_sources_side_by_side(base_url):
    table = cli.compare(api_client.client.WeatherClient(base_url), "Kiruna", "2026-09-24", fake_fetch_day)
    lines = table.splitlines()
    assert lines[0] == "Kiruna, 2026-09-24"
    assert lines[2].split() == ["high", "°C", "2.7", "3.5"]
    assert lines[5].split() == ["wind", "m/s", "-", "9.3"]  # vindgivaren var trasig den dagen


def test_compare_needs_coordinates(base_url):
    with pytest.raises(ValueError, match="no coordinates"):
        cli.compare(api_client.client.WeatherClient(base_url), "Atlantis", "2026-09-24", fake_fetch_day)


def test_compare_needs_an_observation(base_url):
    with pytest.raises(ValueError, match="no observation"):
        cli.compare(api_client.client.WeatherClient(base_url), "Kiruna", "2026-10-01", fake_fetch_day)


# Uppgift 5 ---------------------------------------------------------------


def test_delete_is_405_with_an_allow_header(base_url):
    request = urllib.request.Request(f"{base_url}/cities/Kiruna", method="DELETE")
    with pytest.raises(urllib.error.HTTPError) as error_info:
        urllib.request.urlopen(request, timeout=5)
    response = error_info.value
    assert response.code == 405
    assert response.headers["Allow"] == "GET"
    assert json.loads(response.read()) == {"error": "this API is read-only: use GET"}
