# Week 21 — SQL Level 2 (Intermediate): Keys and JOINs

## Purpose

For two weeks, observations have said `city_id = 5` and you've had to
remember that 5 means Kiruna. That's not an accident of the dataset;
it's how relational databases are meant to be designed. Each fact is
stored once, in the table where it belongs, and tables point at each
other with keys. `JOIN` is how you put the pieces back together when you
query. This week covers both halves: why the data is split up the way it
is, and how to combine it again, including the case every real schema
runs into sooner or later — a row on one side with nothing matching on
the other.

## Objectives

The queries in this project concretely demonstrate:

- Primary keys and foreign keys, and the one-to-many relationship
  between `cities` and `observations`.
- Why a city's name lives in `cities` and not in every observation
  (normalization), and what goes wrong when it doesn't.
- `JOIN ... ON` (an inner join), table aliases, and qualified column
  names like `c.name`.
- Filtering and grouping on columns from either side of a join.
- `LEFT JOIN` to keep rows that have no match, and using `IS NULL` on
  the right-hand side to find exactly those rows.
- Why `COUNT(o.id)` and not `COUNT(*)` after a `LEFT JOIN`.
- A subquery in `FROM`: a grouped result used as if it were a table.
- Joining a table to itself, with two aliases playing two roles.

## Concepts Refresher

### Keys: how rows point at each other

A **primary key** is a column (or set of columns) whose value is unique
for every row and never `NULL`: it's the row's identity. Both tables use
an `INTEGER PRIMARY KEY` called `id`. In SQLite that column is special:
if you insert a row without an `id`, SQLite picks the next free number
for you (a test shows a new city getting `id` 9).

A **foreign key** is a column that holds another table's primary key.
`observations.city_id` holds a `cities.id`, and the schema says so:

```sql
city_id INTEGER NOT NULL REFERENCES cities (id)
```

That describes a **one-to-many** relationship: one city has many
observations, and each observation belongs to exactly one city. Week 4's
data structures give you the intuition: a foreign key is like storing a
dict key instead of a copy of the value.

(`REFERENCES` also lets the database *reject* a `city_id` that doesn't
exist. SQLite only enforces that when you turn it on, which Week 22
does.)

`cities.name` is declared `UNIQUE`: there's a second way to identify a
city, but `id` stays the key other tables use, because names can change
and integers are cheaper to store and compare.

### Why split the data at all?

The alternative is one wide table with the city's details repeated on
every observation:

| observed_on | city_name | country | population | temp_max_c | ... |
|---|---|---|---|---|---|
| 2026-09-21 | Stockholm | Sweden | 984748 | 16.2 | ... |
| 2026-09-22 | Stockholm | Sweden | 984748 | 15.4 | ... |
| ... seven rows per city ... | | | | | |

It works until the data changes. Stockholm's population is now stored
seven times; update six of them and the table contradicts itself, and no
query can tell you which value is right. Misspell "Stockholm" once and
that observation silently becomes a different city in every `GROUP BY`.
And Copenhagen, with no observations yet, can't be stored at all.

Splitting the data so that **each fact is stored in exactly one place**
is called normalization. The rule of thumb: if a value depends only on
the city, it goes in `cities`; if it depends on the city *and* the day,
it goes in `observations`. The price is that queries need to join the
tables back together, which is exactly what databases are built to do
quickly.

### JOIN: pairing rows that belong together

```sql
SELECT c.name, o.observed_on, o.temp_max_c
FROM observations AS o
JOIN cities AS c ON c.id = o.city_id;
```

A useful mental model (not how the database executes it, but what the
result is): take every possible pair of one observation row and one city
row (49 × 8 = 392 pairs), then keep only the pairs where the `ON`
condition is true. Each observation matches exactly one city, so 49 rows
come back, each carrying columns from both tables.

`AS o` and `AS c` are **aliases**: short names for the tables within
this query. (`AS` is optional: `FROM observations o` means the same.)
Once there's more than one table, prefix columns with the alias.
Sometimes it's required: both tables have an `id` column, so a bare `id`
is ambiguous and SQLite refuses the query. Sometimes it's only clarity:
`name` exists in one table only, but `c.name` tells the reader where it
comes from without them checking the schema.

`JOIN` on its own means `INNER JOIN`: only pairs that match survive. A
row with no partner on the other side disappears. That's why
Copenhagen, with no observations, is missing from `q01`–`q04`, and why
Denmark doesn't show up in `q04` at all.

After the join, the combined rows behave like one table: `WHERE`,
`GROUP BY`, `HAVING` and `ORDER BY` from Weeks 19–20 all work, on columns
from either side. The logical order is the same as before, with the join
being part of step 1 (`FROM`).

`q03` groups by `c.id, c.name` rather than just `c.name`. Grouping by the
key guarantees one group per city even if two cities ever share a name,
and adding `c.name` makes the name a grouped column, so it can appear in
`SELECT`.

### LEFT JOIN: keep everything on the left

`LEFT JOIN` keeps **every** row from the table on the left, whether or
not it has a match. When it doesn't, the right table's columns are
filled with `NULL`:

```sql
SELECT c.name, o.id, o.observed_on
FROM cities AS c
LEFT JOIN observations AS o ON o.city_id = c.id;
-- ...
-- Copenhagen | NULL | NULL      <- no observations, kept anyway
```

Which table is "left" matters: it's the one written before `LEFT JOIN`.
That padded row gives you two useful patterns:

- **Find rows with no match** (`q05`): `WHERE o.id IS NULL`. Every real
  observation has an `id`, so a `NULL` there can only mean "no
  observation matched". Always test a column that can't be `NULL` in a
  real row, like the primary key.
- **Count matches, including zero** (`q06`): `COUNT(o.id)` counts
  non-`NULL` values, so Copenhagen's padded row contributes 0. `COUNT(*)`
  counts rows, and Copenhagen does have one row after the join (the
  padded one), so it would wrongly report 1. A test demonstrates both.

One more trap: a condition on the right-hand table belongs in `ON`, not
`WHERE`, if you want to keep the unmatched rows. `WHERE o.conditions =
'snow'` runs *after* the join, sees `NULL` for every padded row, and
throws those rows away, quietly turning your `LEFT JOIN` back into an
inner join. `ON o.city_id = c.id AND o.conditions = 'snow'` restricts
which observations match while still keeping every city. (Try It Yourself
exercise 3 makes you see this for yourself.)

### A subquery as a table

"On which day did each city reach its warmest high?" is two steps: find
each city's maximum (a `GROUP BY`), then find the row that has it. A
query in parentheses in the `FROM` clause produces a result that can be
joined like any table, as long as you give it an alias:

```sql
JOIN (
    SELECT city_id, MAX(temp_max_c) AS warmest_c
    FROM observations
    GROUP BY city_id
) AS best ON best.city_id = o.city_id
         AND best.warmest_c = o.temp_max_c
```

A join condition can have several parts, joined with `AND`: here, the
same city *and* the same temperature. If a city had hit its maximum on
two different days, both days would match and both would be returned,
which is the correct answer to the question as asked.

### Joining a table to itself

Nothing says both sides of a join must be different tables. In `q08`,
`observations` appears twice: `o` is "the city we're looking at" and
`sthlm` is "Stockholm's reading on the same day". Aliases are what make
this possible; without them, `observations.temp_max_c` would be
ambiguous. The join condition pairs rows from the same date, the `WHERE`
restricts one side to Stockholm and keeps the pairs where the other side
was warmer. Stockholm never appears as a result, because it can't be
warmer than itself.

## Design & Architecture

```
Week-21-sql-joins-and-keys/
├── conftest.py                                  - adds src/ to sys.path for pytest
├── src/
│   └── joins/
│       ├── __init__.py
│       ├── runner.py                            - open the database, load and run .sql files, format results
│       ├── cli.py                               - run a query by name, or an interactive SQL prompt
│       ├── data/
│       │   └── weather.sql                      - same data as Weeks 19-20
│       └── queries/
│           ├── q01_observations_with_city_names.sql
│           ├── ...
│           └── q08_warmer_than_stockholm.sql
└── tests/
    ├── test_queries.py                          - each query's exact result, plus the LEFT JOIN traps
    └── test_runner.py                           - the Python plumbing
```

Same structure and data as Weeks 19 and 20. The schema at the top of
`data/weather.sql` is worth rereading this week: the `PRIMARY KEY`,
`REFERENCES` and `UNIQUE` declarations there are what this week's
Concepts Refresher is about.

## How to Build & Run

```bash
cd Month-5-Databases-and-SQL/Week-21-sql-joins-and-keys

# Run one of the bundled queries:
PYTHONPATH=src python3 -m joins.cli q06_observation_count_per_city

# Or open an interactive prompt:
PYTHONPATH=src python3 -m joins.cli
```

On Windows PowerShell: `$env:PYTHONPATH="src"`, then `python -m
joins.cli`. See Week 19's README for opening the data in a graphical
tool, and `../sql-playground/index.html` for the browser version.

## Testing

```bash
cd Month-5-Databases-and-SQL/Week-21-sql-joins-and-keys
python3 -m pytest -q
```

`test_queries.py` checks each query's exact result, and pins down the
behaviors that separate the join types: inner joins drop Copenhagen
(and with it Denmark), `LEFT JOIN` keeps it with a count of 0, `COUNT(*)`
after a `LEFT JOIN` would wrongly report 1, and swapping `q06`'s `LEFT
JOIN` for `JOIN` makes Copenhagen disappear. It also checks that the
subquery in `q07` yields exactly one warmest day per city, that the
self-join in `q08` never compares Stockholm with itself, and that the
schema's keys behave as described (automatic `id`, `UNIQUE` city names).

## Try It Yourself

1. List each country with the number of cities and the number of
   observations it has, including Denmark with 0 observations. (You'll
   need a `LEFT JOIN` and two different `COUNT`s. Check that Sweden's
   city count is 6, not 42.)
2. For every city, show its name and its number of snow days, with 0 for
   cities that had none, using `LEFT JOIN` and **no** `CASE`.
3. Run these two queries and explain, using the logical order of a
   query, why they return a different number of rows:
   ```sql
   SELECT c.name, o.observed_on FROM cities c
   LEFT JOIN observations o ON o.city_id = c.id AND o.conditions = 'snow';

   SELECT c.name, o.observed_on FROM cities c
   LEFT JOIN observations o ON o.city_id = c.id WHERE o.conditions = 'snow';
   ```
4. Using a self-join and SQLite's `date(observed_on, '-1 day')`, list
   every observation whose high was at least 2 degrees warmer than the
   same city's high the day before. Why does no 2026-09-21 observation
   ever appear?
5. Sketch (on paper or as `CREATE TABLE` statements) how you'd add
   weather *warnings* to this schema: a warning covers one city, has a
   level (yellow/orange/red) and a text, and starts and ends on given
   dates. Which table does it reference, and what would a query "cities
   with an active warning on 2026-09-23" look like?
