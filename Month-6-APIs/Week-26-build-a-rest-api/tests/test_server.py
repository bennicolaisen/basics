"""End to end: the same API over real HTTP, to check the server.py layer."""

import json
import threading
import urllib.error
import urllib.request

import pytest

from weather_api import store
from weather_api.server import make_server


@pytest.fixture(scope="module")
def base_url():
    conn = store.open_log()
    store.load_sample(conn)
    server = make_server(conn, port=0)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    host, port = server.server_address[:2]
    yield f"http://{host}:{port}"
    server.shutdown()
    server.server_close()


def send(base_url, method, path, body=None):
    data = None if body is None else json.dumps(body).encode("utf-8")
    request = urllib.request.Request(base_url + path, data=data, method=method)
    if data is not None:
        request.add_header("Content-Type", "application/json")
    try:
        response = urllib.request.urlopen(request, timeout=5)
    except urllib.error.HTTPError as error:
        response = error
    with response:
        return response.status, response.headers, response.read()


def test_get_returns_utf8_json(base_url):
    status, headers, raw = send(base_url, "GET", "/cities/Malm%C3%B6")
    assert status == 200
    assert headers["Content-Type"] == "application/json; charset=utf-8"
    assert int(headers["Content-Length"]) == len(raw)
    assert json.loads(raw.decode("utf-8"))["name"] == "Malmö"


def test_post_reads_the_request_body(base_url):
    status, headers, raw = send(base_url, "POST", "/cities", {"name": "Bergen", "country": "Norway", "population": 291940})
    assert status == 201
    assert headers["Location"] == "/cities/Bergen"
    assert json.loads(raw)["population"] == 291940


def test_error_responses_carry_a_json_message(base_url):
    status, _, raw = send(base_url, "GET", "/cities/Atlantis")
    assert status == 404
    assert json.loads(raw) == {"error": "no city named 'Atlantis'"}


def test_204_has_no_body_and_no_content_type(base_url):
    status, headers, raw = send(base_url, "DELETE", "/cities/Oslo/observations/2026-09-27")
    assert status == 204
    assert raw == b""
    assert "Content-Type" not in headers


def test_405_sends_the_allow_header(base_url):
    status, headers, _ = send(base_url, "PUT", "/cities")
    assert status == 405
    assert headers["Allow"] == "GET, POST"
