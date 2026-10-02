"""Facit vecka 22: veckans CLI med rename-city (uppgift 2) och ett tydligt
besked när en stad inte kan tas bort (uppgift 3).

    PYTHONPATH=src python3 -m facit.cli weather.db init
    PYTHONPATH=src python3 -m facit.cli weather.db rename-city Visby Gotland
    PYTHONPATH=src python3 -m facit.cli weather.db delete-city Copenhagen

Använd en ny databasfil: en fil som skapats med veckans schema har kvar
ON DELETE CASCADE, eftersom CREATE TABLE IF NOT EXISTS inte ändrar en
tabell som redan finns.
"""

import argparse
import sqlite3
import sys
from pathlib import Path

from weather_log.cli import init, print_rows
from weather_log.csv_import import read_observations

from facit import store


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
    delete = commands.add_parser("delete-city", help="delete a city that has no observations")
    delete.add_argument("city")
    rename = commands.add_parser("rename-city", help="give a city a new name")
    rename.add_argument("old")
    rename.add_argument("new")
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
            print(f"Deleted {args.city}.")
        elif args.command == "rename-city":
            store.rename_city(conn, args.old, args.new)
            print(f"Renamed {args.old} to {args.new}.")
    except store.CityInUseError as error:
        sys.exit(f"cannot delete: {error}")
    except store.CityNameTakenError as error:
        sys.exit(f"cannot rename: {error}")
    except (ValueError, sqlite3.Error) as error:
        sys.exit(f"error: {error}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
