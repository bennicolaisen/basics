"""Talk to the practice API (or Open-Meteo) from the command line.

Start the practice API in one terminal:

    python -m api_client.practice_api

Then, in another:

    python -m api_client.cli raw /cities/Kiruna          # the full HTTP response
    python -m api_client.cli cities
    python -m api_client.cli observations Kiruna --from 2026-09-23 --to 2026-09-25
    python -m api_client.cli forecast 67.86 20.23         # live forecast from Open-Meteo
"""

import argparse
import json
import sys
import urllib.error
import urllib.request
from urllib.parse import quote

from api_client.client import ApiError, WeatherClient
from api_client.open_meteo import fetch_forecast

DEFAULT_BASE_URL = "http://127.0.0.1:8000"


def show_raw(base_url: str, path: str) -> None:
    """Print a response the way it arrives: status line, headers, blank line, body."""
    # quote() percent-encodes characters a URL can't carry as-is, like the ö in Malmö.
    url = base_url.rstrip("/") + "/" + quote(path.lstrip("/"), safe="/?=&")
    print(f"> GET {url}\n")
    try:
        response = urllib.request.urlopen(url, timeout=5)
    except urllib.error.HTTPError as error:
        response = error  # an error response still has a status, headers and a body
    except urllib.error.URLError as error:
        raise ConnectionError(f"could not reach {url}: {error.reason}") from None
    with response:
        print(f"< HTTP {response.status} {response.reason}")
        for name, value in response.headers.items():
            print(f"< {name}: {value}")
        print()
        print(response.read().decode("utf-8"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="api_client", description="Call the practice weather API.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help=f"default: {DEFAULT_BASE_URL}")
    commands = parser.add_subparsers(dest="command", required=True)
    raw = commands.add_parser("raw", help="show the full HTTP response for a path")
    raw.add_argument("path", help="for example /cities/Oslo")
    commands.add_parser("cities", help="list the cities")
    observations = commands.add_parser("observations", help="one city's observations")
    observations.add_argument("city")
    observations.add_argument("--from", dest="start", help="YYYY-MM-DD")
    observations.add_argument("--to", dest="end", help="YYYY-MM-DD")
    forecast = commands.add_parser("forecast", help="live 3-day forecast from Open-Meteo")
    forecast.add_argument("latitude", type=float)
    forecast.add_argument("longitude", type=float)
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    client = WeatherClient(args.base_url)
    try:
        if args.command == "raw":
            show_raw(args.base_url, args.path)
        elif args.command == "cities":
            for city in client.cities():
                print(f"{city['name']:<12} {city['country']:<8} {city['population']:>9,}")
        elif args.command == "observations":
            for obs in client.observations(args.city, args.start, args.end):
                print(json.dumps(obs, ensure_ascii=False))
        elif args.command == "forecast":
            for day in fetch_forecast(args.latitude, args.longitude):
                print(f"{day.day}  {day.temp_min_c:5.1f} to {day.temp_max_c:5.1f} °C  {day.precipitation_mm:4.1f} mm")
    except (ApiError, ConnectionError) as error:
        sys.exit(f"error: {error}")


if __name__ == "__main__":
    main()
