# Week 19 — SQL Level 1 (Beginner): Querying One Table

## Purpose

Almost every real program keeps its data in a database, and almost every
database is queried with SQL. Until now, every week kept its data in
Python lists and dicts that vanished when the program exited, and
"find the rows where X" meant writing a loop. SQL flips that around: you
describe *which* rows and columns you want, and the database works out
*how* to find them. This week is only about reading data from one table
at a time, which is most of what people do with SQL day to day, and the
foundation for everything after it.

This month's SQL track has three levels of two weeks each:

| Level | Weeks | You'll be able to |
|---|---|---|
| 1 — Beginner | 19–20 | ask questions of one table: filter, sort, count, sum, group |
| 2 — Intermediate | 21–22 | combine tables with joins, and write data safely from Python |
| 3 — Advanced | 23–24 | run multi-step analyses with CTEs and window functions, and put business rules in the database itself |

## Objectives

The queries in this project concretely demonstrate:

- `SELECT *` versus naming the columns you want, and in which order.
- Computed columns (`temp_max_c - temp_min_c`), `ROUND`, and naming a
  result column with `AS`.
- Filtering rows with `WHERE`: numeric comparisons, text comparisons,
  `AND`, `OR`, `IN`, and `BETWEEN`.
- `NULL` as "unknown": why `= NULL` never matches and `IS NULL` does,
  and how `NULL` behaves inside `OR`.
- Ordering results with `ORDER BY ... DESC` and cutting them off with
  `LIMIT` to get a top-N list.
- Removing duplicate result rows with `DISTINCT`.
- Storing dates as ISO-8601 text (`'2026-09-23'`) so that sorting and
  comparing them as text gives the right answer.

## Concepts Refresher

### Tables, rows, columns

A relational database stores data in **tables**. A table has a fixed set
of named, typed **columns**, and any number of **rows**, each of which
has one value per column. If you think of a list of dicts in Python where
every dict has exactly the same keys, you're close:

```python
cities = [
    {"id": 1, "name": "Stockholm", "country": "Sweden", "population": 984748},
    {"id": 2, "name": "Gothenburg", "country": "Sweden", "population": 604616},
]
```

The difference is that the database enforces the shape (every row has
every column, and a column's values have a declared type), and it owns
the data: your program asks for what it wants instead of looping over
everything itself.

This week's database has two tables, defined at the top of
`src/select_basics/data/weather.sql`:

| Table | One row is | Columns |
|---|---|---|
| `cities` | one city | `id`, `name`, `country`, `population` |
| `observations` | one city's weather on one day | `id`, `city_id`, `observed_on`, `temp_max_c`, `temp_min_c`, `precipitation_mm`, `wind_ms`, `conditions` |

`observations.city_id` holds the `id` of the city the reading belongs to
(1 is Stockholm, 5 is Kiruna, and so on). This week you just read it as a
number; Week 21 is about using it to connect the two tables.

The units are in the column names on purpose: `temp_max_c` is degrees
Celsius, `precipitation_mm` is millimetres, `wind_ms` is metres per
second. A column called just `temperature` invites someone to insert
Fahrenheit into it one day.

### SQL is declarative

A Python loop says *how* to get an answer, step by step. A SQL query says
*what* the answer is, and leaves the "how" to the database:

```python
# Python: you write the algorithm
wet = []
for obs in observations:
    if obs["precipitation_mm"] > 5:
        wet.append(obs)
```

```sql
-- SQL: you describe the result
SELECT *
FROM observations
WHERE precipitation_mm > 5;
```

The database may scan the table, or use an index, or do something
cleverer. You don't have to care, and on large tables that's the whole
point.

### The shape of a SELECT

Every query this week is some subset of this, and the clauses must appear
in this order:

```sql
SELECT DISTINCT column, expression AS alias   -- which columns come back
FROM table                                    -- where the rows come from
WHERE condition                               -- which rows are kept
ORDER BY column DESC                          -- in what order
LIMIT n;                                      -- how many
```

The database does *not* evaluate them in the order they're written. The
logical order is:

1. `FROM`: start with every row of the table.
2. `WHERE`: throw away rows whose condition isn't true.
3. `SELECT`: compute the output columns for the rows that are left.
4. `DISTINCT`: drop output rows that are exact duplicates.
5. `ORDER BY`: sort.
6. `LIMIT`: keep the first *n*.

That order explains a lot of behavior that otherwise looks arbitrary. For
example, `LIMIT 3` without `ORDER BY` gives you *some* three rows, not the
"first" three, because nothing has defined what first means yet. And
without `ORDER BY` at all, the order rows come back in is not part of the
answer: SQLite happens to return this data in insertion order, but
another database, or the same one after an index is added, may not.
That's why the tests for `q01`–`q08` compare results sorted, and only
`q09`–`q11` (which have `ORDER BY`) are compared in order.

Keywords are case-insensitive (`select` works), but writing them in
capitals is the convention because it makes the structure of the query
easy to see. The `;` ends a statement. Tools that accept several
statements at once (the `sqlite3` shell, this week's prompt) need it; a
single statement sent from Python doesn't, but it never hurts.

### Choosing and computing columns

`SELECT *` means every column, in table order. It's handy for exploring,
but in code you should name the columns you need: the result then
doesn't change shape when someone adds a column to the table, and the
reader can see what the query uses.

A column in `SELECT` can be any expression, not just a column name:

```sql
SELECT observed_on,
       city_id,
       ROUND(temp_max_c - temp_min_c, 1) AS range_c
FROM observations;
```

`AS range_c` names the computed column. Without it, the column is named
after the expression text, which is ugly and awkward to refer to from
Python. `ROUND(x, 1)` is there because `REAL` columns are floating point,
so `16.2 - 9.1` is really `7.099999999999999`; rounding for display is
the same fix you'd use in Python.

### Filtering with WHERE

`WHERE` keeps a row only if its condition is **true**. The comparison
operators are `=`, `<>` (or `!=`), `<`, `<=`, `>`, `>=`. Note the single
`=`: SQL has no assignment inside a query, so there's nothing to confuse
it with.

**Text goes in single quotes:** `WHERE conditions = 'sun'`. Double quotes
are for *identifiers* (column and table names that would otherwise be
invalid, like `"my column"`). SQLite forgives `"sun"` when no column is
called `sun`, which hides the mistake until the day someone adds one; use
single quotes and never find out.

**Combining conditions.** `AND` requires both sides, `OR` accepts either.
`AND` binds tighter than `OR`, exactly like `*` binds tighter than `+`, so

```sql
WHERE conditions = 'rain' OR conditions = 'snow' AND temp_max_c > 5
```

means `rain OR (snow AND warm)`, which is probably not what was meant.
When you mix them, write the parentheses yourself:

```sql
WHERE (conditions = 'rain' OR conditions = 'snow') AND temp_max_c > 5
```

**Shorthands.** `IN` replaces a chain of `OR`s on one column, and
`BETWEEN` replaces a pair of `>=`/`<=`. `BETWEEN` includes both ends.

```sql
WHERE name IN ('Stockholm', 'Oslo', 'Copenhagen')
WHERE observed_on BETWEEN '2026-09-23' AND '2026-09-25'
```

**Pattern matching.** `LIKE` compares text against a pattern where `%`
means "any run of characters" and `_` means "exactly one character":
`WHERE name LIKE 'Go%'` matches Gothenburg. In SQLite, `LIKE` ignores
case for plain ASCII letters but not for letters like `ö`. None of this
week's queries need it, but "Try It Yourself" does.

### Dates stored as text

SQLite has no separate date type. This database stores dates as text in
ISO-8601 form, `'YYYY-MM-DD'`, and that's a deliberate choice: with the
biggest unit first and every part zero-padded, comparing two dates as
text gives the same answer as comparing them as dates. `'2026-09-09' <
'2026-09-23'` is true character by character. A format like
`'23/9/2026'` would sort as nonsense. When you control the format,
always store dates this way.

### NULL means "unknown"

Two wind readings are `NULL`: the sensor failed, so the true value is
unknown. `NULL` isn't zero and isn't an empty string; it's the absence of
a value, and SQL treats any comparison with it as unknown too:

- `wind_ms > 10` where `wind_ms` is `NULL` is `NULL`, not false.
- `wind_ms = NULL` is also `NULL` — even when `wind_ms` is `NULL` —
  because "is this unknown value equal to that unknown value?" has no
  known answer.
- `WHERE` keeps only rows whose condition is *true*, so a `NULL`
  condition drops the row just like false does.

That's why the only way to find missing values is the special operator
`IS NULL` (and its opposite, `IS NOT NULL`), which is always true or
false. `q07` uses it, and one of the tests shows that the `= NULL`
version quietly returns nothing.

`NULL` inside `AND`/`OR` follows common sense once you read it as
"unknown": `TRUE OR unknown` is true (one side is enough), `FALSE AND
unknown` is false, and everything else involving unknown stays unknown.
`q06` depends on this: Kiruna's reading on 2026-09-24 has frost and a
`NULL` wind, and it's still returned, because the frost alone makes the
`OR` true.

### Sorting, limiting, and duplicates

`ORDER BY column` sorts ascending; add `DESC` for descending. You can
sort by several columns, each with its own direction:
`ORDER BY observed_on, temp_max_c DESC` sorts by date, and within one
date, warmest first. `LIMIT n` keeps the first *n* rows of the sorted
result, which together with `ORDER BY` is how you ask for a top-N list.

`DISTINCT` removes rows that are identical across *all* selected
columns. `SELECT DISTINCT conditions` gives each kind of weather once;
`SELECT DISTINCT conditions, city_id` gives each (kind, city) pair once.

## Design & Architecture

```
Week-19-sql-select-basics/
├── conftest.py                          - adds src/ to sys.path for pytest
├── src/
│   └── select_basics/
│       ├── __init__.py
│       ├── runner.py                    - open the database, load and run .sql files, format results
│       ├── cli.py                       - run a query by name, or an interactive SQL prompt
│       ├── data/
│       │   └── weather.sql              - CREATE TABLE statements plus all the data
│       └── queries/
│           ├── q01_all_cities.sql       - one question per file, answered in SQL
│           ├── ...
│           └── q11_distinct_conditions.sql
└── tests/
    ├── test_queries.py                  - each query's exact expected result
    └── test_runner.py                   - the Python plumbing
```

The SQL lives in `.sql` files, not in Python strings. Each file starts
with the question it answers as a comment, so you can read the queries
in order as a worked set of exercises, and paste any of them into any
SQL tool. The Python side only loads those files, runs them, and prints
the results.

`runner.open_database()` builds a brand-new **in-memory** database from
`weather.sql` each time it's called. Nothing is written to disk, so you
can run `DELETE FROM cities;` at the prompt to see what happens, and the
next run starts from the original data again. Every test gets its own
fresh copy for the same reason.

## How to Build & Run

Nothing to install: SQLite ships with Python as the `sqlite3` module.

```bash
cd Month-5-Databases-and-SQL/Week-19-sql-select-basics

# Run one of the bundled queries (prints the SQL, then its result):
PYTHONPATH=src python3 -m select_basics.cli q10_three_warmest_days

# Or open an interactive prompt and type your own queries:
PYTHONPATH=src python3 -m select_basics.cli
```

At the prompt, a statement runs once you end it with `;`, so you can
spread a query over several lines:

```
sql> SELECT name, population
 ..> FROM cities
 ..> WHERE country = 'Sweden';
```

On Windows PowerShell, set the path first with `$env:PYTHONPATH="src"`
and then run `python -m select_basics.cli`.

**Prefer a graphical tool?** Write the data to a database file, then open
`weather.db` in [DB Browser for SQLite](https://sqlitebrowser.org/)
(free), VS Code's SQLite extensions, or IntelliJ Ultimate's Database tool
window:

```bash
python3 -c "import sqlite3; sqlite3.connect('weather.db').executescript(open('src/select_basics/data/weather.sql', encoding='utf-8').read())"
```

(Run it once; running it again fails with "table cities already exists".
Delete `weather.db` to start over. `*.db` files are git-ignored.) If you
have the `sqlite3` command-line shell installed, `sqlite3 weather.db <
src/select_basics/data/weather.sql` does the same thing.

There's also a browser-based version of these exercises with instant
feedback: open `../sql-playground/index.html`.

## Testing

```bash
cd Month-5-Databases-and-SQL/Week-19-sql-select-basics
python3 -m pytest -q
```

`test_queries.py` runs every query against the bundled data and checks
its exact result: the column names where they matter (`q01`–`q03`), the
precise set of rows each filter keeps (including the `NULL` wind reading
that `q06` must keep and the `= NULL` mistake that matches nothing), and
the exact order for the queries that sort. `test_runner.py` covers the
Python side: each call gets a fresh database, unknown query names fail
with a helpful message, and the table formatter pads columns, prints
`NULL`, and handles an empty result.

The tests double as an answer key. To practise, empty out a query file,
write your own version, and run the tests again.

## Try It Yourself

Write each answer as a new `.sql` file in `queries/` (for example
`q12_...sql`) so you can run it with the CLI, and add a test for it.

1. List every city in Sweden with fewer than 200,000 inhabitants,
   largest first.
2. Find the observations for Gothenburg (city_id 2) where it rained but
   the high still reached 14 degrees. Then change the query to find days
   that were rainy **or** snowy **and** below 10 degrees, and check that
   your parentheses give the answer you meant (Kiruna should appear,
   Oslo should not).
3. Using `LIKE`, list the cities whose name ends in `a`. Then try
   `LIKE 'malmö'` and `LIKE 'MALMÖ'` and explain why only one of them
   matches.
4. Which three observations had the *smallest* difference between high
   and low? Show the date, city_id and the difference. What happens to
   your query if two observations tie for third place, and how could you
   make the result predictable?
5. Show every observation from the weekend (2026-09-26 and 2026-09-27)
   where the wind reading is known and below 3 m/s. Explain why leaving
   out the `IS NOT NULL` check gives the same result here, and when it
   wouldn't.
