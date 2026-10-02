# Week 24 — SQL Level 3 (Advanced): Business Logic in the Database

## Purpose

Business logic is the set of rules that make data mean something to the
business: you can't sell what isn't on the shelf, a shipped order can't
be cancelled, a price on an invoice doesn't change when the price list
does, big orders get a discount. Week 22 put simple validity rules in the
schema (no negative rain). This week goes further and puts the shop's
*behavior* there too: stock that updates itself when an order is placed,
orders that can only move through allowed states, an audit trail of
every price change, and a discount that every program computes the same
way because it's defined once. The project is the order system for the
weather-gear shop from Week 23. It finishes Level 3, and the SQL track.

## Objectives

The code in this project concretely demonstrates:

- Turning written business rules into database rules, and deciding which
  kind of rule fits each: a constraint, a trigger, or a view.
- Triggers: `BEFORE` and `AFTER`, `INSERT`/`UPDATE`/`DELETE`, the `OLD`
  and `NEW` rows, a `WHEN` condition, and `RAISE(ABORT, ...)` to refuse a
  change with a readable message.
- Keeping derived data correct automatically (stock goes down when an
  order line is added and back up when the order is cancelled).
- A state machine for order status enforced by the database.
- An audit trail (`price_history`) that no program can forget to write.
- Views as the single definition of a calculation (`order_totals`).
- Freezing historical values: copying the price onto the order line.
- Upserts with `INSERT ... ON CONFLICT ... DO UPDATE` and `excluded`.
- Multi-statement business operations as one transaction (an order and
  all its lines, or nothing).

## Concepts Refresher

### Where should business rules live?

Every rule could be written in Python instead: check stock before
inserting a line, subtract it afterwards, check the status before
changing it. The trouble is that the Python check only protects the
Python path. A second program, a quick fix typed at a SQL prompt, a
rewrite next year, or a bug in one function that forgets the check, and
the rule is broken, and the data now contradicts the business. A rule in
the database can't be skipped, because every write goes through the
database.

That doesn't mean everything belongs in SQL (see Reflection). A good
default: **rules about what the data may look like, and what must always
happen together, go in the database. Rules about workflow, presentation
and user interaction stay in the program.**

The shop's rules are listed at the top of `src/shop_rules/schema.sql`,
each labeled with the number used in the comments below it. Three tools
enforce them:

| Tool | Good for | Used for |
|---|---|---|
| Constraint (`CHECK`, `UNIQUE`, `FOREIGN KEY`) | what one row may contain | stock ≥ 0, price > 0, known statuses |
| Trigger | what must happen, or be refused, when data changes | stock updates, status flow, locking lines, audit log |
| View | a calculation everyone must do the same way | order totals and the discount, low stock |

### Triggers

A trigger is SQL the database runs automatically when a row in a table
is inserted, updated, or deleted:

```sql
CREATE TRIGGER order_lines_take_stock
AFTER INSERT ON order_lines
BEGIN
    UPDATE products SET stock = stock - NEW.quantity WHERE id = NEW.product_id;
END;
```

- **`BEFORE` or `AFTER`.** A `BEFORE` trigger runs before the change is
  made, which is the place to refuse it. An `AFTER` trigger runs once the
  change is made, which is the place to update other tables in response.
- **`OLD` and `NEW`** are the row before and after the change. An
  `INSERT` only has `NEW`, a `DELETE` only has `OLD`, an `UPDATE` has
  both. `orders_status_flow` compares `OLD.status` with `NEW.status` to
  decide whether a transition is allowed.
- **`UPDATE OF column`** fires only when that column is in the `UPDATE`'s
  `SET` list, so `products_price_history` ignores stock changes.
- **`WHEN condition`** makes the trigger fire only for some rows.
- **`SELECT RAISE(ABORT, 'message')`** stops the statement: the change
  is undone, and the program receives an error with that message (in
  Python, `sqlite3.IntegrityError`).

Everything a trigger does is part of the statement that fired it. If
the `INSERT` of an order line fails, the stock update its trigger made
is undone with it. And if that `INSERT` is inside a larger transaction
that rolls back, the whole lot rolls back together. That's why
`place_order` can promise all-or-nothing: the order, every line, and
every stock change are one transaction.

Triggers fire in a defined position relative to constraints, which
explains one test: `BEFORE` triggers run before the row's `CHECK`
constraints are tested, so setting an order's status to `'lost'` is
refused by the status-flow trigger ("invalid status change") before the
`CHECK (status IN ...)` ever sees it.

### Derived data that can't drift

`products.stock` is **derived data**: in principle you could compute it
from deliveries minus order lines. Storing it is faster to read, but a
stored copy can drift from the truth if any code path forgets to update
it. Two triggers make the database update it on every path, and the
`CHECK (stock >= 0)` makes a negative stock impossible even if a trigger
has a bug. The `BEFORE INSERT` trigger `order_lines_need_stock` exists
only to replace the check's technical error message ("CHECK constraint
failed: stock >= 0") with one a person understands ("not enough stock").

### State machines

An order's status can only change along certain arrows:

```
open ──► paid ──► shipped
  │
  └────► cancelled
```

`orders_status_flow` lists the allowed arrows and refuses everything
else. Writing it as "what's allowed" rather than "what's forbidden" is
deliberate: a new status added later is refused until someone decides
which arrows lead to and from it, instead of being allowed by default.
`orders_pay_needs_lines` adds a condition to one arrow (an order must
have lines before it's paid), and `orders_cancel_returns_stock` attaches
an action to another.

### History that stays true

Two rules protect the past:

- **Freeze the price on the order line.** `place_order` copies
  `products.price_sek` into `order_lines.unit_price_sek` at the moment the
  line is added (with `INSERT ... SELECT`, so it's the price in the
  database at that instant). A later price change doesn't rewrite what
  Alva agreed to pay. The alternative, joining to `products` whenever you
  need a line's price, silently changes every old order's total whenever
  a price changes. Week 23's `revenue_sek` column is the same idea.
- **Keep an audit trail.** `products_price_history` records every price
  change, old and new. It's a trigger, not a Python function, because the
  whole point of an audit trail is that nobody can forget to write it.

Order lines are locked completely: the triggers refuse any `UPDATE` or
`DELETE` on them. To change an order, you cancel it and place a new one.
That's stricter than many real shops, but it means an order's lines are
a permanent record, and the stock bookkeeping never has to handle an
edited line.

### Views: one definition of a calculation

A view is a named, stored `SELECT` that you query like a table:

```sql
SELECT * FROM order_totals WHERE order_id = 1;
```

`order_totals` computes items, subtotal, the 10% discount on orders of
1,000 SEK or more, and the total. The rule lives in exactly one place.
If the Python code, a reporting tool, and an accountant's spreadsheet
query each recomputed the discount, sooner or later one of them would
use `>` instead of `>=`, and the numbers wouldn't match. Views store no
data: the query runs each time you read from them, so they're always up
to date. (It also means they are only as fast as their query.)

### Upserts

A delivery either adds a new product or tops up an existing one.
"Insert, or update if it already exists" is common enough that SQL has a
statement for it:

```sql
INSERT INTO products (sku, name, price_sek, stock)
VALUES (:sku, :name, :price_sek, :quantity)
ON CONFLICT (sku) DO UPDATE SET stock = stock + excluded.stock;
```

If inserting would violate the `UNIQUE` constraint on `sku`, SQLite runs
the `DO UPDATE` instead. `excluded` is the row that couldn't be
inserted, so `excluded.stock` is the delivered quantity. One statement is
also safer than the Python alternative of a `SELECT` followed by an
`INSERT` or an `UPDATE`: between those two statements, another program
could insert the same SKU. (Upserts need SQLite 3.24 or newer; every
Python 3.10+ has one.)

## Design & Architecture

```
Week-24-sql-business-logic/
├── conftest.py                  - adds src/ to sys.path for pytest
├── src/
│   └── shop_rules/
│       ├── __init__.py
│       ├── schema.sql           - tables, constraints, triggers, views: all the business rules
│       ├── shop.py              - operations: receive_delivery, place_order, pay, ship, cancel, ...
│       └── demo.py              - a scripted day at the shop, printing what each rule does
└── tests/
    ├── test_rules.py            - every rule, tested with raw SQL that bypasses shop.py
    └── test_shop.py             - the Python operations, and a run of the demo
```

The interesting split is between `schema.sql` and `shop.py`. The schema
owns every rule; `shop.py` contains no stock arithmetic, no status checks
and no discount calculation. Its jobs are translating a request into
SQL, grouping the statements of one business operation into one
transaction, and turning "no row matched" into a `ValueError`. Errors
from the rules themselves arrive as `sqlite3.IntegrityError` with the
trigger's message, and `shop.py` lets them through unchanged.

`test_rules.py` is the more important test file: it proves each rule
holds for *any* writer, by writing raw SQL straight at the database.

## How to Build & Run

```bash
cd Month-5-Databases-and-SQL/Week-24-sql-business-logic

# Watch the rules work (and refuse things):
PYTHONPATH=src python3 -m shop_rules.demo
```

On Windows PowerShell: `$env:PYTHONPATH="src"`, then `python -m
shop_rules.demo`.

To try breaking the rules yourself, open a shop in the `sqlite3` shell or
DB Browser for SQLite (both enforce triggers and views; remember
`PRAGMA foreign_keys = ON;` for the foreign keys):

```bash
python3 -c "import sys; sys.path.insert(0, 'src'); from shop_rules.shop import open_shop; open_shop('shop.db').close()"
```

## Testing

```bash
cd Month-5-Databases-and-SQL/Week-24-sql-business-logic
python3 -m pytest -q
```

`test_rules.py` covers every rule with raw SQL: stock taken on insert,
refused when short (with nothing taken), allowed down to exactly 0, the
`CHECK` behind the trigger, and returned on cancel (only for that order's
products); lines only on open orders, never edited or deleted; every
allowed and six refused status changes, including why an unknown status
gets the trigger's message rather than the `CHECK`'s; paying an empty
order; price history recording real changes only; the discount below,
above, and at exactly 1,000 SEK; and reopening a database file.
`test_shop.py` covers the Python operations: the upsert keeping an
existing product's name and price, all-or-nothing orders (a short line
or an unknown SKU rolls back the whole order), the frozen price, and a
full run of the demo.

## Try It Yourself

> **Facit (answer key):** every exercise below is solved, tested and explained
> in Swedish in [FACIT.md](FACIT.md). Try each one yourself first, then compare.

1. Add a `refunded` status: a paid (but not shipped) order can be
   refunded, which returns its stock like a cancellation. Update the
   state diagram, the triggers, and the tests. Which existing trigger
   needs the smallest change?
2. Add a `customers` table with a credit limit, and a rule that an order
   can't be paid if the customer's unpaid-but-shipped orders plus this
   one exceed the limit. Is this a constraint, a trigger, or a view?
3. Add a `stock_movements` table (product, change, reason) and triggers
   so that every change to `products.stock` is logged with a reason
   ('delivery', 'order', 'cancellation'). Then write a query that proves
   `stock` equals the sum of its movements for every product.
4. Change the discount to "10% off orders of 1,000 SEK or more, 15% off
   from 2,500 SEK". How many files do you have to touch? Compare that
   with how many you'd touch if the discount were computed in Python in
   three different places.
5. Write down one rule of the shop that should *not* be in the database,
   and explain why.

## Reflection

**The cost of rules in the database.** Triggers are invisible from the
calling code: reading `place_order`, nothing says that stock changes. A
developer who doesn't know the schema can be surprised, which is why the
rules are listed at the top of `schema.sql` and why the module docstring
of `shop.py` says what it doesn't do. Trigger logic is also harder to
debug than Python, and SQL dialects differ, so moving from SQLite to
PostgreSQL means rewriting triggers (the ideas carry over, the syntax
doesn't).

**What stays in the program.** Rules that need information the database
doesn't have (is the payment provider happy?), that talk to the outside
world (send the confirmation email), or that are about presentation
(which error message to show in which language) belong in application
code. A common, workable split is the one used here: the database
guarantees the data is never wrong, and the program decides what to do
and how to tell the user.
