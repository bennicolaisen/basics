"""The API's behavior, tested by calling app.handle directly: no sockets needed."""

import json

import pytest

from weather_api import store
from weather_api.app import handle

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


def call(conn, method, target, body=None):
    raw = b"" if body is None else (body if isinstance(body, bytes) else json.dumps(body).encode("utf-8"))
    return handle(conn, method, target, raw)


class TestReading:
    def test_list_cities(self, conn):
        response = call(conn, "GET", "/cities")
        assert response.status == 200
        assert len(response.body) == 8
        assert response.body[0] == {"name": "Copenhagen", "country": "Denmark", "population": 660842}

    def test_one_city_with_percent_encoded_name(self, conn):
        response = call(conn, "GET", "/cities/Ume%C3%A5")
        assert (response.status, response.body["name"]) == (200, "Umeå")

    def test_unknown_city_is_404_with_a_message(self, conn):
        response = call(conn, "GET", "/cities/Atlantis")
        assert response.status == 404
        assert response.body == {"error": "no city named 'Atlantis'"}

    def test_observations_filtered_by_date(self, conn):
        response = call(conn, "GET", "/cities/Oslo/observations?from=2026-09-25&to=2026-09-26")
        assert [row["observed_on"] for row in response.body] == ["2026-09-25", "2026-09-26"]

    def test_city_without_observations_is_an_empty_list_not_404(self, conn):
        response = call(conn, "GET", "/cities/Copenhagen/observations")
        assert (response.status, response.body) == (200, [])

    def test_bad_date_parameter_is_400(self, conn):
        assert call(conn, "GET", "/cities/Oslo/observations?from=monday").status == 400

    def test_one_observation(self, conn):
        response = call(conn, "GET", "/cities/Kiruna/observations/2026-09-24")
        assert response.status == 200
        assert response.body["wind_ms"] is None

    def test_missing_observation_is_404(self, conn):
        assert call(conn, "GET", "/cities/Kiruna/observations/2026-10-01").status == 404


class TestCreatingCities:
    def test_created_city_gets_201_and_a_location(self, conn):
        response = call(conn, "POST", "/cities", {"name": "Bergen", "country": "Norway", "population": 291940})
        assert response.status == 201
        assert response.headers == {"Location": "/cities/Bergen"}
        assert call(conn, "GET", response.headers["Location"]).status == 200

    def test_location_is_percent_encoded(self, conn):
        response = call(conn, "POST", "/cities", {"name": "Tromsø", "country": "Norway", "population": 78745})
        assert response.headers["Location"] == "/cities/Troms%C3%B8"

    def test_duplicate_name_is_409_conflict(self, conn):
        response = call(conn, "POST", "/cities", {"name": "Oslo", "country": "Norway", "population": 1})
        assert response.status == 409
        assert response.body == {"error": "city 'Oslo' already exists"}

    def test_database_check_becomes_400(self, conn):
        response = call(conn, "POST", "/cities", {"name": "Nowhere", "country": "Sweden", "population": -5})
        assert response.status == 400
        assert "CHECK" in response.body["error"]

    @pytest.mark.parametrize(
        "body, message",
        [
            (b"{not json", "must be valid JSON"),
            (b"[1, 2]", "must be a JSON object"),
            ({"name": "Bergen", "country": "Norway"}, "missing field: population"),
            ({"name": "Bergen", "country": "Norway", "population": "many"}, "'population' has the wrong type"),
            ({"name": "Bergen", "country": "Norway", "population": True}, "'population' has the wrong type"),
            ({"name": "Bergen", "country": "Norway", "population": 1, "mayor": "X"}, "unknown field(s): mayor"),
        ],
    )
    def test_malformed_bodies_are_400_with_a_reason(self, conn, body, message):
        response = call(conn, "POST", "/cities", body)
        assert response.status == 400
        assert message in response.body["error"]


class TestRecordingObservations:
    def test_created_observation_is_returned_with_its_location(self, conn):
        response = call(conn, "POST", "/cities/Stockholm/observations", NEW_OBSERVATION)
        assert response.status == 201
        assert response.headers["Location"] == "/cities/Stockholm/observations/2026-09-28"
        assert response.body == NEW_OBSERVATION

    def test_wind_is_optional_and_stored_as_null(self, conn):
        body = {key: value for key, value in NEW_OBSERVATION.items() if key != "wind_ms"}
        response = call(conn, "POST", "/cities/Stockholm/observations", body)
        assert response.status == 201
        assert response.body["wind_ms"] is None

    def test_integers_are_accepted_as_numbers(self, conn):
        response = call(conn, "POST", "/cities/Stockholm/observations", {**NEW_OBSERVATION, "temp_min_c": 6})
        assert response.status == 201

    def test_unknown_city_is_404(self, conn):
        assert call(conn, "POST", "/cities/Atlantis/observations", NEW_OBSERVATION).status == 404

    def test_second_reading_for_the_same_day_is_409(self, conn):
        response = call(conn, "POST", "/cities/Stockholm/observations", {**NEW_OBSERVATION, "observed_on": "2026-09-21"})
        assert response.status == 409
        assert response.body == {"error": "an observation for 'Stockholm' on 2026-09-21 already exists"}

    @pytest.mark.parametrize(
        "change",
        [
            {"precipitation_mm": -1},
            {"conditions": "hail"},
            {"observed_on": "28/09/2026"},
            {"temp_min_c": 30.0},
        ],
    )
    def test_values_the_schema_rejects_are_400(self, conn, change):
        response = call(conn, "POST", "/cities/Stockholm/observations", {**NEW_OBSERVATION, **change})
        assert response.status == 400

    def test_nothing_is_stored_when_refused(self, conn):
        call(conn, "POST", "/cities/Stockholm/observations", {**NEW_OBSERVATION, "conditions": "hail"})
        assert call(conn, "GET", "/cities/Stockholm/observations/2026-09-28").status == 404


class TestDeleting:
    def test_delete_is_204_with_no_body_and_really_deletes(self, conn):
        response = call(conn, "DELETE", "/cities/Visby/observations/2026-09-27")
        assert (response.status, response.body) == (204, None)
        assert call(conn, "GET", "/cities/Visby/observations/2026-09-27").status == 404

    def test_deleting_twice_is_404_the_second_time(self, conn):
        call(conn, "DELETE", "/cities/Visby/observations/2026-09-27")
        assert call(conn, "DELETE", "/cities/Visby/observations/2026-09-27").status == 404


class TestRouting:
    def test_unknown_path_is_404(self, conn):
        assert call(conn, "GET", "/weather").status == 404

    def test_trailing_parts_do_not_match_a_shorter_route(self, conn):
        assert call(conn, "GET", "/cities/Oslo/observations/2026-09-21/extra").status == 404

    @pytest.mark.parametrize(
        "method, target, allowed",
        [
            ("DELETE", "/cities", "GET, POST"),
            ("PUT", "/cities/Oslo", "GET"),
            ("PATCH", "/cities/Oslo/observations/2026-09-21", "DELETE, GET"),
        ],
    )
    def test_wrong_method_is_405_with_allow_header(self, conn, method, target, allowed):
        response = call(conn, method, target)
        assert response.status == 405
        assert response.headers == {"Allow": allowed}
