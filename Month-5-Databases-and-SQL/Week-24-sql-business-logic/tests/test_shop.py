import sqlite3

import pytest

from shop_rules import shop


@pytest.fixture
def conn():
    conn = shop.open_shop()
    shop.receive_delivery(conn, "UMB", "Umbrella", 199.0, 10)
    shop.receive_delivery(conn, "JKT", "Rain jacket", 899.0, 2)
    return conn


class TestReceiveDelivery:
    def test_new_sku_creates_the_product(self, conn):
        shop.receive_delivery(conn, "SUN", "Sunglasses", 349.0, 6)
        assert shop.stock(conn, "SUN") == 6

    def test_known_sku_adds_to_stock_and_keeps_its_price(self, conn):
        shop.receive_delivery(conn, "UMB", "Umbrella (new name ignored)", 1.0, 5)
        assert shop.stock(conn, "UMB") == 15
        row = conn.execute("SELECT name, price_sek FROM products WHERE sku = 'UMB'").fetchone()
        assert tuple(row) == ("Umbrella", 199.0)


class TestPlaceOrder:
    def test_creates_order_and_takes_stock(self, conn):
        order_id = shop.place_order(conn, "Alva", {"UMB": 2, "JKT": 1})
        assert shop.order_total(conn, order_id)["items"] == 3
        assert (shop.stock(conn, "UMB"), shop.stock(conn, "JKT")) == (8, 1)

    def test_one_failing_line_rolls_back_the_whole_order(self, conn):
        with pytest.raises(sqlite3.IntegrityError, match="not enough stock"):
            shop.place_order(conn, "Bo", {"UMB": 1, "JKT": 3})
        assert shop.stock(conn, "UMB") == 10
        assert conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 0

    def test_unknown_sku_rolls_back_too(self, conn):
        with pytest.raises(ValueError, match="unknown product: 'XYZ'"):
            shop.place_order(conn, "Bo", {"UMB": 1, "XYZ": 1})
        assert conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 0

    def test_empty_order_is_refused_before_touching_the_database(self, conn):
        with pytest.raises(ValueError, match="at least one item"):
            shop.place_order(conn, "Bo", {})

    def test_price_is_frozen_when_ordered(self, conn):
        order_id = shop.place_order(conn, "Alva", {"JKT": 1})
        shop.change_price(conn, "JKT", 999.0)
        assert shop.order_total(conn, order_id)["subtotal_sek"] == 899.0

    def test_discount_comes_from_the_view(self, conn):
        order_id = shop.place_order(conn, "Alva", {"JKT": 1, "UMB": 1})
        total = shop.order_total(conn, order_id)
        assert (total["subtotal_sek"], total["discount_sek"], total["total_sek"]) == (1098.0, 109.8, 988.2)


class TestStatusChanges:
    def test_pay_then_ship(self, conn):
        order_id = shop.place_order(conn, "Alva", {"UMB": 1})
        shop.pay(conn, order_id)
        shop.ship(conn, order_id)
        assert shop.order_total(conn, order_id)["status"] == "shipped"

    def test_database_rule_surfaces_as_integrity_error(self, conn):
        order_id = shop.place_order(conn, "Alva", {"UMB": 1})
        with pytest.raises(sqlite3.IntegrityError, match="invalid status change"):
            shop.ship(conn, order_id)

    def test_cancel_puts_stock_back(self, conn):
        order_id = shop.place_order(conn, "Alva", {"UMB": 4})
        shop.cancel(conn, order_id)
        assert shop.stock(conn, "UMB") == 10

    def test_unknown_order(self, conn):
        with pytest.raises(ValueError, match="unknown order: 42"):
            shop.pay(conn, 42)


class TestReading:
    def test_price_history(self, conn):
        shop.change_price(conn, "UMB", 249.0)
        shop.change_price(conn, "UMB", 229.0)
        assert shop.price_history(conn, "UMB") == [(199.0, 249.0), (249.0, 229.0)]

    def test_change_price_of_unknown_product(self, conn):
        with pytest.raises(ValueError, match="unknown product"):
            shop.change_price(conn, "XYZ", 1.0)

    def test_low_stock_is_sorted_by_stock(self, conn):
        shop.receive_delivery(conn, "SUN", "Sunglasses", 349.0, 4)
        assert [(row["sku"], row["stock"]) for row in shop.low_stock(conn)] == [("JKT", 2), ("SUN", 4)]


def test_demo_runs_start_to_finish(capsys):
    from shop_rules import demo

    demo.main()
    output = capsys.readouterr().out
    assert "refused: not enough stock" in output
    assert "umbrellas in stock: 13 (the trigger put them back)" in output
