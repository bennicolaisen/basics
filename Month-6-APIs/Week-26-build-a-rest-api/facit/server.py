"""Facit vecka 26: servern med API-nyckel (uppgift 4).

    export WEATHER_API_KEY=hemligt          # PowerShell: $env:WEATHER_API_KEY="hemligt"
    PYTHONPATH=src python3 -m facit.server weather.db --sample

Nyckeln läses EN gång, när servern startar, och skickas sedan till
facit.app.handle med varje förfrågan. Saknas variabeln startar servern
inte alls: hellre ingen server än en server som av misstag är öppen.
"""

import argparse
import json
import os
import sqlite3
import sys
from http.server import HTTPServer
from pathlib import Path

from weather_api import store
from weather_api.server import ApiRequestHandler

from facit.app import handle

API_KEY_VARIABLE = "WEATHER_API_KEY"


class FacitRequestHandler(ApiRequestHandler):
    api_key: str | None  # set by make_server

    def _dispatch(self) -> None:
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else b""
        response = handle(self.conn, self.command, self.path, body, self.headers, self.api_key)

        payload = b""
        if response.body is not None:
            payload = json.dumps(response.body, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(response.status)
        if payload:
            self.send_header("Content-Type", "application/json; charset=utf-8")
        if response.status != 204:
            self.send_header("Content-Length", str(len(payload)))
        for name, value in response.headers.items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(payload)

    do_GET = do_POST = do_PUT = do_PATCH = do_DELETE = _dispatch


def make_server(conn: sqlite3.Connection, api_key: str | None, host: str = "127.0.0.1", port: int = 8000) -> HTTPServer:
    handler = type("Handler", (FacitRequestHandler,), {"conn": conn, "api_key": api_key})
    return HTTPServer((host, port), handler)


def main() -> None:
    parser = argparse.ArgumentParser(prog="facit.server", description="Serve the weather API with an API key.")
    parser.add_argument("database", type=Path)
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--sample", action="store_true")
    args = parser.parse_args()

    api_key = os.environ.get(API_KEY_VARIABLE)
    if not api_key:
        sys.exit(f"set the {API_KEY_VARIABLE} environment variable to the key clients must send")

    conn = store.open_log(args.database)
    if args.sample and store.load_sample(conn):
        print("Loaded the sample week.")
    server = make_server(conn, api_key, port=args.port)
    host, port = server.server_address[:2]
    print(f"Weather API on http://{host}:{port}/cities  (writes need X-API-Key; Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
    finally:
        server.server_close()
        conn.close()


if __name__ == "__main__":
    main()
