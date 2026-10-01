"""The practice API seen at the HTTP level: status codes, headers, JSON bodies."""

import json
import urllib.error
import urllib.request

import pytest


def request(base_url: str, path: str, method: str = "GET"):
    """Return (status, headers, parsed JSON body) whatever the status."""
    req = urllib.request.Request(base_url + path, method=method)
    try:
        response = urllib.request.urlopen(req, timeout=5)
    except urllib.error.HTTPError as error:
        response = error
    with response:
        return response.status, response.headers, json.loads(response.read().decode("utf-8"))


def test_index_lists_the_endpoints(base_url):
    status, _, body = request(base_url, "/")
    assert status == 200
    assert "/cities" in body["endpoints"]


def test_responses_are_labelled_as_utf8_json(base_url):
    _, headers, _ = request(base_url, "/cities")
    assert headers["Content-Type"] == "application/json; charset=utf-8"


def test_cities_is_a_list_of_objects(base_url):
    status, _, body = request(base_url, "/cities")
    assert status == 200
    assert len(body) == 8
    assert body[0] == {"name": "Copenhagen", "country": "Denmark", "population": 660842}


def test_percent_encoded_city_name_is_decoded(base_url):
    status, _, body = request(base_url, "/cities/Malm%C3%B6")
    assert status == 200
    assert body["name"] == "Malmö"


def test_observations_with_date_range(base_url):
    status, _, body = request(base_url, "/cities/Kiruna/observations?from=2026-09-23&to=2026-09-24")
    assert status == 200
    assert [obs["observed_on"] for obs in body] == ["2026-09-23", "2026-09-24"]
    assert body[1]["wind_ms"] is None  # SQL NULL -> JSON null -> Python None


@pytest.mark.parametrize(
    "path, status",
    [
        ("/cities/Atlantis", 404),
        ("/cities/Atlantis/observations", 404),
        ("/weather", 404),
        ("/cities/Kiruna/observations?from=yesterday", 400),
        ("/cities/Kiruna/observations?to=2026-13-01", 400),
    ],
)
def test_errors_have_a_status_and_a_message(base_url, path, status):
    got_status, _, body = request(base_url, path)
    assert got_status == status
    assert body["error"]


def test_writes_are_refused_with_405_and_an_allow_header(base_url):
    status, headers, _ = request(base_url, "/cities", method="POST")
    assert status == 405
    assert headers["Allow"] == "GET"
