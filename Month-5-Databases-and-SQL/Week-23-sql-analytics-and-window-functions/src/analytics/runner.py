"""Load the bundled weather database and run this week's `.sql` files.

The SQL itself lives in `queries/*.sql`, not in Python strings, so each
query can be opened, read, and run in any SQL tool on its own. This
module is only the plumbing that gets those files to SQLite and the
results back.
"""

import sqlite3
from pathlib import Path

PACKAGE_DIR = Path(__file__).parent
DATA_SQL = PACKAGE_DIR / "data" / "weather_shop.sql"
QUERIES_DIR = PACKAGE_DIR / "queries"


def open_database() -> sqlite3.Connection:
    """A fresh in-memory database holding the bundled weather data.

    In-memory means nothing is written to disk and every call starts from
    the same known state, so experimenting (even `DELETE FROM cities;`)
    can never break the next run or the tests.
    """
    conn = sqlite3.connect(":memory:")
    conn.executescript(DATA_SQL.read_text(encoding="utf-8"))
    return conn


def query_names() -> list[str]:
    """The name (file stem) of every bundled query, in order."""
    return sorted(path.stem for path in QUERIES_DIR.glob("*.sql"))


def load_query(name: str) -> str:
    """The SQL text of the bundled query called `name` (e.g. `"q04_wet_days"`)."""
    path = QUERIES_DIR / f"{name}.sql"
    if not path.is_file():
        raise ValueError(f"no query named {name!r}; choose one of: {', '.join(query_names())}")
    return path.read_text(encoding="utf-8")


def run_query(conn: sqlite3.Connection, sql: str) -> tuple[list[str], list[tuple]]:
    """Run one SQL statement and return `(column_names, rows)`.

    Statements that don't produce rows (`INSERT`, `UPDATE`, ...) return
    `([], [])`.
    """
    cursor = conn.execute(sql)
    if cursor.description is None:
        return [], []
    columns = [description[0] for description in cursor.description]
    return columns, cursor.fetchall()


def format_table(columns: list[str], rows: list[tuple]) -> str:
    """Render a query result as a fixed-width text table.

    `None` is shown as `NULL`, the way SQL itself talks about a missing
    value, so it can't be mistaken for the text `'None'`.
    """
    cells = [["NULL" if value is None else str(value) for value in row] for row in rows]
    widths = [max(len(text) for text in column) for column in zip(columns, *cells)]
    lines = [
        "  ".join(name.ljust(width) for name, width in zip(columns, widths)),
        "  ".join("-" * width for width in widths),
    ]
    lines += ["  ".join(text.ljust(width) for text, width in zip(row, widths)) for row in cells]
    lines.append(f"({len(rows)} row{'' if len(rows) == 1 else 's'})")
    return "\n".join(line.rstrip() for line in lines)
