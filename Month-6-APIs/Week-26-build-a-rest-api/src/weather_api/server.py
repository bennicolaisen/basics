"""Serve `app.handle` over real HTTP with the standard library's http.server.

    python -m weather_api.server weather.db --sample     # create/open weather.db, add the sample week
    python -m weather_api.server weather.db --port 8080

This module only moves bytes: it reads the method, path and body off the
socket, asks `app.handle` what to answer, and writes the status line,
headers and JSON body back. All decisions are made in `app.py`.
"""

import argparse
import json
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from weather_api import store
from weather_api.app import handle


class ApiRequestHandler(BaseHTTPRequestHandler):
    conn: sqlite3.Connection  # set by make_server

    def _dispatch(self) -> None:
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else b""
        response = handle(self.conn, self.command, self.path, body)

        payload = b""
        if response.body is not None:
            payload = json.dumps(response.body, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(response.status)
        if payload:
            self.send_header("Content-Type", "application/json; charset=utf-8")
        if response.status != 204:  # a 204 must not carry a body, or a length for one
            self.send_header("Content-Length", str(len(payload)))
        for name, value in response.headers.items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(payload)

    # Every method goes through the same code; app.handle decides what's allowed.
    do_GET = do_POST = do_PUT = do_PATCH = do_DELETE = _dispatch

    def log_request(self, code="-", size="-") -> None:
        print(f"{self.command} {self.path} -> {code}")


def make_server(conn: sqlite3.Connection, host: str = "127.0.0.1", port: int = 8000) -> HTTPServer:
    """Build (but don't start) a server for `conn`. Port 0 means "any free port"."""
    handler = type("Handler", (ApiRequestHandler,), {"conn": conn})
    return HTTPServer((host, port), handler)


def main() -> None:
    parser = argparse.ArgumentParser(prog="weather_api", description="Serve the weather API.")
    parser.add_argument("database", type=Path, help="SQLite file; created if it doesn't exist")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--sample", action="store_true", help="load the sample week if the log is empty")
    args = parser.parse_args()

    conn = store.open_log(args.database)
    if args.sample and store.load_sample(conn):
        print("Loaded the sample week.")
    server = make_server(conn, port=args.port)
    host, port = server.server_address[:2]
    print(f"Weather API on http://{host}:{port}/cities  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
    finally:
        server.server_close()
        conn.close()


if __name__ == "__main__":
    main()
