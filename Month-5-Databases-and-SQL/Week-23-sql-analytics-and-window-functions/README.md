# Week 23 — SQL Level 3 (Advanced): Analytics with CTEs and Window Functions

## Purpose

Levels 1 and 2 answered questions that fit in one pass: filter, group,
join, done. Real analysis questions usually don't. "Which product earns
each store the most?" needs a total per store and product, then a
ranking within each store, then the top row of each ranking. "Did the
store beat its own average today?" needs every day's revenue next to a
number computed from all the other days. This week adds the three tools
that make multi-step analysis readable in SQL: common table expressions
(`WITH`) to build an answer in named steps, window functions to compute
across rows without collapsing them, and correlated subqueries for "is
there a matching row?" questions. It also covers the mistake that
quietly ruins more reports than any syntax error: joining tables at the
wrong level of detail and counting things twice.

## Objectives

The queries in this project concretely demonstrate:

- `WITH` (common table expressions): naming intermediate results, and
  chaining several of them.
- Window functions and the `OVER (...)` clause: `PARTITION BY`, `ORDER BY`
  inside the window, and how they differ from `GROUP BY`.
- Ranking with `ROW_NUMBER`, `RANK`, and `DENSE_RANK`, and the "top-1 per
  group" pattern.
- Share of total with `SUM(...) OVER ()`.
- Running totals with `SUM(...) OVER (ORDER BY ...)`.
- Comparing a row with the previous one using `LAG`.
- Moving averages with a window frame (`ROWS BETWEEN 2 PRECEDING AND
  CURRENT ROW`).
- Filtering on a window function's result from an outer query.
- Pivoting rows into columns with conditional aggregation.
- `NOT EXISTS` with a correlated subquery, and `CROSS JOIN` to build every
  combination to check.
- The fan-out trap: why you aggregate each table first and join the
  summaries second.

## Concepts Refresher

### The data this week

The weather tables from Weeks 19–22 are unchanged. Three tables are new,
describing a made-up chain of shops that sells weather gear, with one
store in each city that has observations:

| Table | One row is | Columns |
|---|---|---|
| `products` | a product | `id`, `name`, `category` (`'rain'`, `'cold'`, `'sun'`), `list_price_sek` |
| `stores` | a store | `id`, `city_id`, `opened_on` |
| `daily_sales` | one product's sales in one store on one day | `store_id`, `product_id`, `sold_on`, `units`, `revenue_sek` |

Two details matter for the analysis. `daily_sales` has no row when a
product sold nothing that day, so "no row" means zero, which will need
handling. And `revenue_sek` is what was actually charged: on Sunday
2026-09-27 umbrellas were 20% off, so revenue isn't always
`units * list_price_sek`. (Storing the price actually paid, rather than
recomputing it from today's price list, is a business-logic decision
Week 24 comes back to.)

Store ids are *not* city ids: store 4 is in Oslo, whose city id is 7. The
only safe way to get from a sale to a city name is through the keys:
`daily_sales.store_id → stores.id`, `stores.city_id → cities.id`.

### WITH: build the answer in named steps

A common table expression (CTE) is a named query you define at the top
and then use like a table in the rest of the statement:

```sql
WITH store_totals AS (
    SELECT store_id, SUM(revenue_sek) AS revenue_sek
    FROM daily_sales
    GROUP BY store_id
)
SELECT c.name, t.revenue_sek
FROM store_totals AS t
JOIN stores AS s ON s.id = t.store_id
JOIN cities AS c ON c.id = s.city_id;
```

It's the same idea as Week 21's subquery in `FROM`, but written first and
given a name, so the query reads top to bottom as a sequence of steps.
Several CTEs are separated by commas, and each one can use the ones
defined before it (`q03`: totals → ranked → top row). A CTE exists only
for the statement it belongs to.

Use them the way you'd use well-named helper functions: when a query has
more than one logical step, give each step a name. When a query has a
bug, you can also run each CTE on its own to find which step is wrong.

### Window functions: calculations across rows, keeping the rows

`GROUP BY` collapses each group into one row. A **window function**
computes something across a set of rows, but gives the answer *on every
row* instead of collapsing them. The set of rows it looks at is called
the window, and the `OVER (...)` clause defines it:

```sql
SUM(revenue_sek) OVER ()                                     -- window: every row
AVG(revenue_sek) OVER (PARTITION BY store_id)                -- window: rows of the same store
SUM(revenue_sek) OVER (PARTITION BY store_id ORDER BY sold_on) -- same store, up to this day
```

- `PARTITION BY` splits the rows into independent groups, like `GROUP BY`
  but without merging them. Without it, the whole result is one
  partition.
- `ORDER BY` inside `OVER` puts the rows of each partition in order. That
  order is what "previous row" (`LAG`), "row number" (`ROW_NUMBER`), and
  "everything so far" (running totals) are relative to. It's independent
  of the query's final `ORDER BY`.

Window functions are computed after `WHERE`, `GROUP BY` and `HAVING`, as
part of `SELECT`. Two consequences: you can put a window function around
an aggregate (`SUM(t.revenue_sek) OVER ()` in `q02` sums the per-store
totals), and you **can't** use a window function in `WHERE`. To filter
on one, compute it in a CTE and filter in the outer query, as `q08` does.

SQLite has supported window functions since version 3.25 (2018); every
Python 3.10+ ships with a newer one. Check yours with `SELECT
sqlite_version();`.

### Ranking: ROW_NUMBER, RANK, DENSE_RANK

All three number the rows of each partition in the window's order. They
differ only on ties. Ranking the stores by how many sales rows they have
shows the difference (Oslo and Stockholm both have 24, Kiruna and Umeå
both have 23):

| store | rows | `ROW_NUMBER()` | `RANK()` | `DENSE_RANK()` |
|---|---|---|---|---|
| Oslo | 24 | 1 | 1 | 1 |
| Stockholm | 24 | 2 | 1 | 1 |
| Kiruna | 23 | 3 | 3 | 2 |
| Umeå | 23 | 4 | 3 | 2 |
| Gothenburg | 22 | 5 | 5 | 3 |

`ROW_NUMBER` never repeats a number, and breaks ties arbitrarily (Oslo
could just as well have been 2), so add a tie-breaking column to the
window's `ORDER BY` when the choice matters. `RANK` gives ties the same
number and then skips (1, 1, 3), like a sports table. `DENSE_RANK` gives
ties the same number without skipping (1, 1, 2).

"Top-1 per group" (`q03`) is the most common use: number the rows within
each partition, then keep `WHERE position = 1` in an outer query. Use
`ROW_NUMBER` for exactly one row per group, or `RANK` to keep all the
rows tied for first.

### Running totals, previous rows, and moving averages

With `ORDER BY` inside `OVER`, an aggregate like `SUM` covers the rows
from the start of the partition up to the current row, which is a
running total (`q04`). `LAG(x)` returns `x` from the previous row in the
window's order and `LEAD(x)` from the next one; on the first row, `LAG`
has nothing to return and gives `NULL` (`q05`), so the first day's
change is `NULL`, not 0. That's correct: there's no previous day to
compare with.

A **frame** narrows the window further. `q06` uses

```sql
AVG(temp_max_c) OVER (
    PARTITION BY city_id
    ORDER BY observed_on
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
)
```

which averages each day with the two days before it: a three-day moving
average, which smooths out single odd days. On the first two days the
frame simply has fewer rows in it, so the first value is just that day's
high.

`ROWS` counts rows, which only equals counting days if there is exactly
one row per day with no gaps, as there is here. With gaps in the dates,
"the two rows before" could reach back further than two days.

### Subqueries that test for existence

`EXISTS (subquery)` is true if the subquery returns at least one row, and
`NOT EXISTS` if it returns none. What the subquery selects doesn't
matter, so `SELECT 1` is the convention. It's usually **correlated**: it
refers to a column of the outer query, so it's evaluated for each outer
row:

```sql
WHERE NOT EXISTS (
    SELECT 1 FROM daily_sales AS ds
    WHERE ds.store_id = s.id AND ds.product_id = p.id   -- s and p come from the outer query
)
```

To ask "which combinations never happened?" you first need every
combination. `CROSS JOIN` pairs every row of one table with every row of
the other (7 stores × 5 products = 35 pairs), and `NOT EXISTS` keeps the
pairs with no sales. `NOT EXISTS` is also safer than `NOT IN (subquery)`:
if the subquery returns a single `NULL`, `x NOT IN (...)` is never true,
for the same three-valued-logic reason as Week 19's `= NULL`.

### Pivoting with conditional aggregation

`q09` turns category *rows* into category *columns* with one
`SUM(CASE WHEN category = '...' THEN revenue_sek ELSE 0 END)` per
category: Week 20's frost-night pattern, applied to money. The `ELSE 0`
matters: without it, a store that sold nothing in a category would get
`NULL` instead of 0.

### The fan-out trap: aggregate first, then join

This is the most important idea of the week, because it produces wrong
numbers with no error. Suppose you want total precipitation in the cities
where the stores are, and you already have a query joining weather and
sales:

```sql
SELECT SUM(o.precipitation_mm)
FROM observations AS o
JOIN stores AS s ON s.city_id = o.city_id
JOIN daily_sales AS ds ON ds.store_id = s.id AND ds.sold_on = o.observed_on;
```

The true total is 120.3 mm (Week 20). This query says 331.6. Each
observation is one row per city per day, but `daily_sales` has up to five
rows per store per day, one per product sold. The join repeats ("fans
out") each weather row once for every matching sales row, and the sum
counts most days' rain two, three or four times. A test in `test_queries.py`
pins this down.

The rule: **decide what one row means before you aggregate.** Summarize
each table at the level you need in its own CTE (one row per store-day,
or per store), and only then join the summaries, so every join is
one-to-one. `q07` follows it: it builds one row per store-day from the
weather, one row per store-day of umbrella sales, and joins those.

`q07` also shows the other half of the problem: rows that don't exist.
Days with no umbrella sales have no row in `daily_sales`, and averaging
only the rows that exist would ignore exactly the days that matter for
the question. Starting from every store-day and `LEFT JOIN`-ing the
sales, with `COALESCE(u.units, 0)` turning "no row" into 0, makes those
days count.

## Design & Architecture

```
Week-23-sql-analytics-and-window-functions/
├── conftest.py                                - adds src/ to sys.path for pytest
├── src/
│   └── analytics/
│       ├── __init__.py
│       ├── runner.py                          - open the database, load and run .sql files, format results
│       ├── cli.py                             - run a query by name, or an interactive SQL prompt
│       ├── data/
│       │   └── weather_shop.sql               - Weeks 19-22's weather data plus the shop tables
│       └── queries/
│           ├── q01_revenue_per_store.sql
│           ├── ...
│           └── q10_products_never_sold.sql
└── tests/
    ├── test_queries.py                        - exact results, plus consistency checks between queries
    └── test_runner.py                         - the Python plumbing
```

Same structure as Weeks 19–21. The queries are longer, so each one is
laid out one CTE per step, with the step's purpose in its name.

## How to Build & Run

```bash
cd Month-5-Databases-and-SQL/Week-23-sql-analytics-and-window-functions

# Run one of the bundled queries:
PYTHONPATH=src python3 -m analytics.cli q03_best_product_per_store

# Or open an interactive prompt:
PYTHONPATH=src python3 -m analytics.cli
```

On Windows PowerShell: `$env:PYTHONPATH="src"`, then `python -m
analytics.cli`. The interactive prompt is the best way to take a long
query apart: paste just its first CTE's `SELECT`, check the result, then
add the next step.

## Testing

```bash
cd Month-5-Databases-and-SQL/Week-23-sql-analytics-and-window-functions
python3 -m pytest -q
```

Besides each query's exact result, the tests check that the queries agree
with each other and with the raw data, which is how you should check
real analysis too: the per-store totals add up to the table's total, the
shares add up to 100%, the running total ends at the week's total from
`q01`, each running total step adds exactly that day's revenue, the
category pivot adds up to each store's total, and `q07` covers all 49
store-days. Others pin down window behavior: `LAG` is `NULL` on each
store's first day and never compares one store with another, and the
moving average uses one, two, then three days. One test demonstrates the
fan-out trap. The expected numbers were cross-checked with an
independent plain-Python calculation, not only copied from SQLite.

## Try It Yourself

1. For each product, rank the stores by units sold with `DENSE_RANK`, and
   list only each product's top two stores. Where do ties appear?
2. Using `LAG` twice (or a frame), find the store-days where revenue rose
   two days in a row.
3. Compute each store's revenue per 1,000 inhabitants of its city, and
   rank the stores by it. Does the ranking change compared with `q02`,
   and what does that tell you about raw totals?
4. The Sunday umbrella promotion: for each store, compare Sunday's
   umbrella units with the store's average umbrella units on the other
   days. Can you tell from this data whether the promotion worked? What
   else would you need to know? (Hint: what was the weather on Sunday?)
5. Write a query that shows, for each city, the precipitation total from
   `observations` and the rain-category revenue from `daily_sales` side
   by side, one row per city. Make it give the right precipitation (the
   Week 20 numbers), and write down how you checked that it isn't
   fanning out.
