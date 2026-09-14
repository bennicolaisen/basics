# Authoring Guide (internal — for whoever builds a week's project)

Every week is a **complete, correct, already-working reference
project**, not a fill-in-the-blank stub. A student should be able to
clone it and immediately build it, run it, and see its tests pass.

## Required files per week

```
Month-N-.../Week-NN-slug/
├── README.md
└── (Python weeks)                      (Java weeks)
    ├── src/<package>/*.py              ├── pom.xml
    ├── tests/test_*.py                 ├── src/main/java/com/crashcourse/weekNN/**
    └── (no build tool needed;          └── src/test/java/com/crashcourse/weekNN/**
        stdlib + pytest only)
```

Python weeks: put importable code under `src/<package_name>/`, tests
under `tests/`, and include a minimal `pyproject.toml` or a `conftest.py`
that adds `src` to `sys.path` — whichever makes `pytest` runnable from the
project directory with zero extra flags. No third-party dependencies
beyond `pytest` itself.

Java weeks: copy `Laboration_1/pom.xml` (in the sibling
`teacher_repo_for_assignment` repo, already cloned locally) as the
starting point — same Java 17 target, same JUnit Jupiter version, same
plugin set. Change `groupId`/`artifactId`/`name`/`description` and the
package to `com.crashcourse.weekNN`.

## README.md template

Use this section order (skip "Design & Architecture" only for very small
single-file weeks; everything else applies every week):

1. `# Week N — Title`
2. `## Purpose` — 1 short paragraph, plain language, why this topic matters.
3. `## Objectives` — bullet list of concrete things the code demonstrates.
4. `## Concepts Refresher` — the actual teaching content. Write this
   assuming the reader half-remembers the topic and needs it rebuilt from
   first principles, not just a vocabulary reminder. This is the most
   important section — don't skimp on it. Use small code snippets inline
   where they clarify faster than prose.
5. `## Design & Architecture` — how the files relate, and why they're
   split that way. A short tree diagram like `Laboration_1/README.md`
   uses is good here.
6. `## How to Build & Run` — exact copy-pasteable commands.
7. `## Testing` — what's covered, how to run it (`pytest` / `mvn test`).
8. `## Try It Yourself` — 3–5 unsolved extension exercises, harder than
   what's implemented, no solutions given. These are for a student who
   already understands the reference code and wants fresh practice.
9. Optional `## Reflection` for weeks where a design trade-off is worth
   naming explicitly (matches `Laboration_1`'s closing section).

Tone: direct, precise, no filler, no marketing language. Explain the
*why*, not just the *what* — assume an intelligent reader who is rusty,
not one who is new. This matches `Laboration_1/README.md` in the sibling
repo — read it once before writing if you want the calibration.

## Code conventions

- Every function/class earns its existence — no speculative
  generalization, no unused parameters, no framework for a problem this
  small.
- Comments only where the *why* isn't obvious from good naming (mirror
  the root `CLAUDE.md`/system conventions: no restating what the code
  does).
- Validate inputs at the boundary (parsing, public API entry points);
  don't defensively check things that can't happen internally.
- Custom exceptions where the week is explicitly about exceptions
  (Weeks 13+); plain `ValueError`/`IndexError`/etc. elsewhere unless the
  week's topic is exceptions themselves.

## Before you're done

**Actually run the build and the tests and confirm they pass.**
Python: `cd <week-dir> && python -m pytest -q`.
Java: `cd <week-dir> && mvn -q clean test`.
A week isn't finished until this is verified green — don't hand back a
project you haven't actually executed.

Do not run any `git` commands (no `add`/`commit`/`push`) — just create
the files. Commits are handled centrally once every week is verified.
