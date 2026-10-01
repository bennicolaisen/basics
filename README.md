# Basics — A Coding Crash Course for Rusty Second-Years

## Who this is for

This is a from-scratch refresher for second-year CS students whose
fundamentals have gone shaky — the kind of gap where `for` loops, function
decomposition, or "wait, why does this recurse forever" have stopped being
automatic, and that's starting to get in the way of second-year coursework.

It assumes you've *seen* programming before (you're in a CS program, after
all) but re-teaches it from the ground up rather than assuming any of it is
solid. Nothing here is skipped as "too basic to cover."

The course runs for six months, one project per week:

| Months | Weeks | Part |
|---|---|---|
| 1–4 | 1–18 | Programming fundamentals: Python, data structures, OOP, Java, testing, debugging, Git, and a capstone |
| 5 | 19–24 | Databases and SQL, in three levels: beginner, intermediate, advanced |
| 6 | 25–26 | Web APIs: calling one, then building one on top of your own database |

The two halves use the same project format and build on each other: the
SQL weeks are written in the Python you rebuilt in Months 1–3, use the
testing habits from Month 4, and end with the database and API layers
that most real applications are made of.

**New here?** Start with [`GETTING_STARTED.md`](GETTING_STARTED.md) — clone,
open, run your first week's tests, in five steps.

**Working through this in IntelliJ?** See [`INTELLIJ_SETUP.md`](INTELLIJ_SETUP.md) —
the repo opens as one project with every Java week's tests and demo apps
already wired into the Run Configuration dropdown, so you can work
week-to-week without touching a terminal if you don't want to.

## How this course is built

Every week is a **complete, correct, runnable project** — not a blank
assignment with pieces missing. Clone it, build it, run it, read the code,
run the tests, and watch them pass. Each project's `README.md` follows the
same shape:

- **Purpose** — why this topic, in plain terms.
- **Objectives** — what the code concretely demonstrates.
- **Concepts Refresher** — the minimum background you need if the topic
  feels rusty, explained from first principles.
- **Design & Architecture** — how the code is put together and why.
- **How to Build & Run** — exact commands.
- **Testing** — what the test suite covers and how to run it.
- **Try It Yourself** — unsolved extension exercises, for once the reference
  code makes sense and you want to practice writing it yourself instead of
  reading it.

**Use it however fits:** read a project's README and code without touching
anything, to review a topic quickly. Or delete the implementation and
rebuild it yourself from the README's objectives, then diff against the
reference. Or just use the "Try It Yourself" section at the end of each
week as fresh, unsolved practice. All three are legitimate ways to use this
repo.

## Prerequisites

- **Python 3.10+** (Months 1–2, Week 9, and Months 5–6) — no third-party
  packages; everything uses the standard library and `pytest` for tests.
  That includes the databases and web servers in Months 5–6: SQLite ships
  with Python as the `sqlite3` module, and `http.server`/`urllib` cover
  HTTP.
- **Java 17** and **Maven** (Weeks 10–17) — Maven downloads the one
  dependency the Java weeks use (JUnit 5) by itself.
- A terminal and a text editor or IDE you're comfortable in. An IDE with a
  real debugger (IntelliJ, VS Code) matters more from Month 3 onward.

## Pacing

Twenty-six weeks, written as one project per week. That's a plan, not a
contract — go slower on weeks that expose a real gap, and faster on ones
that turn out to just be rust. If you need to compress, the
**capstone-adjacent** weeks (4, 8, 12, 17, 24, 26) are the ones least safe
to skip — they're where each month's pieces get put together.

Week 18 is the halfway point, where the programming fundamentals end
and the databases and APIs half begins (see "Where this leads"). The SQL weeks
are split into three levels of two weeks each (Weeks 19–20, 21–22,
23–24), so if time runs short you can stop after any level with a
complete, usable skill set, and still do Month 6's API weeks, which only
need Levels 1–2.

## Syllabus

### Month 1 — Foundations (Python)
*Getting the absolute basics automatic again: variables, control flow,
functions, the core collection types.*

| Week | Project | Topic |
|---|---|---|
| 1 | [`01-unit-converter-toolkit`](Month-1-Python-Foundations/Week-01-unit-converter-toolkit/) | Variables, types, expressions, formatted I/O, input validation |
| 2 | [`02-input-validators-and-games`](Month-1-Python-Foundations/Week-02-input-validators-and-games/) | Control flow: `if`/`elif`/`else`, `while`, `for`, `break`/`continue` |
| 3 | [`03-function-library`](Month-1-Python-Foundations/Week-03-function-library/) | Functions, parameters, scope, decomposing a monolithic script |
| 4 | [`04-text-analyzer`](Month-1-Python-Foundations/Week-04-text-analyzer/) | Core collections: `list`, `dict`, `set`, `tuple`, comprehensions |

### Month 2 — Recursion & Data Structures (Python)
*The two things that usually explain "I understood this once and now I
don't": recursion, and what a data structure actually is under the hood.*

| Week | Project | Topic |
|---|---|---|
| 5 | [`05-recursion-basics`](Month-2-Recursion-and-Data-Structures/Week-05-recursion-basics/) | Recursion I: base/recursive cases, the call stack, tracing |
| 6 | [`06-backtracking-puzzles`](Month-2-Recursion-and-Data-Structures/Week-06-backtracking-puzzles/) | Recursion II: backtracking, search-and-undo |
| 7 | [`07-diy-data-structures`](Month-2-Recursion-and-Data-Structures/Week-07-diy-data-structures/) | Building a linked list, stack, and queue from nothing |
| 8 | [`08-search-and-sort`](Month-2-Recursion-and-Data-Structures/Week-08-search-and-sort/) | Searching, sorting, and Big-O intuition |

### Month 3 — OOP & the Jump to Java
*From "a program is a sequence of steps" to "a program is a set of
objects that collaborate" — and from Python's dynamic typing to Java's
static, compiled world.*

| Week | Project | Topic |
|---|---|---|
| 9 | [`09-oop-bank-simulation`](Month-3-OOP-and-Java-Bridge/Week-09-oop-bank-simulation/) | OOP in Python: classes, encapsulation, composition |
| 10 | [`10-java-bridge`](Month-3-OOP-and-Java-Bridge/Week-10-java-bridge/) | The Java bridge: static typing, compiling, Maven, `main` |
| 11 | [`11-java-oop-shapes`](Month-3-OOP-and-Java-Bridge/Week-11-java-oop-shapes/) | Java OOP: interfaces, abstract classes, inheritance, polymorphism |
| 12 | [`12-java-collections-catalog`](Month-3-OOP-and-Java-Bridge/Week-12-java-collections-catalog/) | The Collections Framework, generics, `Comparable`/`Comparator` |

### Month 4 — Testing, Debugging, Git & Capstone
*The professional habits around the code — testing it, debugging it when
it's wrong, collaborating on it — plus a capstone that pulls Months 1–4
together into one multi-class application.*

| Week | Project | Topic |
|---|---|---|
| 13 | [`13-java-exceptions-parser`](Month-4-Testing-Debugging-and-Capstone/Week-13-java-exceptions-parser/) | Exceptions, defensive programming, resilient parsing |
| 14 | [`14-java-junit-testing`](Month-4-Testing-Debugging-and-Capstone/Week-14-java-junit-testing/) | JUnit 5 in depth, assertions, TDD |
| 15 | [`15-debugging-clinic`](Month-4-Testing-Debugging-and-Capstone/Week-15-debugging-clinic/) | Systematic debugging: stack traces, breakpoints, bisection |
| 16 | [`16-git-workflow-lab`](Month-4-Testing-Debugging-and-Capstone/Week-16-git-workflow-lab/) | Git & collaboration: branches, merges, conflicts, PRs |
| 17–18 | [`17-capstone-library-system`](Month-4-Testing-Debugging-and-Capstone/Week-17-capstone-library-system/) | Capstone: a full library management system |

### Month 5 — Databases & SQL (Python + SQLite)
*From "the data lives in a list" to "the data lives in a database": asking
questions of it, combining it, changing it safely, analysing it, and
making the database itself enforce the rules. Three levels, all on one
dataset of Nordic weather (and, in Level 3, a shop that sells weather
gear). For instant-feedback practice alongside the weeks, open
[`sql-playground/index.html`](Month-5-Databases-and-SQL/sql-playground/index.html)
in a browser.*

| Week | Level | Project | Topic |
|---|---|---|---|
| 19 | 1 · Beginner | [`19-sql-select-basics`](Month-5-Databases-and-SQL/Week-19-sql-select-basics/) | `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, `NULL` |
| 20 | 1 · Beginner | [`20-sql-aggregates-and-grouping`](Month-5-Databases-and-SQL/Week-20-sql-aggregates-and-grouping/) | Aggregates, `GROUP BY`, `HAVING` |
| 21 | 2 · Intermediate | [`21-sql-joins-and-keys`](Month-5-Databases-and-SQL/Week-21-sql-joins-and-keys/) | Keys, normalization, `JOIN`, `LEFT JOIN`, subqueries |
| 22 | 2 · Intermediate | [`22-sqlite-weather-log`](Month-5-Databases-and-SQL/Week-22-sqlite-weather-log/) | Writing data from Python: constraints, transactions, parameters |
| 23 | 3 · Advanced | [`23-sql-analytics-and-window-functions`](Month-5-Databases-and-SQL/Week-23-sql-analytics-and-window-functions/) | Analytics: CTEs, window functions, `EXISTS`, the fan-out trap |
| 24 | 3 · Advanced | [`24-sql-business-logic`](Month-5-Databases-and-SQL/Week-24-sql-business-logic/) | Business logic in the database: triggers, views, upserts |

### Month 6 — Web APIs (Python)
*How programs talk to each other over the network: first as a client
calling someone else's API, then as the server, with Week 22's weather
log behind it.*

| Week | Project | Topic |
|---|---|---|
| 25 | [`25-how-apis-work`](Month-6-APIs/Week-25-how-apis-work/) | HTTP, JSON, status codes, calling an API from Python |
| 26 | [`26-build-a-rest-api`](Month-6-APIs/Week-26-build-a-rest-api/) | Building a REST API: routing, validation, status codes |

## Where this leads

At the halfway point, after Week 18, a good gut-check is to reread the
"Concepts Refresher" sections of Months 1–3: if they read as reminders
rather than new material, the fundamentals part of this course did its
job.

After Week 26 you have the pieces of most real applications: a database,
the SQL to query and protect it, and an API in front of it. A good next
project is to put them together yourself, for example a weather app that
fetches forecasts from a public API, stores them in SQLite, and serves
its own summary API.
