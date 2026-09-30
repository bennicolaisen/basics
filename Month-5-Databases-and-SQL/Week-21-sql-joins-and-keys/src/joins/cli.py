"""Run a bundled query by name, or type your own SQL at a prompt.

    python -m joins.cli                  # interactive SQL prompt
    python -m joins.cli q04_wet_days     # run one bundled query
"""

import sqlite3
import sys

from joins.runner import format_table, load_query, open_database, query_names, run_query

PROMPT = "sql> "
CONTINUATION_PROMPT = " ..> "


def print_result(conn: sqlite3.Connection, sql: str) -> None:
    columns, rows = run_query(conn, sql)
    print(format_table(columns, rows) if columns else "OK")


def shell(conn: sqlite3.Connection) -> None:
    """Read SQL until a complete statement (ending in `;`) is typed, run it, repeat."""
    print("Weather database loaded (tables: cities, observations).")
    print("Type SQL ending in ';'. 'quit' or Ctrl+D exits (Ctrl+Z then Enter on Windows).")
    print(f"Bundled queries: {', '.join(query_names())}\n")
    buffer: list[str] = []
    while True:
        try:
            line = input(CONTINUATION_PROMPT if buffer else PROMPT)
        except EOFError:
            print()
            return
        if not buffer and line.strip().lower() in {"quit", "exit"}:
            return
        buffer.append(line)
        statement = "\n".join(buffer)
        if not sqlite3.complete_statement(statement):
            continue
        buffer.clear()
        # sqlite3.Warning is what Python 3.10 raises for "more than one
        # statement"; 3.11+ raises ProgrammingError, a subclass of Error.
        try:
            print_result(conn, statement)
        except (sqlite3.Error, sqlite3.Warning) as error:
            print(f"error: {error}")
        print()


def main() -> None:
    conn = open_database()
    if len(sys.argv) > 1:
        try:
            sql = load_query(sys.argv[1])
        except ValueError as error:
            sys.exit(str(error))
        print(sql)
        print_result(conn, sql)
    else:
        shell(conn)


if __name__ == "__main__":
    main()
