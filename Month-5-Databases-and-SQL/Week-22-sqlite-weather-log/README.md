# Week 22 — SQL Level 2 (Intermediate): Writing Data from Python

## Purpose

Weeks 19–21 only *read* a database someone else had filled. Real programs
write to one too, and that's where the hard parts are: bad data trying to
get in, a crash halfway through a batch of inserts, and user input that
ends up inside a SQL statement. This week's project is a small weather
log, a command-line program that keeps observations in a SQLite file, and
it closes Level 2: the schema from Week 21 gets rules that
reject impossible data, every write goes through a transaction so it
either fully happens or doesn't happen at all, and every value from
outside reaches SQLite as a parameter, which is what makes SQL injection
impossible rather than merely unlikely.

## Objectives

The code in this project concretely demonstrates:

- `CREATE TABLE` with constraints — `NOT NULL`, `UNIQUE`, `CHECK`, a
  multi-column `UNIQUE`, and a foreign key with `ON DELETE CASCADE` — and
  why a `CHECK` needs `IS` rather than `=` when `NULL` is possible.
- `PRAGMA foreign_keys = ON`, and what SQLite silently allows without it.
- `INSERT`, `INSERT ... SELECT`, `UPDATE`, and `DELETE`, and reading
  `cursor.rowcount` and `cursor.lastrowid` to find out what they did.
- Transactions with `with conn:` — commit on success, roll back on any
  exception — including an import that is all-or-nothing across many
  rows.
- Parameterised queries with `?` and `:name` placeholders, and exactly
  why pasting values into SQL text is dangerous.
- `sqlite3.Row` for reading columns by name instead of by position.
- Where each kind of validation belongs: text parsing at the program's
  boundary, data rules in the schema.

## Concepts Refresher

### Creating tables: types and constraints

`CREATE TABLE` names the columns, their types, and the rules every row
must satisfy. Look at `src/weather_log/schema.sql` alongside this
section.

SQLite's types are looser than most databases'. A column's declared type
is a preference (SQLite calls it *affinity*), not a hard rule: SQLite
will convert `'12.5'` to a number for a `REAL` column, but it will also
store `'warm'` there without complaint. (SQLite 3.37+ has `STRICT` tables
that reject that; this project uses constraints instead, which work on
every version and say more than a type can anyway.)

Constraints are what actually keep bad data out:

| Constraint | Rejects | Example in `schema.sql` |
|---|---|---|
| `NOT NULL` | a missing value | every column except `wind_ms` |
| `UNIQUE` | a value already used in another row | `cities.name` |
| `UNIQUE (a, b)` | a *combination* already used | one observation per city per day |
| `CHECK (expr)` | a row for which `expr` is false | `precipitation_mm >= 0`, `conditions IN (...)` |
| `REFERENCES t (col)` | a value that doesn't exist in `t.col` | `observations.city_id` |

A `CHECK` can involve several columns (`CHECK (temp_min_c <=
temp_max_c)`), and can call functions: `date(observed_on) IS
observed_on` accepts only real dates written as `YYYY-MM-DD`, because
`date()` normalizes anything it understands (so `'2026-02-30'` becomes
`'2026-03-02'`, which doesn't match) and returns `NULL` for anything it
doesn't.

That `IS` matters. A `CHECK` **fails only when its expression is false**.
If the expression is `NULL`, the row is accepted, because `NULL` means
"unknown" and SQL gives unknown the benefit of the doubt. `CHECK
(date(observed_on) = observed_on)` would therefore let `'yesterday'`
through: `date('yesterday')` is `NULL`, so the comparison is `NULL`, not
false. `IS` is the `NULL`-safe comparison: `NULL IS 'yesterday'` is
false. The same rule is also why `CHECK (wind_ms >= 0)` doesn't need a
special case for missing readings: `NULL >= 0` is `NULL`, which passes.

### Foreign keys have to be switched on

SQLite parses `REFERENCES` but, for backwards compatibility, doesn't
enforce it unless each connection runs `PRAGMA foreign_keys = ON`. Without
it, you can insert an observation for city 99 that doesn't exist, and
nothing complains. `open_log` turns it on first thing, and a test shows
the difference. Most other databases always enforce foreign keys.

`ON DELETE CASCADE` says what happens to observations when their city is
deleted: they're deleted too. The default (no `ON DELETE` clause) is to
refuse to delete a city that still has observations. See Reflection for
which one to pick.

### Changing data: INSERT, UPDATE, DELETE

```sql
INSERT INTO cities (name, country, population) VALUES ('Bergen', 'Norway', 291940);
UPDATE observations SET precipitation_mm = 6.0 WHERE id = 39;
DELETE FROM cities WHERE name = 'Copenhagen';
```

- Always **name the columns** in an `INSERT`. `INSERT INTO cities VALUES
  (...)` depends on the table's column order and breaks, or silently
  puts values in the wrong columns, when the table changes. Columns you
  leave out get their default (`NULL`, or for `INTEGER PRIMARY KEY`, the
  next free id).
- `UPDATE` and `DELETE` without `WHERE` apply to **every row in the
  table**. There's no undo, and no warning. Write the `WHERE` first, and
  when unsure, run it as a `SELECT` to see which rows it matches.
- `INSERT ... SELECT` inserts whatever rows a query returns. `store.py`
  uses it to turn a city *name* into a `city_id` inside the insert
  itself: if no city has that name, the `SELECT` returns no row, nothing
  is inserted, and `cursor.rowcount` is 0, which the code turns into
  `ValueError("unknown city")`.

After an `execute`, `cursor.rowcount` is how many rows the statement
changed, and `cursor.lastrowid` is the id of the row it inserted.
`correct_precipitation` and `delete_city` use `rowcount == 0` to report
"nothing matched" instead of silently doing nothing.

### Transactions: all or nothing

A **transaction** groups statements so they take effect together or not
at all. Importing a CSV file is the textbook case: if row 3 of 3 is
invalid, you don't want rows 1 and 2 left in the database, because then
fixing the file and importing it again fails on duplicates (or, without a
`UNIQUE` constraint, silently double-counts). Databases guarantee this
under the name *atomicity* — the "A" in ACID — along with *consistency*
(constraints hold after every transaction), *isolation* (other
connections don't see half-finished work), and *durability* (once
committed, it survives a crash).

Python's `sqlite3` module opens a transaction automatically before the
first `INSERT`/`UPDATE`/`DELETE`, and you end it with `conn.commit()` or
`conn.rollback()`. Using the connection as a context manager does that
for you:

```python
with conn:                       # on exit: commit() if no exception, rollback() if there was one
    for observation in observations:
        _insert_observation(conn, observation)
```

If any insert raises (a `CHECK` fails, a city is unknown), the exception
leaves the `with` block, everything since the transaction began is
rolled back, and the exception carries on to the caller. Two tests show
this: a batch whose last row is invalid leaves zero rows behind, and
data committed *before* a failed import is untouched.

Until a transaction commits, other connections can't see its changes. A
program that inserts and never commits looks fine while it runs and then
loses everything when it exits; that's the most common "my data didn't
save" bug with `sqlite3`.

`with conn:` does **not** nest. An inner `with conn:` commits when it
exits, even if an outer one is still open. That's why `import_observations`
calls the private `_insert_observation` in its loop rather than the
public `record` (which has its own `with conn:` and would commit after
every row, making the import no longer all-or-nothing).

### Parameters, and why never to build SQL with f-strings

Here's the tempting way to look up a city:

```python
# DON'T
conn.execute(f"SELECT * FROM cities WHERE name = '{city}'")
```

With `city = "Oslo"` it works. With `city = "Val d'Isère"` the apostrophe
ends the string early and the query is a syntax error. With `city = "' OR
'1'='1"` the query becomes

```sql
SELECT * FROM cities WHERE name = '' OR '1'='1'
```

which is true for every row, so the user sees data they asked no
questions about. That's **SQL injection**: input that was meant to be a
value gets interpreted as SQL. In a program with a login form or a
`DELETE`, it's a security hole, not a curiosity.

The fix isn't escaping quotes more carefully; it's never putting values
into SQL text at all. Use a placeholder and pass the values separately:

```python
conn.execute("SELECT * FROM cities WHERE name = ?", (city,))            # positional
conn.execute("SELECT * FROM cities WHERE name = :name", {"name": city}) # named
```

The SQL text and the values travel to SQLite separately. SQLite parses
the SQL once, with a hole where the value goes, and then fills the hole
with the value as data, so no value can ever change the structure of the
statement. The tests store `"Val d'Isère"` without trouble, and looking up
`"' OR '1'='1"` returns no rows. (`(city,)` is a one-element tuple; the
comma matters.) Named placeholders pair well with dataclasses:
`asdict(observation)` produces exactly the dict that `:observed_on`,
`:temp_max_c`, and so on, need.

Placeholders work for *values* only. Table and column names can't be
parameters, so if a column name ever comes from input, check it against a
fixed list of allowed names in your code.

### Reading rows by name

By default a row comes back as a tuple, so `row[4]` means "whatever the
fifth column in this `SELECT` is", which breaks quietly when the query
changes. Setting `conn.row_factory = sqlite3.Row` makes rows that also
support `row["wind_ms"]` and `row.keys()`, while still behaving like
tuples where needed.

### Which layer validates what

There are two kinds of bad input, and they're caught in two places:

- **Malformed text** — `"warm"` where a number should be — can't even be
  turned into an `Observation`. `csv_import.py` catches that while
  parsing, and reports the file's line number.
- **Well-formed but impossible values** — negative rain, `'hail'`, a
  low above the high, a second reading for the same day — are rejected
  by the schema. Putting those rules in the database means they hold for
  every program that ever writes to it, including the `sqlite3` shell
  and next year's rewrite, not only for this one. The Python code
  doesn't repeat them; it lets `sqlite3.IntegrityError` propagate, and
  the CLI prints its message.

## Design & Architecture

```
Week-22-sqlite-weather-log/
├── conftest.py                          - adds src/ to sys.path for pytest
├── src/
│   └── weather_log/
│       ├── __init__.py
│       ├── schema.sql                   - tables and every data rule
│       ├── store.py                     - all SQL: open_log, add_city, record, import_observations,
│       │                                  correct_precipitation, delete_city, city_observations, summary
│       ├── csv_import.py                - CSV text -> Observation objects (no SQL, no database)
│       ├── cli.py                       - argparse commands; prints results and errors
│       └── data/
│           ├── cities.csv               - the eight cities from Weeks 19-21
│           ├── sample_week.csv          - the same 49 observations
│           ├── 2026-09-28.csv           - one more day, including Copenhagen's first reading
│           └── 2026-09-29-with-error.csv - three rows, the last one invalid ('hail')
└── tests/
    ├── test_schema.py                   - the rules, tested with raw SQL that bypasses store.py
    ├── test_store.py                    - each store function, transactions, injection
    └── test_csv_import.py               - parsing, and importing the bundled files
```

The split follows the same pure-logic/thin-CLI line as every earlier
week, with one more layer. `schema.sql` owns the rules. `store.py` is the
only module that contains SQL; each function takes a connection as its
first argument rather than opening its own, so tests can hand it a fresh
in-memory database and the CLI can hand it a file. `csv_import.py` knows
about CSV files but not about databases. `cli.py` wires them together and
is the only place that prints or exits.

## How to Build & Run

```bash
cd Month-5-Databases-and-SQL/Week-22-sqlite-weather-log
export PYTHONPATH=src            # PowerShell: $env:PYTHONPATH="src"

# Create weather.db and load the sample week:
python3 -m weather_log.cli weather.db init
python3 -m weather_log.cli weather.db report

# Try importing a file with an invalid last row, then check nothing was added:
python3 -m weather_log.cli weather.db import src/weather_log/data/2026-09-29-with-error.csv
python3 -m weather_log.cli weather.db report

# Import a valid day (run it twice to see the UNIQUE constraint stop the duplicate):
python3 -m weather_log.cli weather.db import src/weather_log/data/2026-09-28.csv

# Look at, correct, and delete data:
python3 -m weather_log.cli weather.db show Kiruna
python3 -m weather_log.cli weather.db correct Visby 2026-09-24 6.0
python3 -m weather_log.cli weather.db delete-city Copenhagen
```

`weather.db` is an ordinary SQLite file (and git-ignored). Open it in DB
Browser for SQLite or the `sqlite3` shell to see exactly what the program
wrote; delete it to start over.

## Testing

```bash
cd Month-5-Databases-and-SQL/Week-22-sqlite-weather-log
python3 -m pytest -q
```

`test_schema.py` writes raw SQL straight at the database, bypassing
`store.py`, to show that the rules hold for any writer: foreign keys
(including a demonstration that SQLite ignores them without the
`PRAGMA`), cascading deletes, every `CHECK` (negative rain and wind,
unknown weather, low above high, five kinds of bad date, negative
population), both `UNIQUE` constraints, and reopening an existing file.
`test_store.py` covers each store function, the all-or-nothing import
(an invalid last row, an unknown city mid-batch, and earlier data
surviving a failed import), commits being visible from a second
connection, the apostrophe and injection cases, and `summary` including a
city with no observations. `test_csv_import.py` covers parsing (missing
wind, a non-number with its line number) and the bundled data files.

## Try It Yourself

> **Facit (answer key):** every exercise below is solved, tested and explained
> in Swedish in [FACIT.md](FACIT.md). Try each one yourself first, then compare.

1. Add `record_or_replace(conn, observation)`, which inserts a new
   observation or, if that city already has one for that day, replaces
   it. Use SQLite's `INSERT ... ON CONFLICT (city_id, observed_on) DO
   UPDATE SET ...` rather than a `SELECT` followed by an `INSERT` or
   `UPDATE`, and write a test showing the row count doesn't grow.
2. Add a `rename-city OLD NEW` command. What should happen if `NEW` is
   already taken, and which layer should decide that? Write the test
   before the code.
3. Replace `ON DELETE CASCADE` with the default behavior, so a city with
   observations can't be deleted. Update `delete_city` and its tests, and
   decide what message the CLI should show in that case.
4. Add a `warnings` table (see Week 21, Try It Yourself 5) with its own
   `CHECK` constraints — the level must be yellow, orange or red, and a
   warning can't end before it starts — plus a function that returns the
   cities with an active warning on a given date. Make sure every value
   in it is a parameter.
5. Write a deliberately vulnerable `unsafe_city_observations` that builds
   its SQL with an f-string, and a test that proves the injection string
   returns every observation. Then delete the function, and keep the
   test's input in `test_store.py`'s injection test, where it proves the
   real function is safe.

## Reflection

**Rules in the schema, or in Python?** Putting them in the schema means
they can't be bypassed, but it also means error messages come from
SQLite (`CHECK constraint failed: conditions IN (...)`), which are
precise but not friendly. A larger program would often check the same
rules in Python too, to give users better messages, and keep the schema
as the last line of defense. The duplication is the price of both.

**CASCADE or not?** Cascading is convenient: deleting a city cleans up
after itself. It's also a way to delete a thousand rows by deleting one.
For observations that only mean something together with their city, it's
reasonable. For something with value of its own, like invoices belonging
to a customer, refusing the delete (the default) is usually the safer
choice, and forces whoever deletes to decide what happens to the rest
first.
