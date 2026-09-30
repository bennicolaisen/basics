"""A small, read-only weather API to practise on, running on your own machine.

    python -m api_client.practice_api            # serves http://127.0.0.1:8000

Endpoints (all GET, all answering JSON):

    /                                       what this API offers
    /cities                                 every city
    /cities/{name}                          one city
    /cities/{name}/observations             that city's observations
        ?from=YYYY-MM-DD&to=YYYY-MM-DD      optional date range, inclusive

This week is about *using* an API, so treat this file as the server
someone else wrote. Week 26 is about building one, and explains every
part of how this works.
"""

import json
import re
import sqlite3
from datetime import date
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

DATA_SQL = Path(__file__).parent / "data" / "weather.sql"
CITY_PATH = re.compile(r"^/cities/([^/]+)$")
OBSERVATIONS_PATH = re.compile(r"^/cities/([^/]+)/observations$")


class ClientError(Exception):
    """A request the API can't answer; carries the HTTP status to reply with."""

    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status = status


def open_database() -> sqlite3.Connection:
    # The server answers requests on its own thread, not the one that
    # opened the connection; it handles one request at a time, so sharing is safe.
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.executescript(DATA_SQL.read_text(encoding="utf-8"))
    return conn


def _city(conn: sqlite3.Connection, name: str) -> sqlite3.Row:
    row = conn.execute("SELECT id, name, country, population FROM cities WHERE name = ?", (name,)).fetchone()
    if row is None:
        raise ClientError(404, f"no city named {name!r}")
    return row


def _date_param(query: dict[str, list[str]], key: str) -> str | None:
    if key not in query:
        return None
    value = query[key][0]
    try:
        date.fromisoformat(value)
    except ValueError:
        raise ClientError(400, f"'{key}' must be a date like 2026-09-23, got {value!r}") from None
    return value


def route(conn: sqlite3.Connection, path: str, query: dict[str, list[str]]) -> object:
    """Answer one GET request with a JSON-ready value, or raise ClientError."""
    if path == "/":
        return {
            "endpoints": [
                "/cities",
                "/cities/{name}",
                "/cities/{name}/observations?from=YYYY-MM-DD&to=YYYY-MM-DD",
            ]
        }
    if path == "/cities":
        rows = conn.execute("SELECT name, country, population FROM cities ORDER BY name").fetchall()
        return [dict(row) for row in rows]
    if match := CITY_PATH.match(path):
        city = dict(_city(conn, unquote(match.group(1))))
        del city["id"]
        return city
    if match := OBSERVATIONS_PATH.match(path):
        city = _city(conn, unquote(match.group(1)))
        start = _date_param(query, "from") or "0000-01-01"
        end = _date_param(query, "to") or "9999-12-31"
        rows = conn.execute(
            """
            SELECT observed_on, temp_max_c, temp_min_c, precipitation_mm, wind_ms, conditions
            FROM observations
            WHERE city_id = ? AND observed_on BETWEEN ? AND ?
            ORDER BY observed_on
            """,
            (city["id"], start, end),
        ).fetchall()
        return [dict(row) for row in rows]
    raise ClientError(404, f"no such endpoint: {path}")


class PracticeApiHandler(BaseHTTPRequestHandler):
    conn: sqlite3.Connection  # set by make_server

    def do_GET(self) -> None:
        url = urlsplit(self.path)
        try:
            status, payload = 200, route(self.conn, url.path, parse_qs(url.query))
        except ClientError as error:
            status, payload = error.status, {"error": str(error)}
        self._send_json(status, payload)

    def _method_not_allowed(self) -> None:
        self._send_json(405, {"error": "this API is read-only: use GET"}, {"Allow": "GET"})

    do_POST = do_PUT = do_PATCH = do_DELETE = _method_not_allowed

    def _send_json(self, status: int, payload: object, headers: dict[str, str] | None = None) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        for name, value in (headers or {}).items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(body)

    def log_request(self, code="-", size="-") -> None:
        # One short line per request instead of the default Apache-style log.
        print(f"{self.command} {self.path} -> {code}")


def make_server(host: str = "127.0.0.1", port: int = 8000) -> HTTPServer:
    """Build (but don't start) the server. Port 0 means "any free port"."""
    handler = type("Handler", (PracticeApiHandler,), {"conn": open_database()})
    return HTTPServer((host, port), handler)


def main() -> None:
    server = make_server()
    host, port = server.server_address[:2]
    print(f"Practice weather API on http://{host}:{port}/  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
