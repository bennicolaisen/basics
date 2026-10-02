# Authoring Guide (internal — for whoever builds a week's project)

Every week is a **complete, correct, already-working reference
project**, not a fill-in-the-blank stub. A student should be able to
clone it and immediately build it, run it, and see its tests pass.

The course assumes **no prior programming experience**. Weeks 1–4 are
written in Swedish for complete beginners; Weeks 5–26 are written in
English. Every exercise in every week has a tested answer key (facit),
explained in Swedish.

## Required files per week

### Weeks 1–4 (Swedish, beginner format)

```
Month-1-.../Week-0N-slug/
├── README.md              lesson in small steps, each ending with "Öva:" exercises
├── conftest.py            src/ on sys.path, the --facit option, fixtures `ovning` and `kor`
├── pytest.ini             testpaths = tests, addopts = --tb=short
├── starta.py              runs the week's project
├── src/<package>/*.py     the week's project
├── tests/test_*.py        tests for the project and for facit/prova_sjalv.py
├── ovningar/NN_name.py    one stub per exercise, with instructions in a comment
├── kontroll/test_ovningar.py   checks the student's ovningar/ files
├── facit/NN_name.py       a solution for every exercise
├── facit/prova_sjalv.py   solutions for "Prova själv"
└── FACIT.md               every solution explained
```

`python -m pytest kontroll -k 05` checks one exercise;
`python -m pytest kontroll --facit` runs the same checks against
`facit/`, which proves the answer key passes. Keep pytest's output
readable for a beginner: `PYTEST_DONT_REWRITE` in the kontroll module and
`--tb=short`.

README headings, in order: `## Syfte`, `## Mål`, `## Genomgång` (with
`### Steg N` and an "Öva:" list after each step), `## Veckans projekt: …`,
`## Köra programmet`, `## Testa`, `## Prova själv`, `## Facit`.

### Weeks 5–26

```
Month-N-.../Week-NN-slug/
├── README.md
├── FACIT.md                                  (Swedish answer key, see below)
└── (Python weeks)                      (Java weeks)
    ├── src/<package>/*.py              ├── pom.xml
    ├── tests/test_*.py                 ├── src/main/java/com/crashcourse/weekNN/**
    ├── tests/test_facit.py             ├── src/main/java/com/crashcourse/weekNN/facit/**
    └── facit/                          ├── src/test/java/com/crashcourse/weekNN/**
                                        └── src/test/java/com/crashcourse/weekNN/facit/FacitTest.java
```

Python weeks: put importable code under `src/<package_name>/`, tests
under `tests/`, and include a `conftest.py` that adds `src` to
`sys.path`, so that `pytest` runs from the project directory with zero
extra flags. No third-party dependencies beyond `pytest` itself.

Java weeks: copy an existing Java week's `pom.xml` (Week 10's, for
example) as the starting point: same Java 17 target, same JUnit Jupiter
version, same plugin set. Change `groupId`/`artifactId`/`name`/`description` and the
package to `com.crashcourse.weekNN`.

## README.md template (Weeks 5–26)

Use this section order (skip "Design & Architecture" only for very small
single-file weeks; everything else applies every week):

1. `# Week N — Title`
2. `## Purpose` — 1 short paragraph, plain language, why this topic matters.
3. `## Objectives` — bullet list of concrete things the code demonstrates.
4. `## Concepts Refresher` — the actual teaching content. Build the topic
   from first principles; the reader has only the earlier weeks of this
   course behind them. This is the most important section — don't skimp
   on it. Use small code snippets inline where they clarify faster than
   prose.
5. `## Design & Architecture` — how the files relate, and why they're
   split that way. A short tree diagram, like the existing weeks use, is
   good here.
6. `## How to Build & Run` — exact copy-pasteable commands.
7. `## Testing` — what's covered, how to run it (`pytest` / `mvn test`).
8. `## Try It Yourself` — 3–5 extension exercises, harder than what's
   implemented. Start the section with the standard note linking
   `FACIT.md`.
9. Optional `## Reflection` for weeks where a design trade-off is worth
   naming explicitly.

Tone: direct, precise, no filler, no marketing language. Explain the
*why*, not just the *what*. Read an existing week's README (Week 4 or
Week 17, say) once before writing if you want the calibration.

## The answer key (facit)

Every Try It exercise gets a solution that **runs and is tested**, and an
explanation in `FACIT.md`, written in Swedish (English technical terms are
fine, explained where they first appear).

- **Python weeks:** solutions in `facit/` (`facit/prova_sjalv.py`, or
  modules that reuse the week's code and add only what the exercise asks
  for). Tests in `tests/test_facit.py`, which run with the rest of the
  week.
- **SQL weeks:** one `.sql` file per answer in `facit/`, runnable with
  `python3 facit/kor.py [prefix]`, checked row for row in
  `tests/test_facit.py`.
- **Java weeks:** a `com.crashcourse.weekNN.facit` package. When the
  exercises change the week's classes, the package holds full solved
  copies; otherwise only the new classes. Tests in `facit/FacitTest.java`,
  so `mvn test` checks them.

`FACIT.md` explains **how to think**, not just what to type: the decision
behind each answer, the tempting wrong version and why it fails, and the
edge cases the tests pin down. When an exercise is ambiguous or doesn't
fit the code as written, say so and explain the interpretation chosen.

## Glossary

Every new term a week introduces belongs in `ordlista/termer.json`
(English term, Swedish translation, Swedish explanation, week). Run
`python ordlista/bygg.py` to regenerate `ORDLISTA.md` and
`ordlista/index.html`, and `python -m pytest ordlista` to check that
they're up to date.

## Code conventions

- Every function/class earns its existence — no speculative
  generalization, no unused parameters, no framework for a problem this
  small.
- Comments only where the *why* isn't obvious from good naming.
- Validate inputs at the boundary (parsing, public API entry points);
  don't defensively check things that can't happen internally.
- Custom exceptions where the week is explicitly about exceptions
  (Weeks 13+); plain `ValueError`/`IndexError`/etc. elsewhere unless the
  week's topic is exceptions themselves.

## Before you're done

**Actually run the build and the tests and confirm they pass,** facit
included.
Python: `cd <week-dir> && python -m pytest -q`.
Weeks 1–4 also: `python -m pytest kontroll --facit`.
Java: `cd <week-dir> && mvn -q clean test`.
Glossary: `python -m pytest ordlista`.
A week isn't finished until this is verified green — don't hand back a
project you haven't actually executed.

Do not run any `git` commands (no `add`/`commit`/`push`) — just create
the files. Commits are handled centrally once every week is verified.
