import pytest

from api_client.client import ApiError, WeatherClient, build_url, get_json


class TestBuildUrl:
    def test_joins_segments_under_the_base(self):
        assert build_url("http://api.test/", ["cities", "Oslo"]) == "http://api.test/cities/Oslo"

    def test_percent_encodes_non_ascii_and_spaces(self):
        assert build_url("http://api.test", ["cities", "Malmö"]) == "http://api.test/cities/Malm%C3%B6"
        assert build_url("http://api.test", ["cities", "New York"]) == "http://api.test/cities/New%20York"

    def test_slash_in_a_value_cannot_add_a_path_level(self):
        assert build_url("http://api.test", ["cities", "a/b"]) == "http://api.test/cities/a%2Fb"

    def test_adds_query_parameters_and_skips_none(self):
        url = build_url("http://api.test", ["obs"], {"from": "2026-09-23", "to": None})
        assert url == "http://api.test/obs?from=2026-09-23"

    def test_encodes_query_values(self):
        assert build_url("http://api.test", ["search"], {"q": "rain & snow"}) == "http://api.test/search?q=rain+%26+snow"


class TestWeatherClient:
    def test_cities(self, base_url):
        names = [city["name"] for city in WeatherClient(base_url).cities()]
        assert names[:3] == ["Copenhagen", "Gothenburg", "Kiruna"]

    def test_city_with_non_ascii_name(self, base_url):
        assert WeatherClient(base_url).city("Umeå")["population"] == 132235

    def test_observations_in_range(self, base_url):
        rows = WeatherClient(base_url).observations("Stockholm", start="2026-09-26")
        assert [row["observed_on"] for row in rows] == ["2026-09-26", "2026-09-27"]

    def test_json_types_arrive_as_python_types(self, base_url):
        (row,) = WeatherClient(base_url).observations("Umeå", "2026-09-22", "2026-09-22")
        assert row == {
            "observed_on": "2026-09-22",
            "temp_max_c": 11.2,
            "temp_min_c": 5.3,
            "precipitation_mm": 2.4,
            "wind_ms": None,
            "conditions": "cloud",
        }

    def test_not_found_becomes_api_error_with_status_and_message(self, base_url):
        with pytest.raises(ApiError) as caught:
            WeatherClient(base_url).city("Atlantis")
        assert caught.value.status == 404
        assert caught.value.message == "no city named 'Atlantis'"

    def test_bad_request_becomes_api_error(self, base_url):
        with pytest.raises(ApiError) as caught:
            WeatherClient(base_url).observations("Kiruna", start="yesterday")
        assert caught.value.status == 400

    def test_no_server_is_a_connection_error_not_an_api_error(self, closed_port_url):
        with pytest.raises(ConnectionError, match="could not reach"):
            WeatherClient(closed_port_url).cities()


def test_get_json_works_for_any_endpoint(base_url):
    assert get_json(base_url + "/")["endpoints"]
