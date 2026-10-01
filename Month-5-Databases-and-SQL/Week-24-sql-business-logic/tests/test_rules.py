"""The business rules in schema.sql, tested with raw SQL that bypasses shop.py.

If these pass, the rules hold no matter which program (or person at a
SQL prompt) writes to the database.
"""

import sqlite3

import pytest

from shop_rules.shop import open_shop


@pytest.fixture
def conn():
    conn = open_shop()
    conn.executescript(
        """
        INSERT INTO products (id, sku, name, price_sek, stock) VALUES
            (1, 'UMB', 'Umbrella', 199, 10),
            (2, 'JKT', 'Rain jacket', 899, 2);
        INSERT INTO orders (id, customer) VALUES (1, 'Alva');
        """
    )
    return conn


def add_line(conn, order_id, product_id, quantity, price=199):
    conn.execute("INSERT INTO order_lines VALUES (?, ?, ?, ?)", (order_id, product_id, quantity, price))


def stock(conn, product_id):
    return conn.execute("SELECT stock FROM products WHERE id = ?", (product_id,)).fetchone()[0]


def set_status(conn, order_id, status):
    conn.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))


class TestStock:
    def test_adding_a_line_takes_stock(self, conn):
        add_line(conn, 1, 1, 3)
        assert stock(conn, 1) == 7

    def test_line_larger_than_stock_is_refused_and_takes_nothing(self, conn):
        with pytest.raises(sqlite3.IntegrityError, match="not enough stock"):
            add_line(conn, 1, 2, 3, price=899)
        assert stock(conn, 2) == 2
        assert conn.execute("SELECT COUNT(*) FROM order_lines").fetchone()[0] == 0

    def test_taking_exactly_the_last_units_is_allowed(self, conn):
        add_line(conn, 1, 2, 2, price=899)
        assert stock(conn, 2) == 0

    def test_check_constraint_backs_up_the_trigger(self, conn):
        with pytest.raises(sqlite3.IntegrityError, match="CHECK"):
            conn.execute("UPDATE products SET stock = -1 WHERE id = 1")

    def test_cancelling_returns_every_line_to_stock(self, conn):
        add_line(conn, 1, 1, 4)
        add_line(conn, 1, 2, 1, price=899)
        set_status(conn, 1, "cancelled")
        assert (stock(conn, 1), stock(conn, 2)) == (10, 2)

    def test_cancelling_leaves_other_products_alone(self, conn):
        conn.execute("INSERT INTO orders (id, customer) VALUES (2, 'Bo')")
        add_line(conn, 1, 1, 4)
        add_line(conn, 2, 2, 1, price=899)
        set_status(conn, 1, "cancelled")
        assert (stock(conn, 1), stock(conn, 2)) == (10, 1)


class TestOrderLines:
    def test_lines_can_only_be_added_to_open_orders(self, conn):
        add_line(conn, 1, 1, 1)
        set_status(conn, 1, "paid")
        with pytest.raises(sqlite3.IntegrityError, match="order is not open"):
            add_line(conn, 1, 2, 1, price=899)

    def test_lines_cannot_be_edited(self, conn):
        add_line(conn, 1, 1, 1)
        with pytest.raises(sqlite3.IntegrityError, match="cannot be changed"):
            conn.execute("UPDATE order_lines SET quantity = 100")

    def test_lines_cannot_be_deleted(self, conn):
        add_line(conn, 1, 1, 1)
        with pytest.raises(sqlite3.IntegrityError, match="cannot be deleted"):
            conn.execute("DELETE FROM order_lines")

    def test_line_for_missing_order_is_a_foreign_key_error(self, conn):
        with pytest.raises(sqlite3.IntegrityError, match="FOREIGN KEY"):
            add_line(conn, 99, 1, 1)


class TestStatusFlow:
    @pytest.mark.parametrize(
        "path",
        [["paid", "shipped"], ["cancelled"]],
    )
    def test_allowed_paths(self, conn, path):
        add_line(conn, 1, 1, 1)
        for status in path:
            set_status(conn, 1, status)
        assert conn.execute("SELECT status FROM orders WHERE id = 1").fetchone()[0] == path[-1]

    @pytest.mark.parametrize(
        "path, refused",
        [
            ([], "shipped"),               # can't skip paying
            (["paid"], "cancelled"),       # paid orders are refunded, not cancelled
            (["paid"], "open"),            # never backwards
            (["paid", "shipped"], "paid"),
            (["cancelled"], "open"),
            (["cancelled"], "paid"),
        ],
    )
    def test_refused_changes(self, conn, path, refused):
        add_line(conn, 1, 1, 1)
        for status in path:
            set_status(conn, 1, status)
        with pytest.raises(sqlite3.IntegrityError, match="invalid status change"):
            set_status(conn, 1, refused)

    def test_unknown_status_is_refused_by_the_trigger_first(self, conn):
        # BEFORE triggers run before the row's CHECK constraints are tested,
        # so 'lost' is refused as a transition, not as an invalid value.
        with pytest.raises(sqlite3.IntegrityError, match="invalid status change"):
            set_status(conn, 1, "lost")

    def test_empty_order_cannot_be_paid(self, conn):
        with pytest.raises(sqlite3.IntegrityError, match="empty order"):
            set_status(conn, 1, "paid")

    def test_empty_order_can_still_be_cancelled(self, conn):
        set_status(conn, 1, "cancelled")


class TestPriceHistory:
    def test_every_change_is_recorded_in_order(self, conn):
        conn.execute("UPDATE products SET price_sek = 249 WHERE id = 1")
        conn.execute("UPDATE products SET price_sek = 229 WHERE id = 1")
        rows = conn.execute("SELECT old_price_sek, new_price_sek FROM price_history ORDER BY id").fetchall()
        assert [tuple(row) for row in rows] == [(199, 249), (249, 229)]

    def test_update_to_the_same_price_is_not_a_change(self, conn):
        conn.execute("UPDATE products SET price_sek = 199 WHERE id = 1")
        assert conn.execute("SELECT COUNT(*) FROM price_history").fetchone()[0] == 0

    def test_other_updates_are_not_logged(self, conn):
        conn.execute("UPDATE products SET stock = 50 WHERE id = 1")
        assert conn.execute("SELECT COUNT(*) FROM price_history").fetchone()[0] == 0


class TestViews:
    def total(self, conn, order_id=1):
        return tuple(conn.execute("SELECT * FROM order_totals WHERE order_id = ?", (order_id,)).fetchone())

    def test_no_discount_below_1000(self, conn):
        add_line(conn, 1, 1, 5)  # 995 SEK
        assert self.total(conn) == (1, "Alva", "open", 5, 995.0, 0.0, 995.0)

    def test_ten_percent_off_from_1000(self, conn):
        add_line(conn, 1, 2, 1, price=899)
        add_line(conn, 1, 1, 1)  # 1098 SEK
        assert self.total(conn) == (1, "Alva", "open", 2, 1098.0, 109.8, 988.2)

    def test_discount_applies_at_exactly_1000(self, conn):
        add_line(conn, 1, 1, 4, price=250)
        assert self.total(conn)[5:] == (100.0, 900.0)

    def test_empty_order_totals_zero(self, conn):
        assert self.total(conn) == (1, "Alva", "open", 0, 0.0, 0.0, 0.0)

    def test_low_stock_lists_products_under_five(self, conn):
        rows = conn.execute("SELECT sku, stock FROM low_stock").fetchall()
        assert [tuple(row) for row in rows] == [("JKT", 2)]


def test_opening_twice_is_harmless(tmp_path):
    path = tmp_path / "shop.db"
    first = open_shop(path)
    with first:
        first.execute("INSERT INTO products (sku, name, price_sek, stock) VALUES ('UMB', 'Umbrella', 199, 1)")
    first.close()
    assert open_shop(path).execute("SELECT COUNT(*) FROM products").fetchone()[0] == 1
