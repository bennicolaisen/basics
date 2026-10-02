"""Facit vecka 25, uppgift 4: kommandot compare. Se FACIT.md.

Starta övnings-API:et i en terminal (python -m api_client.practice_api)
och kör sedan, i en annan, från veckans mapp:

    PYTHONPATH=src python3 -m facit.cli compare Kiruna 2026-09-23
"""

import argparse
import sys

from api_client.client import ApiError, WeatherClient

from facit import open_meteo

DEFAULT_BASE_URL = "http://127.0.0.1:8000"

# Det övnings-API:et inte har: var städerna ligger. Open-Meteo vill ha
# latitud och longitud, inte ett namn. (Ungefärliga koordinater för
# stadskärnan, i decimalgrader.)
CITY_COORDINATES = {
    "Stockholm": (59.33, 18.07),
    "Gothenburg": (57.71, 11.97),
    "Malmö": (55.60, 13.00),
    "Umeå": (63.83, 20.26),
    "Kiruna": (67.86, 20.23),
    "Visby": (57.64, 18.30),
    "Oslo": (59.91, 10.75),
    "Copenhagen": (55.68, 12.57),
}

FIELDS = [
    ("temp_max_c", "high °C"),
    ("temp_min_c", "low °C"),
    ("precipitation_mm", "precipitation mm"),
    ("wind_ms", "wind m/s"),
]


def compare(client: WeatherClient, city: str, day: str, fetch_day=open_meteo.fetch_day) -> str:
    """Övnings-API:ets observation och Open-Meteos värden för samma stad och dag, som en tabell."""
    if city not in CITY_COORDINATES:
        raise ValueError(f"no coordinates for {city!r}; known cities: {', '.join(CITY_COORDINATES)}")
    observations = client.observations(city, day, day)
    if not observations:
        raise ValueError(f"the practice API has no observation for {city} on {day}")
    observed = observations[0]
    latitude, longitude = CITY_COORDINATES[city]
    forecast = fetch_day(latitude, longitude, day)
    forecast_values = {
        "temp_max_c": forecast.temp_max_c,
        "temp_min_c": forecast.temp_min_c,
        "precipitation_mm": forecast.precipitation_mm,
        "wind_ms": forecast.wind_max_ms,
    }
    lines = [f"{city}, {day}", f"{'':<18}{'observed':>10}{'Open-Meteo':>12}"]
    for key, label in FIELDS:
        lines.append(f"{label:<18}{_cell(observed[key]):>10}{_cell(forecast_values[key]):>12}")
    lines.append("(observed wind is the daily mean; Open-Meteo's is the daily maximum)")
    return "\n".join(lines)


def _cell(value) -> str:
    return "-" if value is None else f"{value:.1f}"


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="facit.cli")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    commands = parser.add_subparsers(dest="command", required=True)
    compare_parser = commands.add_parser("compare", help="practice API vs Open-Meteo for one city and day")
    compare_parser.add_argument("city")
    compare_parser.add_argument("day", help="YYYY-MM-DD")
    args = parser.parse_args(argv)
    try:
        print(compare(WeatherClient(args.base_url), args.city, args.day))
    except (ApiError, ConnectionError, ValueError) as error:
        sys.exit(f"error: {error}")


if __name__ == "__main__":
    main()
