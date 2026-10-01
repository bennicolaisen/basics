"""Command-line front end for a weather log stored in a SQLite file.

    python -m weather_log.cli weather.db init
    python -m weather_log.cli weather.db report
    python -m weather_log.cli weather.db show Kiruna
    python -m weather_log.cli weather.db import src/weather_log/data/2026-09-28.csv
    python -m weather_log.cli weather.db correct Visby 2026-09-24 6.0
    python -m weather_log.cli weather.db delete-city Copenhagen
"""

import argparse
import sqlite3
import sys
from pathlib import Path

from weather_log import store
from weather_log.csv_import import read_cities, read_observations

DATA_DIR = Path(__file__).parent / "data"


def print_rows(rows: list[sqlite3.Row]) -> None:
    if not rows:
        print("(no rows)")
        return
    columns = rows[0].keys()
    cells = [["" if row[column] is None else str(row[column]) for column in columns] for row in rows]
    widths = [max(len(text) for text in column) for column in zip(columns, *cells)]
    for line in [columns, ["-" * width for width in widths], *cells]:
        print("  ".join(text.ljust(width) for text, width in zip(line, widths)).rstrip())


def init(conn: sqlite3.Connection) -> None:
    """Load the bundled cities and sample week into an empty log."""
    if conn.execute("SELECT COUNT(*) FROM cities").fetchone()[0]:
        raise ValueError("this log already has data; init only fills an empty one")
    cities = read_cities(DATA_DIR / "cities.csv")
    for name, country, population in cities:
        store.add_city(conn, name, country, population)
    count = store.import_observations(conn, read_observations(DATA_DIR / "sample_week.csv"))
    print(f"Loaded {len(cities)} cities and {count} observations.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="weather_log", description="Keep a weather log in a SQLite file.")
    parser.add_argument("database", type=Path, help="SQLite file; created if it doesn't exist")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("init", help="load the bundled sample week into an empty log")
    commands.add_parser("report", help="per-city summary")
    show = commands.add_parser("show", help="one city's observations")
    show.add_argument("city")
    import_ = commands.add_parser("import", help="add observations from a CSV file, all or nothing")
    import_.add_argument("csv_file", type=Path)
    correct = commands.add_parser("correct", help="fix one precipitation reading")
    correct.add_argument("city")
    correct.add_argument("observed_on", help="YYYY-MM-DD")
    correct.add_argument("precipitation_mm", type=float)
    delete = commands.add_parser("delete-city", help="delete a city and all its observations")
    delete.add_argument("city")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    conn = store.open_log(args.database)
    try:
        if args.command == "init":
            init(conn)
        elif args.command == "report":
            print_rows(store.summary(conn))
        elif args.command == "show":
            print_rows(store.city_observations(conn, args.city))
        elif args.command == "import":
            count = store.import_observations(conn, read_observations(args.csv_file))
            print(f"Imported {count} observations.")
        elif args.command == "correct":
            store.correct_precipitation(conn, args.city, args.observed_on, args.precipitation_mm)
            print("Corrected.")
        elif args.command == "delete-city":
            store.delete_city(conn, args.city)
            print(f"Deleted {args.city} and its observations.")
    except (ValueError, sqlite3.Error) as error:
        sys.exit(f"error: {error}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
