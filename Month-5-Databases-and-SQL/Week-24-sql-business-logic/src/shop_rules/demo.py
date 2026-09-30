"""A guided run through a day at the shop, showing each business rule at work.

    python -m shop_rules.demo

Each step prints what's being tried and what the database answered. The
steps that fail are meant to: they're the rules in `schema.sql`
refusing something the business doesn't allow.
"""

import sqlite3

from shop_rules import shop


def attempt(description: str, action) -> None:
    print(f"- {description}")
    try:
        result = action()
    except (ValueError, sqlite3.IntegrityError) as error:
        print(f"    refused: {error}")
    else:
        print("    ok" if result is None else f"    ok: {result}")


def show_order(conn: sqlite3.Connection, order_id: int) -> None:
    row = shop.order_total(conn, order_id)
    print(
        f"    order {row['order_id']} ({row['customer']}, {row['status']}): {row['items']} items, "
        f"subtotal {row['subtotal_sek']:.2f}, discount {row['discount_sek']:.2f}, total {row['total_sek']:.2f} SEK"
    )


def main() -> None:
    conn = shop.open_shop()

    print("Morning delivery")
    attempt("receive 10 umbrellas", lambda: shop.receive_delivery(conn, "UMB", "Umbrella", 199.0, 10))
    attempt("receive 4 rain jackets", lambda: shop.receive_delivery(conn, "JKT", "Rain jacket", 899.0, 4))
    attempt("receive 5 more umbrellas (same SKU: upsert adds to stock)",
            lambda: shop.receive_delivery(conn, "UMB", "Umbrella", 199.0, 5))
    print(f"    umbrellas in stock: {shop.stock(conn, 'UMB')}")

    print("\nAlva orders a jacket and two umbrellas")
    alva = shop.place_order(conn, "Alva", {"JKT": 1, "UMB": 2})
    show_order(conn, alva)
    print(f"    jackets left: {shop.stock(conn, 'JKT')} (the trigger took them from stock)")

    print("\nThe price of jackets goes up")
    attempt("change jacket price to 999", lambda: shop.change_price(conn, "JKT", 999.0))
    print(f"    price history: {shop.price_history(conn, 'JKT')}")
    show_order(conn, alva)
    print("    (Alva's order keeps the price she ordered at)")

    print("\nBo tries to buy more jackets than there are")
    attempt("order 5 jackets and 1 umbrella", lambda: shop.place_order(conn, "Bo", {"UMB": 1, "JKT": 5}))
    print(f"    umbrellas in stock: {shop.stock(conn, 'UMB')} (the umbrella line was rolled back too)")

    print("\nAlva's order moves through its states")
    attempt("ship before paying", lambda: shop.ship(conn, alva))
    attempt("pay", lambda: shop.pay(conn, alva))
    attempt("cancel after paying", lambda: shop.cancel(conn, alva))
    attempt("ship", lambda: shop.ship(conn, alva))
    attempt("add another line to the shipped order",
            lambda: conn.execute("INSERT INTO order_lines VALUES (?, 1, 1, 199.0)", (alva,)))

    print("\nCyril orders, then changes his mind")
    cyril = shop.place_order(conn, "Cyril", {"UMB": 3})
    print(f"    umbrellas in stock: {shop.stock(conn, 'UMB')}")
    attempt("cancel", lambda: shop.cancel(conn, cyril))
    print(f"    umbrellas in stock: {shop.stock(conn, 'UMB')} (the trigger put them back)")

    print("\nEnd of day")
    print(f"    low stock: {[(row['sku'], row['stock']) for row in shop.low_stock(conn)]}")


if __name__ == "__main__":
    main()
