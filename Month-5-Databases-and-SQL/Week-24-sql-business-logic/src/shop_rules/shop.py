"""The shop's operations, as small functions over a connection.

Notice what this module does *not* contain: no stock arithmetic, no
status checks, no discount calculation, no audit logging. Those rules
live in `schema.sql` as constraints, triggers and views, so they hold
for any program that writes to the database. The Python side only
translates requests into SQL, groups related writes into transactions,
and turns "nothing matched" into a clear error.
"""

import sqlite3
from pathlib import Path

SCHEMA_SQL = Path(__file__).parent / "schema.sql"


def open_shop(path: str | Path = ":memory:") -> sqlite3.Connection:
    """Open (or create) a shop database with all its tables, triggers and views."""
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA_SQL.read_text(encoding="utf-8"))
    return conn


def receive_delivery(conn: sqlite3.Connection, sku: str, name: str, price_sek: float, quantity: int) -> None:
    """Add `quantity` units to stock, creating the product if the SKU is new.

    For a product that already exists, only the stock changes: `name` and
    `price_sek` are used for new products only (prices change through
    `change_price`, so that the change is recorded).
    """
    with conn:
        conn.execute(
            """
            INSERT INTO products (sku, name, price_sek, stock)
            VALUES (:sku, :name, :price_sek, :quantity)
            ON CONFLICT (sku) DO UPDATE SET stock = stock + excluded.stock
            """,
            {"sku": sku, "name": name, "price_sek": price_sek, "quantity": quantity},
        )


def change_price(conn: sqlite3.Connection, sku: str, price_sek: float) -> None:
    with conn:
        cursor = conn.execute("UPDATE products SET price_sek = ? WHERE sku = ?", (price_sek, sku))
        if cursor.rowcount == 0:
            raise ValueError(f"unknown product: {sku!r}")


def place_order(conn: sqlite3.Connection, customer: str, items: dict[str, int]) -> int:
    """Create an order with one line per `sku: quantity`, and return its id.

    All or nothing: if any line is rejected (unknown SKU, not enough
    stock), the order and every line before it are rolled back, and no
    stock is taken.
    """
    if not items:
        raise ValueError("an order needs at least one item")
    with conn:
        order_id = conn.execute("INSERT INTO orders (customer) VALUES (?)", (customer,)).lastrowid
        for sku, quantity in items.items():
            # Copying price_sek into the line is what freezes the price (rule 3).
            cursor = conn.execute(
                """
                INSERT INTO order_lines (order_id, product_id, quantity, unit_price_sek)
                SELECT :order_id, id, :quantity, price_sek
                FROM products
                WHERE sku = :sku
                """,
                {"order_id": order_id, "quantity": quantity, "sku": sku},
            )
            if cursor.rowcount == 0:
                raise ValueError(f"unknown product: {sku!r}")
    return order_id


def _set_status(conn: sqlite3.Connection, order_id: int, status: str) -> None:
    with conn:
        cursor = conn.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
        if cursor.rowcount == 0:
            raise ValueError(f"unknown order: {order_id}")


def pay(conn: sqlite3.Connection, order_id: int) -> None:
    _set_status(conn, order_id, "paid")


def ship(conn: sqlite3.Connection, order_id: int) -> None:
    _set_status(conn, order_id, "shipped")


def cancel(conn: sqlite3.Connection, order_id: int) -> None:
    _set_status(conn, order_id, "cancelled")


def order_total(conn: sqlite3.Connection, order_id: int) -> sqlite3.Row:
    row = conn.execute("SELECT * FROM order_totals WHERE order_id = ?", (order_id,)).fetchone()
    if row is None:
        raise ValueError(f"unknown order: {order_id}")
    return row


def stock(conn: sqlite3.Connection, sku: str) -> int:
    row = conn.execute("SELECT stock FROM products WHERE sku = ?", (sku,)).fetchone()
    if row is None:
        raise ValueError(f"unknown product: {sku!r}")
    return row["stock"]


def low_stock(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute("SELECT * FROM low_stock ORDER BY stock, sku").fetchall()


def price_history(conn: sqlite3.Connection, sku: str) -> list[tuple[float, float]]:
    """Every price change for `sku`, oldest first, as (old, new) pairs."""
    rows = conn.execute(
        """
        SELECT h.old_price_sek, h.new_price_sek
        FROM price_history AS h
        JOIN products AS p ON p.id = h.product_id
        WHERE p.sku = ?
        ORDER BY h.id
        """,
        (sku,),
    ).fetchall()
    return [tuple(row) for row in rows]
