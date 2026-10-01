"""The API itself: which URLs exist, what each method does, and what to answer.

`handle()` takes a request as plain values (method, path, body bytes) and
returns a `Response` (status, JSON-ready body, headers). It never touches
a socket, so every rule of the API can be tested by calling one function;
`server.py` is the thin layer that connects it to real HTTP.

Endpoints:

    GET    /cities                                   list cities
    POST   /cities                                   create a city
    GET    /cities/{name}                            one city
    GET    /cities/{name}/observations?from=&to=     a city's observations, optionally by date range
    POST   /cities/{name}/observations               record an observation
    GET    /cities/{name}/observations/{date}        one observation
    DELETE /cities/{name}/observations/{date}        delete one observation
"""

import json
import re
import sqlite3
from dataclasses import dataclass, field
from datetime import date
from urllib.parse import parse_qs, quote, unquote, urlsplit

from weather_api import store


@dataclass(frozen=True)
class Response:
    status: int
    body: object = None  # anything json.dumps accepts; None means "no body"
    headers: dict[str, str] = field(default_factory=dict)


class HttpError(Exception):
    """Raised by a handler to stop and answer with an error status."""

    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status = status


# Each field a client may send, and the JSON types it may have.
# bool is excluded from numbers explicitly: in Python, True is an int.
CITY_FIELDS = {"name": (str,), "country": (str,), "population": (int,)}
OBSERVATION_FIELDS = {
    "observed_on": (str,),
    "temp_max_c": (int, float),
    "temp_min_c": (int, float),
    "precipitation_mm": (int, float),
    "wind_ms": (int, float, type(None)),
    "conditions": (str,),
}
OPTIONAL_FIELDS = {"wind_ms"}


def _parse_body(body: bytes, fields: dict[str, tuple[type, ...]]) -> dict:
    """Decode a JSON object and check it has exactly the expected fields and types."""
    try:
        data = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise HttpError(400, "request body must be valid JSON") from None
    if not isinstance(data, dict):
        raise HttpError(400, "request body must be a JSON object")
    unknown = sorted(set(data) - set(fields))
    if unknown:
        raise HttpError(400, f"unknown field(s): {', '.join(unknown)}")
    for name, types in fields.items():
        if name not in data:
            if name in OPTIONAL_FIELDS:
                data[name] = None
                continue
            raise HttpError(400, f"missing field: {name}")
        value = data[name]
        if isinstance(value, bool) or not isinstance(value, types):
            raise HttpError(400, f"field {name!r} has the wrong type")
    return data


def _date_param(query: dict[str, list[str]], key: str, default: str) -> str:
    if key not in query:
        return default
    value = query[key][0]
    try:
        date.fromisoformat(value)
    except ValueError:
        raise HttpError(400, f"'{key}' must be a date like 2026-09-23, got {value!r}") from None
    return value


def _require_city(conn: sqlite3.Connection, name: str) -> None:
    if store.city(conn, name) is None:
        raise HttpError(404, f"no city named {name!r}")


def _refused_by_database(error: sqlite3.IntegrityError, what: str) -> HttpError:
    # UNIQUE: the thing already exists, which is a clash with current state (409).
    # Anything else (CHECK, NOT NULL): the values themselves are invalid (400).
    if "UNIQUE" in str(error):
        return HttpError(409, f"{what} already exists")
    return HttpError(400, f"invalid value: {error}")


def list_cities(conn, query, body):
    return Response(200, [dict(row) for row in store.cities(conn)])


def create_city(conn, query, body):
    data = _parse_body(body, CITY_FIELDS)
    try:
        store.add_city(conn, data["name"], data["country"], data["population"])
    except sqlite3.IntegrityError as error:
        raise _refused_by_database(error, f"city {data['name']!r}") from None
    location = f"/cities/{quote(data['name'], safe='')}"
    return Response(201, dict(store.city(conn, data["name"])), {"Location": location})


def show_city(conn, query, body, city):
    row = store.city(conn, city)
    if row is None:
        raise HttpError(404, f"no city named {city!r}")
    return Response(200, dict(row))


def list_observations(conn, query, body, city):
    _require_city(conn, city)
    start = _date_param(query, "from", "0000-01-01")
    end = _date_param(query, "to", "9999-12-31")
    return Response(200, [dict(row) for row in store.observations(conn, city, start, end)])


def create_observation(conn, query, body, city):
    data = _parse_body(body, OBSERVATION_FIELDS)
    try:
        created = store.add_observation(conn, city, data)
    except sqlite3.IntegrityError as error:
        raise _refused_by_database(error, f"an observation for {city!r} on {data['observed_on']}") from None
    if not created:
        raise HttpError(404, f"no city named {city!r}")
    location = f"/cities/{quote(city, safe='')}/observations/{data['observed_on']}"
    return Response(201, dict(store.observation(conn, city, data["observed_on"])), {"Location": location})


def show_observation(conn, query, body, city, day):
    row = store.observation(conn, city, day)
    if row is None:
        raise HttpError(404, f"no observation for {city!r} on {day}")
    return Response(200, dict(row))


def delete_observation(conn, query, body, city, day):
    if not store.delete_observation(conn, city, day):
        raise HttpError(404, f"no observation for {city!r} on {day}")
    return Response(204)


ROUTES = [
    (re.compile(r"/cities"), {"GET": list_cities, "POST": create_city}),
    (re.compile(r"/cities/(?P<city>[^/]+)"), {"GET": show_city}),
    (re.compile(r"/cities/(?P<city>[^/]+)/observations"), {"GET": list_observations, "POST": create_observation}),
    (re.compile(r"/cities/(?P<city>[^/]+)/observations/(?P<day>[^/]+)"),
     {"GET": show_observation, "DELETE": delete_observation}),
]


def handle(conn: sqlite3.Connection, method: str, target: str, body: bytes = b"") -> Response:
    """Answer one request. `target` is the path plus any query string, as sent by the client."""
    url = urlsplit(target)
    for pattern, handlers in ROUTES:
        match = pattern.fullmatch(url.path)
        if match:
            break
    else:
        return Response(404, {"error": f"no such endpoint: {url.path}"})

    if method not in handlers:
        allowed = ", ".join(sorted(handlers))
        return Response(405, {"error": f"{method} is not allowed here; use {allowed}"}, {"Allow": allowed})

    path_params = {name: unquote(value) for name, value in match.groupdict().items()}
    try:
        return handlers[method](conn, parse_qs(url.query), body, **path_params)
    except HttpError as error:
        return Response(error.status, {"error": str(error)})
