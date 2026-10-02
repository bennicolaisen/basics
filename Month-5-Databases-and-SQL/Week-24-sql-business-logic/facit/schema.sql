-- Facit vecka 24: veckans schema med Try It Yourself 1-4 gjorda.
-- Ändringar mot src/shop_rules/schema.sql är märkta med "Uppgift N".
--
--   1. Stock can never go negative: an order can't take more than is on the shelf.
--   2. Placing an order takes its items out of stock; cancelling or refunding puts them back.
--   3. A line's price is the price when the order was placed, whatever happens later.
--   4. Orders move through the allowed statuses only (see orders_status_flow), never backwards.
--   5. Only open orders can get new lines; lines are never edited or deleted.
--   6. An empty order can't be paid for or invoiced.
--   7. Every price change is recorded in price_history.
--   8. Orders get 10% off from 1,000 SEK and 15% off from 2,500 SEK (order_totals view).
--   9. Uppgift 2: an order can only be invoiced (shipped before payment) if the customer's
--      unpaid invoices plus this order stay within their credit limit.
--  10. Uppgift 3: every change to products.stock is a row in stock_movements, with a reason.

CREATE TABLE IF NOT EXISTS products (
    id         INTEGER PRIMARY KEY,
    sku        TEXT    NOT NULL UNIQUE,
    name       TEXT    NOT NULL,
    price_sek  REAL    NOT NULL CHECK (price_sek > 0),
    stock      INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0)
);

CREATE TABLE IF NOT EXISTS price_history (
    id             INTEGER PRIMARY KEY,
    product_id     INTEGER NOT NULL REFERENCES products (id),
    old_price_sek  REAL    NOT NULL,
    new_price_sek  REAL    NOT NULL
);

-- Uppgift 2: kunder med en kreditgräns. En kund som saknas här har gränsen 0.
CREATE TABLE IF NOT EXISTS customers (
    name              TEXT PRIMARY KEY,
    credit_limit_sek  REAL NOT NULL CHECK (credit_limit_sek >= 0)
);

CREATE TABLE IF NOT EXISTS orders (
    id        INTEGER PRIMARY KEY,
    customer  TEXT    NOT NULL,
    status    TEXT    NOT NULL DEFAULT 'open'
                      -- Uppgift 1: 'refunded'. Uppgift 2: 'invoiced'.
                      CHECK (status IN ('open', 'paid', 'invoiced', 'shipped', 'cancelled', 'refunded'))
);

CREATE TABLE IF NOT EXISTS order_lines (
    order_id        INTEGER NOT NULL REFERENCES orders (id),
    product_id      INTEGER NOT NULL REFERENCES products (id),
    quantity        INTEGER NOT NULL CHECK (quantity > 0),
    unit_price_sek  REAL    NOT NULL,
    PRIMARY KEY (order_id, product_id)
);

-- Uppgift 3: lagerrörelser. Lagret i products är summan av dessa rader.
CREATE TABLE IF NOT EXISTS stock_movements (
    id          INTEGER PRIMARY KEY,
    product_id  INTEGER NOT NULL REFERENCES products (id),
    change      INTEGER NOT NULL CHECK (change <> 0),
    reason      TEXT    NOT NULL CHECK (reason IN ('delivery', 'order', 'cancellation', 'refund'))
);

-- Uppgift 3: varje rörelse ändrar lagret. Det är det ENDA stället som gör det.
CREATE TRIGGER IF NOT EXISTS stock_movements_change_stock
AFTER INSERT ON stock_movements
BEGIN
    UPDATE products SET stock = stock + NEW.change WHERE id = NEW.product_id;
END;

-- Uppgift 3: en ny produkt börjar med tomt lager; varorna kommer in som en leverans.
CREATE TRIGGER IF NOT EXISTS products_start_empty
BEFORE INSERT ON products
WHEN NEW.stock <> 0
BEGIN
    SELECT RAISE(ABORT, 'new products start with stock 0; record a delivery instead');
END;

-- Uppgift 3: en ändring av lagret som inte kommer från en rörelse stoppas.
CREATE TRIGGER IF NOT EXISTS products_stock_matches_movements
AFTER UPDATE OF stock ON products
WHEN NEW.stock <> (SELECT COALESCE(SUM(change), 0) FROM stock_movements WHERE product_id = NEW.id)
BEGIN
    SELECT RAISE(ABORT, 'stock can only change through stock_movements');
END;

CREATE TRIGGER IF NOT EXISTS order_lines_need_stock
BEFORE INSERT ON order_lines
WHEN NEW.quantity > (SELECT stock FROM products WHERE id = NEW.product_id)
BEGIN
    SELECT RAISE(ABORT, 'not enough stock');
END;

-- Regel 2, första halvan. Uppgift 3: via en rörelse i stället för direkt.
CREATE TRIGGER IF NOT EXISTS order_lines_take_stock
AFTER INSERT ON order_lines
BEGIN
    INSERT INTO stock_movements (product_id, change, reason)
    VALUES (NEW.product_id, -NEW.quantity, 'order');
END;

CREATE TRIGGER IF NOT EXISTS order_lines_only_on_open_orders
BEFORE INSERT ON order_lines
WHEN (SELECT status FROM orders WHERE id = NEW.order_id) <> 'open'
BEGIN
    SELECT RAISE(ABORT, 'order is not open');
END;

CREATE TRIGGER IF NOT EXISTS order_lines_are_not_edited
BEFORE UPDATE ON order_lines
BEGIN
    SELECT RAISE(ABORT, 'order lines cannot be changed; cancel the order instead');
END;

CREATE TRIGGER IF NOT EXISTS order_lines_are_not_deleted
BEFORE DELETE ON order_lines
BEGIN
    SELECT RAISE(ABORT, 'order lines cannot be deleted; cancel the order instead');
END;

-- Regel 4, med de nya pilarna från uppgift 1 och 2.
--
--   open ──► paid ──► shipped
--    │        │          ▲
--    │        └─► refunded
--    ├──► invoiced ──────┘   (skickad mot faktura; 'shipped' när fakturan är betald)
--    └──► cancelled
CREATE TRIGGER IF NOT EXISTS orders_status_flow
BEFORE UPDATE OF status ON orders
WHEN NOT (
       NEW.status = OLD.status
    OR (OLD.status = 'open'     AND NEW.status IN ('paid', 'invoiced', 'cancelled'))
    OR (OLD.status = 'paid'     AND NEW.status IN ('shipped', 'refunded'))
    OR (OLD.status = 'invoiced' AND NEW.status = 'shipped')
)
BEGIN
    SELECT RAISE(ABORT, 'invalid status change');
END;

-- Regel 6, nu även för fakturering.
CREATE TRIGGER IF NOT EXISTS orders_pay_needs_lines
BEFORE UPDATE OF status ON orders
WHEN NEW.status IN ('paid', 'invoiced')
 AND NOT EXISTS (SELECT 1 FROM order_lines WHERE order_id = NEW.id)
BEGIN
    SELECT RAISE(ABORT, 'cannot pay for an empty order');
END;

-- Uppgift 2: kreditgränsen. Obetalda fakturor plus den här ordern får inte
-- överstiga kundens gräns.
CREATE TRIGGER IF NOT EXISTS orders_credit_limit
BEFORE UPDATE OF status ON orders
WHEN NEW.status = 'invoiced' AND OLD.status <> 'invoiced'
 AND (SELECT COALESCE(SUM(total_sek), 0) FROM order_totals
      WHERE customer = NEW.customer AND status = 'invoiced')
   + (SELECT total_sek FROM order_totals WHERE order_id = NEW.id)
   > COALESCE((SELECT credit_limit_sek FROM customers WHERE name = NEW.customer), 0)
BEGIN
    SELECT RAISE(ABORT, 'credit limit exceeded');
END;

-- Regel 2, andra halvan. Uppgift 1: återbetalning lämnar tillbaka varorna
-- precis som en avbokning. Uppgift 3: via rörelser, med rätt orsak.
CREATE TRIGGER IF NOT EXISTS orders_return_stock
AFTER UPDATE OF status ON orders
WHEN NEW.status IN ('cancelled', 'refunded') AND OLD.status NOT IN ('cancelled', 'refunded')
BEGIN
    INSERT INTO stock_movements (product_id, change, reason)
    SELECT product_id,
           quantity,
           CASE NEW.status WHEN 'cancelled' THEN 'cancellation' ELSE 'refund' END
    FROM order_lines
    WHERE order_id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS products_price_history
AFTER UPDATE OF price_sek ON products
WHEN NEW.price_sek <> OLD.price_sek
BEGIN
    INSERT INTO price_history (product_id, old_price_sek, new_price_sek)
    VALUES (NEW.id, OLD.price_sek, NEW.price_sek);
END;

-- Regel 8. Uppgift 4: två rabattnivåer. DROP + CREATE i stället för
-- IF NOT EXISTS, så att en befintlig databas också får den nya regeln.
DROP VIEW IF EXISTS order_totals;
CREATE VIEW order_totals AS
WITH subtotals AS (
    SELECT o.id     AS order_id,
           o.customer,
           o.status,
           COALESCE(SUM(l.quantity), 0)                    AS items,
           COALESCE(SUM(l.quantity * l.unit_price_sek), 0) AS subtotal_sek
    FROM orders AS o
    LEFT JOIN order_lines AS l ON l.order_id = o.id
    GROUP BY o.id, o.customer, o.status
),
discounted AS (
    SELECT *,
           CASE
               WHEN subtotal_sek >= 2500 THEN subtotal_sek * 0.15
               WHEN subtotal_sek >= 1000 THEN subtotal_sek * 0.10
               ELSE 0
           END AS discount_sek
    FROM subtotals
)
SELECT order_id,
       customer,
       status,
       items,
       ROUND(subtotal_sek, 2)                AS subtotal_sek,
       ROUND(discount_sek, 2)                AS discount_sek,
       ROUND(subtotal_sek - discount_sek, 2) AS total_sek
FROM discounted;

CREATE VIEW IF NOT EXISTS low_stock AS
SELECT sku, name, stock
FROM products
WHERE stock < 5;

-- Uppgift 2: vad varje kund är skyldig, bredvid gränsen.
CREATE VIEW IF NOT EXISTS customer_credit AS
SELECT c.name                           AS customer,
       c.credit_limit_sek,
       COALESCE(SUM(t.total_sek), 0)    AS unpaid_invoices_sek
FROM customers AS c
LEFT JOIN order_totals AS t ON t.customer = c.name AND t.status = 'invoiced'
GROUP BY c.name, c.credit_limit_sek;
