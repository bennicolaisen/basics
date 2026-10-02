"""Facit vecka 26: API:et med uppgift 1-4. Se FACIT.md.

Allt från veckans app.py som inte ändras återanvänds härifrån. Nytt:

    PATCH  /cities/{name}/observations/{date}     ändra några fält (uppgift 1)
    DELETE /cities/{name}                         ta bort staden och dess observationer (uppgift 2)
    GET    /cities/{name}/summary?from=&to=       sammanfattning räknad i SQL (uppgift 3)

och, om servern startas med en nyckel, kräver alla skrivande anrop
headern X-API-Key (uppgift 4).
"""

import hmac
import json
import re
import sqlite3
from collections.abc import Mapping
from urllib.parse import parse_qs, unquote, urlsplit

from weather_api import app as original
from weather_api.app import HttpError, Response, _date_param, _require_city

from facit import store as facit_store

WRITE_METHODS = {"POST", "PATCH", "PUT", "DELETE"}


def _parse_patch(body: bytes) -> dict:
    """Uppgift 1: ett JSON-objekt med NÅGRA av observationens fält, rätt typer."""
    try:
        data = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise HttpError(400, "request body must be valid JSON") from None
    if not isinstance(data, dict):
        raise HttpError(400, "request body must be a JSON object")
    if "observed_on" in data:
        raise HttpError(400, "observed_on cannot be changed; delete the observation and create a new one")
    unknown = sorted(set(data) - set(facit_store.PATCHABLE_FIELDS))
    if unknown:
        raise HttpError(400, f"unknown field(s): {', '.join(unknown)}")
    if not data:
        raise HttpError(400, "nothing to change: send at least one field")
    for name, value in data.items():
        types = original.OBSERVATION_FIELDS[name]
        if isinstance(value, bool) or not isinstance(value, types):
            raise HttpError(400, f"field {name!r} has the wrong type")
    return data


def patch_observation(conn, query, body, city, day):
    changes = _parse_patch(body)
    try:
        updated = facit_store.update_observation(conn, city, day, changes)
    except sqlite3.IntegrityError as error:
        # CHECK-regler, till exempel att lägsta inte får vara över högsta
        # efter ändringen. Det är värdena som är fel: 400.
        raise HttpError(400, f"invalid value: {error}") from None
    if not updated:
        raise HttpError(404, f"no observation for {city!r} on {day}")
    return Response(200, dict(original.store.observation(conn, city, day)))


def delete_city(conn, query, body, city):
    if not facit_store.delete_city(conn, city):
        raise HttpError(404, f"no city named {city!r}")
    return Response(204)


def city_summary(conn, query, body, city):
    _require_city(conn, city)
    start = _date_param(query, "from", "0000-01-01")
    end = _date_param(query, "to", "9999-12-31")
    if start > end:
        raise HttpError(400, f"'from' ({start}) is after 'to' ({end})")
    row = dict(facit_store.summary(conn, city, start, end))
    if "from" in query:
        row["from"] = start
    if "to" in query:
        row["to"] = end
    return Response(200, row)


ROUTES = [
    (re.compile(r"/cities"), {"GET": original.list_cities, "POST": original.create_city}),
    (re.compile(r"/cities/(?P<city>[^/]+)"), {"GET": original.show_city, "DELETE": delete_city}),
    (re.compile(r"/cities/(?P<city>[^/]+)/summary"), {"GET": city_summary}),
    (re.compile(r"/cities/(?P<city>[^/]+)/observations"),
     {"GET": original.list_observations, "POST": original.create_observation}),
    (re.compile(r"/cities/(?P<city>[^/]+)/observations/(?P<day>[^/]+)"),
     {"GET": original.show_observation, "PATCH": patch_observation, "DELETE": original.delete_observation}),
]


def _authorized(headers: Mapping[str, str] | None, api_key: str) -> bool:
    # HTTP-headers är inte skiftlägeskänsliga: X-API-Key och x-api-key är samma header.
    sent = {name.lower(): value for name, value in (headers or {}).items()}.get("x-api-key", "")
    # compare_digest tar lika lång tid oavsett hur många tecken som stämmer,
    # så nyckeln kan inte gissas fram tecken för tecken genom att mäta svarstiden.
    return hmac.compare_digest(sent.encode("utf-8"), api_key.encode("utf-8"))


def handle(
    conn: sqlite3.Connection,
    method: str,
    target: str,
    body: bytes = b"",
    headers: Mapping[str, str] | None = None,
    api_key: str | None = None,
) -> Response:
    """Som veckans handle, plus headers och nyckeln servern startades med.

    Med api_key=None är API:et öppet, som veckans original.
    """
    if api_key is not None and method in WRITE_METHODS and not _authorized(headers, api_key):
        return Response(
            401,
            {"error": "missing or wrong API key; send it in the X-API-Key header"},
            {"WWW-Authenticate": 'ApiKey header="X-API-Key"'},
        )

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
