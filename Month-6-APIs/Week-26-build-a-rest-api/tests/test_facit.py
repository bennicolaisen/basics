"""Tester för facit/ (uppgift 1-5). Se FACIT.md."""

import json
import threading
import urllib.error
import urllib.request

import pytest

from facit import app as facit_app
from facit.client import ApiError, FacitWeatherClient
from facit.server import make_server
from weather_api import store

KEY = "test-key"

NEW_OBSERVATION = {
    "observed_on": "2026-09-28",
    "temp_max_c": 12.6,
    "temp_min_c": 6.1,
    "precipitation_mm": 2.8,
    "wind_ms": 5.9,
    "conditions": "rain",
}


@pytest.fixture
def conn():
    conn = store.open_log()
    store.load_sample(conn)
    return conn


def call(conn, method, target, body=None, headers=None, api_key=None):
    raw = b"" if body is None else (body if isinstance(body, bytes) else json.dumps(body).encode("utf-8"))
    return facit_app.handle(conn, method, target, raw, headers, api_key)


# Uppgift 1: PATCH --------------------------------------------------------


class TestPatch:
    def test_changes_only_the_fields_sent(self, conn):
        response = call(conn, "PATCH", "/cities/Kiruna/observations/2026-09-24", {"wind_ms": 4.0})
        assert response.status == 200
        assert response.body == {
            "observed_on": "2026-09-24",
            "temp_max_c": 2.7,
            "temp_min_c": -3.8,
            "precipitation_mm": 2.9,
            "wind_ms": 4.0,
            "conditions": "snow",
        }

    def test_several_fields_and_null_wind(self, conn):
        response = call(
            conn, "PATCH", "/cities/Oslo/observations/2026-09-21", {"conditions": "cloud", "wind_ms": None}
        )
        assert (response.body["conditions"], response.body["wind_ms"]) == ("cloud", None)

    def test_other_observations_are_untouched(self, conn):
        call(conn, "PATCH", "/cities/Oslo/observations/2026-09-21", {"temp_max_c": 20.0})
        assert call(conn, "GET", "/cities/Oslo/observations/2026-09-22").body["temp_max_c"] == 13.6
        assert call(conn, "GET", "/cities/Stockholm/observations/2026-09-21").body["temp_max_c"] == 16.2

    @pytest.mark.parametrize(
        ("body", "message"),
        [
            ({}, "nothing to change"),
            ({"observed_on": "2026-09-30"}, "cannot be changed"),
            ({"humidity": 80}, "unknown field"),
            ({"temp_max_c": "warm"}, "wrong type"),
            ({"temp_max_c": True}, "wrong type"),
            ([1, 2], "JSON object"),
            (b"{not json", "valid JSON"),
        ],
    )
    def test_bad_bodies_are_400(self, conn, body, message):
        response = call(conn, "PATCH", "/cities/Oslo/observations/2026-09-21", body)
        assert response.status == 400
        assert message in response.body["error"]

    def test_values_the_schema_refuses_are_400_and_change_nothing(self, conn):
        response = call(conn, "PATCH", "/cities/Oslo/observations/2026-09-21", {"temp_min_c": 30.0})
        assert response.status == 400
        assert call(conn, "GET", "/cities/Oslo/observations/2026-09-21").body["temp_min_c"] == 7.2

    @pytest.mark.parametrize(
        "target", ["/cities/Atlantis/observations/2026-09-21", "/cities/Oslo/observations/2026-10-01"]
    )
    def test_missing_city_or_day_is_404(self, conn, target):
        assert call(conn, "PATCH", target, {"wind_ms": 1.0}).status == 404


# Uppgift 2: DELETE /cities/{name} ----------------------------------------


class TestDeleteCity:
    def test_deletes_the_city_and_its_observations(self, conn):
        response = call(conn, "DELETE", "/cities/Kiruna")
        assert (response.status, response.body) == (204, None)
        assert call(conn, "GET", "/cities/Kiruna").status == 404
        left = conn.execute(
            "SELECT COUNT(*) FROM observations WHERE city_id NOT IN (SELECT id FROM cities)"
        ).fetchone()[0]
        assert left == 0
        assert conn.execute("SELECT COUNT(*) FROM observations").fetchone()[0] == 42

    def test_unknown_city_is_404(self, conn):
        assert call(conn, "DELETE", "/cities/Atlantis").status == 404

    def test_allow_header_now_lists_delete(self, conn):
        response = call(conn, "PUT", "/cities/Oslo")
        assert response.status == 405
        assert response.headers["Allow"] == "DELETE, GET"


# Uppgift 3: summary --------------------------------------------------------


class TestSummary:
    def test_whole_week(self, conn):
        response = call(conn, "GET", "/cities/Stockholm/summary")
        assert response.status == 200
        assert response.body == {
            "city": "Stockholm",
            "observations": 7,
            "average_high_c": 14.8,
            "total_precipitation_mm": 11.1,
        }

    def test_date_range_is_inclusive_and_echoed(self, conn):
        response = call(conn, "GET", "/cities/Stockholm/summary?from=2026-09-23&to=2026-09-25")
        assert response.body == {
            "city": "Stockholm",
            "observations": 3,
            "average_high_c": 13.8,
            "total_precipitation_mm": 9.5,
            "from": "2026-09-23",
            "to": "2026-09-25",
        }

    def test_range_without_observations(self, conn):
        response = call(conn, "GET", "/cities/Oslo/summary?from=2026-10-01")
        assert response.status == 200
        assert response.body["observations"] == 0
        assert response.body["average_high_c"] is None
        assert response.body["total_precipitation_mm"] == 0

    def test_city_without_any_observations(self, conn):
        assert call(conn, "GET", "/cities/Copenhagen/summary").body["observations"] == 0

    @pytest.mark.parametrize(
        ("target", "status"),
        [
            ("/cities/Atlantis/summary", 404),
            ("/cities/Oslo/summary?from=yesterday", 400),
            ("/cities/Oslo/summary?from=2026-09-25&to=2026-09-21", 400),
        ],
    )
    def test_errors(self, conn, target, status):
        assert call(conn, "GET", target).status == status


# Uppgift 4: API-nyckel ---------------------------------------------------


class TestApiKey:
    def test_writes_without_a_key_are_401(self, conn):
        response = call(conn, "POST", "/cities/Oslo/observations", NEW_OBSERVATION, api_key=KEY)
        assert response.status == 401
        assert response.headers["WWW-Authenticate"] == 'ApiKey header="X-API-Key"'
        assert call(conn, "GET", "/cities/Oslo/observations/2026-09-28").status == 404

    def test_a_wrong_key_is_401(self, conn):
        response = call(conn, "DELETE", "/cities/Oslo", headers={"X-API-Key": "guess"}, api_key=KEY)
        assert response.status == 401

    def test_the_right_key_is_accepted_whatever_the_header_case(self, conn):
        response = call(conn, "DELETE", "/cities/Oslo", headers={"x-api-key": KEY}, api_key=KEY)
        assert response.status == 204

    def test_reads_stay_open(self, conn):
        assert call(conn, "GET", "/cities/Oslo", api_key=KEY).status == 200

    def test_without_a_configured_key_the_api_is_open(self, conn):
        assert call(conn, "DELETE", "/cities/Oslo").status == 204


# Uppgift 4 och 5 över riktig HTTP ----------------------------------------


@pytest.fixture
def server_url():
    conn = store.open_log()
    store.load_sample(conn)
    server = make_server(conn, KEY, port=0)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    host, port = server.server_address[:2]
    yield f"http://{host}:{port}"
    server.shutdown()
    server.server_close()


def test_server_passes_the_header_through(server_url):
    def delete(headers):
        request = urllib.request.Request(f"{server_url}/cities/Visby", method="DELETE", headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=5) as response:
                return response.status
        except urllib.error.HTTPError as error:
            return error.code

    assert delete({}) == 401
    assert delete({"X-API-Key": KEY}) == 204


class TestClient:
    def test_add_observation_returns_what_was_stored(self, server_url):
        client = FacitWeatherClient(server_url, api_key=KEY)
        stored = client.add_observation("Oslo", NEW_OBSERVATION)
        assert stored == NEW_OBSERVATION
        assert client.observations("Oslo", "2026-09-28", "2026-09-28") == [NEW_OBSERVATION]

    def test_city_names_are_encoded(self, server_url):
        stored = FacitWeatherClient(server_url, api_key=KEY).add_observation("Malmö", NEW_OBSERVATION)
        assert stored["observed_on"] == "2026-09-28"

    @pytest.mark.parametrize(
        ("city", "changes", "status"),
        [
            ("Oslo", {"conditions": "hail"}, 400),
            ("Atlantis", {}, 404),
            ("Oslo", {"observed_on": "2026-09-21"}, 409),
        ],
    )
    def test_errors_carry_the_status(self, server_url, city, changes, status):
        client = FacitWeatherClient(server_url, api_key=KEY)
        with pytest.raises(ApiError) as error_info:
            client.add_observation(city, {**NEW_OBSERVATION, **changes})
        assert error_info.value.status == status

    def test_missing_key_is_401(self, server_url):
        with pytest.raises(ApiError) as error_info:
            FacitWeatherClient(server_url).add_observation("Oslo", NEW_OBSERVATION)
        assert error_info.value.status == 401
