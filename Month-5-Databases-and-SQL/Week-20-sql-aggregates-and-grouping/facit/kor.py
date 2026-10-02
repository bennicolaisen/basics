"""Kör facit-frågorna mot veckans databas och visa resultaten.

    python3 facit/kor.py          # alla facit-filer
    python3 facit/kor.py u2       # bara de som börjar med u2

Varje fil får en ny databas i minnet, precis som veckans egna frågor. En
fil kan innehålla flera satser (till exempel CREATE TABLE, INSERT och sist
en SELECT); de körs i ordning och resultatet av den sista visas.
"""

import sqlite3
import sys
from pathlib import Path

FACIT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(FACIT_DIR.parent / "src"))

from aggregates.runner import format_table, open_database, run_query  # noqa: E402


def facit_files(prefix: str = "") -> list[Path]:
    return sorted(path for path in FACIT_DIR.glob("*.sql") if path.stem.startswith(prefix))


def statements(sql: str) -> list[str]:
    """Dela upp SQL-text i hela satser (var och en slutar med ;)."""
    result: list[str] = []
    buffer: list[str] = []
    for line in sql.splitlines():
        buffer.append(line)
        text = "\n".join(buffer)
        if sqlite3.complete_statement(text):
            result.append(text)
            buffer.clear()
    leftover = [line for line in buffer if line.strip() and not line.strip().startswith("--")]
    if leftover:
        result.append("\n".join(buffer))
    return result


def run_file(path: Path) -> tuple[list[str], list[tuple]]:
    """Kör alla satser i filen mot en ny databas; returnera resultatet av den sista."""
    conn = open_database()
    *setup, last = statements(path.read_text(encoding="utf-8"))
    for statement in setup:
        conn.execute(statement)
    return run_query(conn, last)


def main(argv: list[str]) -> None:
    prefix = argv[1] if len(argv) > 1 else ""
    files = facit_files(prefix)
    if not files:
        sys.exit(f"ingen facit-fil börjar med {prefix!r}")
    for path in files:
        print(f"== {path.name}")
        print(path.read_text(encoding="utf-8").strip())
        print()
        columns, rows = run_file(path)
        print(format_table(columns, rows) if columns else "OK")
        print()


if __name__ == "__main__":
    main(sys.argv)
