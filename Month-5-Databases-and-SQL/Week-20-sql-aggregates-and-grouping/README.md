# Week 20 — SQL Level 1 (Beginner): Aggregates, GROUP BY, and HAVING

## Purpose

Week 19's queries returned rows as they are stored. Most questions people
actually ask a database are summaries instead: how much rain fell in
total, which city was windiest on average, how many sunny days each city
got. In Python you'd answer those with a loop and a dict of running
totals, the same pattern as Week 4's `word_frequencies`. SQL builds that
pattern into the language as aggregate functions and `GROUP BY`. This
week completes Level 1 (Beginner), and is about using them correctly,
including the two places people most often get them wrong: `NULL` values
inside aggregates, and the difference between `WHERE` and `HAVING`.

## Objectives

The queries in this project concretely demonstrate:

- The five standard aggregates: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, and
  how several of them in one `SELECT` produce a single summary row.
- `COUNT(*)` (rows) versus `COUNT(column)` (non-`NULL` values).
- How aggregates treat `NULL`: skipped by `SUM`/`AVG`/`MIN`/`MAX`, and
  what that does to an average.
- `GROUP BY` one column and `GROUP BY` two columns: one result row per
  group.
- `HAVING` for filtering groups, and why it can't be replaced by `WHERE`.
- `WHERE` and `HAVING` in the same query, each doing its own job.
- Conditional aggregation with `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` to
  count only some rows per group without losing the others.

## Concepts Refresher

### Aggregates collapse many rows into one value

An aggregate function takes a whole column's worth of values and returns
one value:

| Function | Returns | Ignores `NULL`? |
|---|---|---|
| `COUNT(*)` | number of rows | nothing to ignore: counts rows, not values |
| `COUNT(col)` | number of non-`NULL` values in `col` | yes |
| `COUNT(DISTINCT col)` | number of different non-`NULL` values | yes |
| `SUM(col)` | total | yes |
| `AVG(col)` | mean | yes |
| `MIN(col)`, `MAX(col)` | smallest, largest | yes |

Without `GROUP BY`, the whole table (after `WHERE`) is one group, so the
result is always exactly one row, however many aggregates you ask for:

```sql
SELECT MIN(temp_min_c), MAX(temp_max_c), ROUND(AVG(temp_max_c), 1)
FROM observations;
-- -4.1 | 17.9 | 12.8
```

The Python equivalent makes the "many rows in, one value out" shape
explicit:

```python
min(o["temp_min_c"] for o in observations)
```

### NULL inside aggregates

Two wind readings are `NULL`. `COUNT(*)` counts all 49 rows;
`COUNT(wind_ms)` counts 47, because it counts *values*, and a `NULL`
isn't one. The same rule applies to `AVG`: it's the sum of the known
values divided by the number of known values. For Kiruna:

```
known readings: 3.4 + 4.6 + 7.1 + 2.1 + 1.8 + 3.5 = 22.5 over 6 readings
AVG(wind_ms)     = 22.5 / 6 = 3.75
wrong: 22.5 / 7  = 3.21     (what you'd get by treating NULL as 0)
```

Skipping unknowns is usually what you want, since a broken sensor
doesn't mean the air was still. But an average built from fewer readings
is less trustworthy, which is why `q08` shows `COUNT(wind_ms)` next to
the average. If you ever do want a `NULL` treated as a value, say so
explicitly: `AVG(COALESCE(wind_ms, 0))` replaces each `NULL` with 0
first.

There's one more trap. Aggregating **zero rows** gives `COUNT` = 0, but
`SUM`, `AVG`, `MIN` and `MAX` return `NULL`, not 0: the sum of no numbers
is "nothing there", not zero, as far as SQL is concerned. A test in
`test_queries.py` shows this for Copenhagen, which has no observations.

### GROUP BY: one output row per group

`GROUP BY city_id` sorts the rows into buckets, one per distinct
`city_id`, and then evaluates every aggregate once *per bucket*:

```sql
SELECT city_id, ROUND(SUM(precipitation_mm), 1) AS total_mm
FROM observations
GROUP BY city_id;
```

That's exactly Week 4's dict-of-running-totals, done by the database:

```python
totals = {}
for o in observations:
    totals[o["city_id"]] = totals.get(o["city_id"], 0) + o["precipitation_mm"]
```

Two consequences follow from "one output row per group":

- **Only groups that exist get a row.** Copenhagen has no observations,
  so there's no `city_id = 8` bucket and no row for it. (Getting a row
  with 0 for it needs the other table: Week 21.) Likewise in `q10`, a
  city that never had snow gets no `(city, 'snow')` row, not a row with
  0.
- **Every column in `SELECT` must be grouped or aggregated.** In
  `SELECT city_id, SUM(precipitation_mm)`, `city_id` is the same for
  every row in a bucket, so it has one answer. If you added
  `observed_on`, which of the bucket's seven dates would it show?
  PostgreSQL and most other databases reject that query. SQLite accepts
  it and shows the value from an arbitrary row in the bucket, which is
  worse, because the output looks plausible. Don't rely on it.

`GROUP BY` can take several columns. `GROUP BY city_id, conditions`
makes one bucket per distinct *pair*, which is how `q10` counts each
city's sunny, cloudy, and rainy days separately.

### WHERE versus HAVING

Here's the full logical order of a query, extended from Week 19:

1. `FROM` — start with every row.
2. `WHERE` — drop individual **rows**.
3. `GROUP BY` — sort the surviving rows into buckets.
4. `HAVING` — drop whole **groups**.
5. `SELECT` — compute one output row per remaining group.
6. `ORDER BY`, then `LIMIT`.

`WHERE` runs before any groups exist, so it can only look at one row at
a time: `WHERE SUM(precipitation_mm) > 20` is an error, because there's
no sum yet. `HAVING` runs after grouping, so it can test aggregates.

`q07` uses both, and each does something the other can't:

```sql
SELECT city_id, COUNT(*) AS rainy_days
FROM observations
WHERE conditions = 'rain'      -- rows: keep only the rainy days
GROUP BY city_id               -- buckets: one per city
HAVING COUNT(*) >= 3           -- groups: keep cities with 3 or more
ORDER BY city_id;
```

If a condition only involves plain columns, put it in `WHERE`: filtering
rows before grouping means less work, and it reads as what it is.

The queries repeat the aggregate in `HAVING` (`HAVING
SUM(precipitation_mm) > 20`) rather than using its alias (`HAVING
total_mm > 20`). SQLite accepts the alias, but standard SQL doesn't,
because `HAVING` logically runs before `SELECT` gives the alias a name.
`ORDER BY` runs after `SELECT`, so aliases there are fine everywhere.

### Counting some rows per group: conditional aggregation

"How many frost nights did each city have?" looks like a job for `WHERE
temp_min_c < 0`, but that throws away every city without frost before
grouping, so they'd vanish from the result instead of showing 0. The fix
is to keep every row and count selectively inside the aggregate:

```sql
SUM(CASE WHEN temp_min_c < 0 THEN 1 ELSE 0 END) AS frost_nights
```

`CASE WHEN condition THEN a ELSE b END` is SQL's if-expression (like
Python's `a if condition else b`). Each row contributes 1 or 0, and the
sum is the count of matching rows, with non-matching cities getting 0.
You can put several of these side by side to build a small cross-tab in
one query.

### Rounding aggregates

`AVG` of `REAL` values gives long floating-point results
(`8.042857142857143`). The queries round with `ROUND(AVG(...), 2)` for
display. Round in the outermost expression only: rounding each value
before summing adds up the rounding errors.

## Design & Architecture

```
Week-20-sql-aggregates-and-grouping/
├── conftest.py                              - adds src/ to sys.path for pytest
├── src/
│   └── aggregates/
│       ├── __init__.py
│       ├── runner.py                        - open the database, load and run .sql files, format results
│       ├── cli.py                           - run a query by name, or an interactive SQL prompt
│       ├── data/
│       │   └── weather.sql                  - same data as Week 19
│       └── queries/
│           ├── q01_count_observations.sql   - one question per file, answered in SQL
│           ├── ...
│           └── q11_frost_nights_per_city.sql
└── tests/
    ├── test_queries.py                      - each query's exact expected result
    └── test_runner.py                       - the Python plumbing
```

Same structure and same data as Week 19, so the only new thing is the
SQL. `runner.py` and `cli.py` are copies of Week 19's (weeks stay
standalone), with the package name changed. `data/weather.sql` is
identical, so you can compare this week's summaries against the raw rows
you queried last week.

## How to Build & Run

```bash
cd Month-5-Databases-and-SQL/Week-20-sql-aggregates-and-grouping

# Run one of the bundled queries:
PYTHONPATH=src python3 -m aggregates.cli q07_cities_with_three_rainy_days

# Or open an interactive prompt:
PYTHONPATH=src python3 -m aggregates.cli
```

On Windows PowerShell: `$env:PYTHONPATH="src"`, then
`python -m aggregates.cli`. See Week 19's README for opening the data in a
graphical tool, and `../sql-playground/index.html` for the browser
version.

## Testing

```bash
cd Month-5-Databases-and-SQL/Week-20-sql-aggregates-and-grouping
python3 -m pytest -q
```

`test_queries.py` checks every query's exact result, in order. It also
pins down the behaviors this week is about: `COUNT(*)` versus
`COUNT(wind_ms)` (49 versus 47), `AVG` skipping `NULL` (Kiruna's 3.75,
not 3.21), aggregates over zero rows returning `NULL` rather than 0,
Copenhagen getting no group at all in `q05`, per-group counts adding up
to the table's 49 rows, and `q11` keeping frost-free cities with a count
of 0. `test_runner.py` covers the same Python plumbing as Week 19.

## Try It Yourself

1. For each date, show the average high across all cities and the number
   of cities that reported, in date order. Which day was coldest on
   average?
2. Show, for each city_id, the number of dry days (0 mm) and wet days
   (more than 0 mm) side by side in one row per city, using two `CASE`
   expressions. Check that the two columns add up to 7 for every city.
3. Find the cities whose *lowest* daily high of the week was still above
   13 degrees. Decide whether the condition belongs in `WHERE` or
   `HAVING`, and write down why the other one gives a different answer.
4. Using `COUNT(DISTINCT ...)`, find how many different kinds of weather
   each city had, and list only the cities that had three or more kinds.
5. Write a query that returns each city_id's average wind *treating
   missing readings as 0*, next to the correct average from `q08`. For
   which two cities do they differ, and which number would you put in a
   weather report?
