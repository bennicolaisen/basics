"""Tester för facit (facit/schema.sql, facit/shop.py). Se FACIT.md."""

import sqlite3

import pytest

from facit import shop


@pytest.fixture
def conn():
    conn = shop.open_shop()
    shop.receive_delivery(conn, "UMB", "Umbrella", 199, 10)
    shop.receive_delivery(conn, "JKT", "Rain jacket", 899, 5)
    return conn


def status(conn, order_id):
    return shop.order_total(conn, order_id)["status"]


class TestRefund:
    def test_paid_order_can_be_refunded_and_returns_stock(self, conn):
        order = shop.place_order(conn, "Alva", {"UMB": 2, "JKT": 1})
        shop.pay(conn, order)
        shop.refund(conn, order)
        assert status(conn, order) == "refunded"
        assert (shop.stock(conn, "UMB"), shop.stock(conn, "JKT")) == (10, 5)

    @pytest.mark.parametrize("before", [[], ["pay", "ship"], ["cancel"]])
    def test_only_paid_orders_can_be_refunded(self, conn, before):
        order = shop.place_order(conn, "Alva", {"UMB": 1})
        for step in before:
            getattr(shop, step)(conn, order)
        with pytest.raises(sqlite3.IntegrityError, match="invalid status change"):
            shop.refund(conn, order)

    def test_refunded_is_final(self, conn):
        order = shop.place_order(conn, "Alva", {"UMB": 1})
        shop.pay(conn, order)
        shop.refund(conn, order)
        for step in (shop.pay, shop.ship, shop.cancel):
            with pytest.raises(sqlite3.IntegrityError):
                step(conn, order)
        assert shop.stock(conn, "UMB") == 10

    def test_refund_does_not_return_stock_twice(self, conn):
        order = shop.place_order(conn, "Alva", {"UMB": 3})
        shop.pay(conn, order)
        shop.refund(conn, order)
        conn.execute("UPDATE orders SET status = 'refunded' WHERE id = ?", (order,))
        assert shop.stock(conn, "UMB") == 10


class TestCreditLimit:
    def test_invoice_within_the_limit(self, conn):
        shop.add_customer(conn, "Firma AB", 2000)
        order = shop.place_order(conn, "Firma AB", {"JKT": 2})  # 1 798 kr, minus 10 % = 1 618,20
        shop.invoice(conn, order)
        assert status(conn, order) == "invoiced"
        assert shop.unpaid_invoices(conn, "Firma AB") == 1618.2

    def test_unpaid_invoices_plus_this_order_may_not_exceed_the_limit(self, conn):
        shop.add_customer(conn, "Firma AB", 2000)
        first = shop.place_order(conn, "Firma AB", {"JKT": 2})
        shop.invoice(conn, first)
        second = shop.place_order(conn, "Firma AB", {"UMB": 2})  # 398 kr; 1 618,20 + 398 > 2 000
        with pytest.raises(sqlite3.IntegrityError, match="credit limit exceeded"):
            shop.invoice(conn, second)
        assert status(conn, second) == "open"

    def test_settled_invoices_free_up_credit(self, conn):
        shop.add_customer(conn, "Firma AB", 2000)
        first = shop.place_order(conn, "Firma AB", {"JKT": 2})
        shop.invoice(conn, first)
        shop.settle_invoice(conn, first)
        assert status(conn, first) == "shipped"
        second = shop.place_order(conn, "Firma AB", {"UMB": 2})
        shop.invoice(conn, second)
        assert shop.unpaid_invoices(conn, "Firma AB") == 398

    def test_exactly_at_the_limit_is_allowed(self, conn):
        shop.add_customer(conn, "Firma AB", 398)
        order = shop.place_order(conn, "Firma AB", {"UMB": 2})
        shop.invoice(conn, order)

    def test_unknown_customer_has_no_credit(self, conn):
        order = shop.place_order(conn, "Alva", {"UMB": 1})
        with pytest.raises(sqlite3.IntegrityError, match="credit limit exceeded"):
            shop.invoice(conn, order)
        shop.pay(conn, order)  # att betala direkt går som vanligt

    def test_paying_up_front_ignores_the_limit(self, conn):
        shop.add_customer(conn, "Firma AB", 0)
        order = shop.place_order(conn, "Firma AB", {"JKT": 5})
        shop.pay(conn, order)
        shop.ship(conn, order)

    def test_empty_order_cannot_be_invoiced(self, conn):
        shop.add_customer(conn, "Firma AB", 1000)
        order = conn.execute("INSERT INTO orders (customer) VALUES ('Firma AB')").lastrowid
        with pytest.raises(sqlite3.IntegrityError, match="empty order"):
            shop.invoice(conn, order)

    def test_invoiced_order_cannot_be_cancelled(self, conn):
        shop.add_customer(conn, "Firma AB", 1000)
        order = shop.place_order(conn, "Firma AB", {"UMB": 1})
        shop.invoice(conn, order)
        with pytest.raises(sqlite3.IntegrityError, match="invalid status change"):
            shop.cancel(conn, order)


class TestStockMovements:
    def test_every_change_is_logged_with_a_reason(self, conn):
        first = shop.place_order(conn, "Alva", {"UMB": 3})
        second = shop.place_order(conn, "Bo", {"UMB": 2})
        shop.cancel(conn, first)
        shop.pay(conn, second)
        shop.refund(conn, second)
        shop.receive_delivery(conn, "UMB", "Umbrella", 199, 4)
        assert shop.stock_movements(conn, "UMB") == [
            (10, "delivery"),
            (-3, "order"),
            (-2, "order"),
            (3, "cancellation"),
            (2, "refund"),
            (4, "delivery"),
        ]
        assert shop.stock(conn, "UMB") == 14

    def test_stock_equals_the_sum_of_its_movements(self, conn):
        order = shop.place_order(conn, "Alva", {"UMB": 3, "JKT": 2})
        shop.pay(conn, order)
        shop.place_order(conn, "Bo", {"JKT": 1})
        rows = shop.stock_check(conn)
        assert [(row["sku"], row["stock"], row["difference"]) for row in rows] == [
            ("JKT", 2, 0),
            ("UMB", 7, 0),
        ]

    def test_a_direct_update_of_stock_is_refused(self, conn):
        with pytest.raises(sqlite3.IntegrityError, match="stock_movements"):
            conn.execute("UPDATE products SET stock = 99 WHERE sku = 'UMB'")
        assert shop.stock(conn, "UMB") == 10

    def test_a_new_product_cannot_start_with_stock(self, conn):
        with pytest.raises(sqlite3.IntegrityError, match="start with stock 0"):
            conn.execute("INSERT INTO products (sku, name, price_sek, stock) VALUES ('X', 'X', 1, 5)")

    def test_a_movement_cannot_make_stock_negative(self, conn):
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO stock_movements (product_id, change, reason)"
                " SELECT id, -11, 'order' FROM products WHERE sku = 'UMB'"
            )
        assert shop.stock(conn, "UMB") == 10
        assert len(shop.stock_movements(conn, "UMB")) == 1

    def test_not_enough_stock_still_has_the_friendly_message(self, conn):
        with pytest.raises(sqlite3.IntegrityError, match="not enough stock"):
            shop.place_order(conn, "Alva", {"JKT": 6})
        assert shop.stock_movements(conn, "JKT") == [(5, "delivery")]


class TestDiscountTiers:
    @pytest.mark.parametrize(
        ("items", "subtotal", "discount"),
        [
            ({"UMB": 5}, 995.0, 0.0),
            ({"JKT": 1, "UMB": 1}, 1098.0, 109.8),
            ({"JKT": 2, "UMB": 4}, 2594.0, 389.1),
        ],
    )
    def test_ten_and_fifteen_percent(self, conn, items, subtotal, discount):
        order = shop.place_order(conn, "Alva", items)
        row = shop.order_total(conn, order)
        assert (row["subtotal_sek"], row["discount_sek"]) == (subtotal, discount)
        assert row["total_sek"] == round(subtotal - discount, 2)

    def test_fifteen_percent_starts_at_exactly_2500(self, conn):
        shop.change_price(conn, "UMB", 250)
        order = shop.place_order(conn, "Alva", {"UMB": 10})
        assert shop.order_total(conn, order)["discount_sek"] == 375.0

    def test_reopening_an_old_database_updates_the_view(self, tmp_path):
        from shop_rules.shop import open_shop as open_original

        path = tmp_path / "shop.db"
        old = open_original(path)
        old.execute("INSERT INTO products (sku, name, price_sek, stock) VALUES ('BIG', 'Big', 2500, 1)")
        old.execute("INSERT INTO orders (customer) VALUES ('Alva')")
        old.execute("INSERT INTO order_lines VALUES (1, 1, 1, 2500)")
        old.commit()
        assert old.execute("SELECT discount_sek FROM order_totals").fetchone()[0] == 250
        old.close()
        new = shop.open_shop(path)
        assert new.execute("SELECT discount_sek FROM order_totals").fetchone()[0] == 375
