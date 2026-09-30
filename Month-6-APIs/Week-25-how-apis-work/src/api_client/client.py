"""Calling a JSON web API from Python with nothing but the standard library.

`build_url` and `get_json` work with any JSON API. `WeatherClient` wraps
them into methods for the practice API, so the rest of a program can ask
for "Kiruna's observations" without knowing anything about URLs, HTTP
status codes or JSON.
"""

import json
import urllib.error
import urllib.request
from urllib.parse import quote, urlencode

USER_AGENT = "basics-course-weather-client/1.0"


class ApiError(Exception):
    """The server answered, but with an error status (4xx or 5xx)."""

    def __init__(self, status: int, message: str):
        super().__init__(f"HTTP {status}: {message}")
        self.status = status
        self.message = message


def build_url(base_url: str, path_segments: list[str], params: dict[str, object] | None = None) -> str:
    """Join a base URL, path segments and query parameters, encoding each part.

    Each segment is percent-encoded on its own, so a city called
    `"Malmö"` becomes `Malm%C3%B6` and a `/` inside a value can't create
    an extra path level. Parameters whose value is `None` are left out.
    """
    path = "/".join(quote(segment, safe="") for segment in path_segments)
    url = f"{base_url.rstrip('/')}/{path}"
    query = urlencode({key: value for key, value in (params or {}).items() if value is not None})
    return f"{url}?{query}" if query else url


def _error_message(error: urllib.error.HTTPError) -> str:
    # Most JSON APIs explain errors in the body; fall back to the status's reason phrase.
    try:
        body = json.loads(error.read().decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return error.reason
    if isinstance(body, dict):
        return str(body.get("error") or body.get("reason") or error.reason)
    return error.reason


def get_json(url: str, timeout: float = 5.0) -> object:
    """GET `url` and return its JSON body as Python values.

    Raises `ApiError` when the server answers with an error status, and
    `ConnectionError` when there is no answer at all (wrong address,
    server not running, no network).
    """
    request = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:  # must come first: HTTPError is a kind of URLError
        raise ApiError(error.code, _error_message(error)) from None
    except urllib.error.URLError as error:
        raise ConnectionError(f"could not reach {url}: {error.reason}") from None


class WeatherClient:
    """The practice API's endpoints as Python methods."""

    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url

    def cities(self) -> list[dict]:
        return get_json(build_url(self.base_url, ["cities"]))

    def city(self, name: str) -> dict:
        return get_json(build_url(self.base_url, ["cities", name]))

    def observations(self, city: str, start: str | None = None, end: str | None = None) -> list[dict]:
        url = build_url(self.base_url, ["cities", city, "observations"], {"from": start, "to": end})
        return get_json(url)
