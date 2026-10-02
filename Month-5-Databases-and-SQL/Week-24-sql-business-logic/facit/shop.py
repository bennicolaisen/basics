"""Facit vecka 24: veckans shop.py för facit-schemat. Se FACIT.md.

Det mesta återanvänds från shop_rules.shop; reglerna sitter fortfarande i
schemat. Här finns bara det som är nytt: återbetalning, kunder och
fakturor, lagerrörelser, och en leveransfunktion som går via rörelserna.
"""

import sqlite3
from pathlib import Path

from shop_rules.shop import (  # noqa: F401  (används härifrån av tester och demo)
    _set_status,
    cancel,
    change_price,
    low_stock,
    order_total,
    pay,
    place_order,
    price_history,
    ship,
    stock,
)

FACIT_DIR = Path(__file__).parent
SCHEMA_SQL = FACIT_DIR / "schema.sql"
STOCK_CHECK_SQL = FACIT_DIR / "stock_check.sql"


def open_shop(path: str | Path = ":memory:") -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA_SQL.read_text(encoding="utf-8"))
    return conn


def receive_delivery(conn: sqlite3.Connection, sku: str, name: str, price_sek: float, quantity: int) -> None:
    """Uppgift 3: skapa produkten vid behov (med tomt lager) och logga leveransen som en rörelse."""
    with conn:
        conn.execute(
            "INSERT INTO products (sku, name, price_sek) VALUES (?, ?, ?) ON CONFLICT (sku) DO NOTHING",
            (sku, name, price_sek),
        )
        conn.execute(
            """
            INSERT INTO stock_movements (product_id, change, reason)
            SELECT id, ?, 'delivery' FROM products WHERE sku = ?
            """,
            (quantity, sku),
        )


def refund(conn: sqlite3.Connection, order_id: int) -> None:
    """Uppgift 1: en betald men inte skickad order återbetalas; varorna går tillbaka."""
    _set_status(conn, order_id, "refunded")


def add_customer(conn: sqlite3.Connection, name: str, credit_limit_sek: float) -> None:
    """Uppgift 2: lägg till en kund, eller ändra gränsen för en som redan finns."""
    with conn:
        conn.execute(
            """
            INSERT INTO customers (name, credit_limit_sek) VALUES (?, ?)
            ON CONFLICT (name) DO UPDATE SET credit_limit_sek = excluded.credit_limit_sek
            """,
            (name, credit_limit_sek),
        )


def invoice(conn: sqlite3.Connection, order_id: int) -> None:
    """Uppgift 2: skicka ordern före betalning, mot faktura (inom kreditgränsen)."""
    _set_status(conn, order_id, "invoiced")


def settle_invoice(conn: sqlite3.Connection, order_id: int) -> None:
    """Uppgift 2: fakturan är betald; ordern är klar."""
    _set_status(conn, order_id, "shipped")


def unpaid_invoices(conn: sqlite3.Connection, customer: str) -> float:
    row = conn.execute(
        "SELECT unpaid_invoices_sek FROM customer_credit WHERE customer = ?", (customer,)
    ).fetchone()
    return 0.0 if row is None else row["unpaid_invoices_sek"]


def stock_movements(conn: sqlite3.Connection, sku: str) -> list[tuple[int, str]]:
    """Uppgift 3: varje lagerrörelse för en produkt, äldst först, som (ändring, orsak)."""
    rows = conn.execute(
        """
        SELECT m.change, m.reason
        FROM stock_movements AS m
        JOIN products AS p ON p.id = m.product_id
        WHERE p.sku = ?
        ORDER BY m.id
        """,
        (sku,),
    ).fetchall()
    return [tuple(row) for row in rows]


def stock_check(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    """Uppgift 3: lagret jämfört med summan av rörelserna, en rad per produkt."""
    return conn.execute(STOCK_CHECK_SQL.read_text(encoding="utf-8")).fetchall()
