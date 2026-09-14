# Working Through This Course in IntelliJ

This repository is set up to open as **one IntelliJ project**, with every
Java week already wired into the Run Configurations dropdown so you can
run a week's tests (or its demo app) in one click instead of hunting
through folders and typing Maven commands.

## One-time setup

1. **Clone the repo, then open it in IntelliJ**: `File > Open...` and
   select the repository's root folder (the one containing `pom.xml` and
   this file) — not any individual week's folder.
2. IntelliJ will detect the root `pom.xml` and offer to **"Load Maven
   Project"** — accept it. This imports all eight Java weeks (10–17) as
   modules in one project. Give it a minute the first time; it's
   downloading each week's dependencies (just JUnit 5 — nothing heavy).
3. Open the **Run Configuration dropdown** in the top toolbar (next to the
   ▶ and 🐞 icons). Every week already has one or two entries there:
   - `Week NN - Run Tests` — runs that week's full test suite. This is
     your main "did I get it right" loop for every Java week.
   - `Week NN - Run App (ClassName)` — runs that week's demo entry point
     where one exists, so you can see the thing actually work, not just
     watch tests pass.
   - `00 All Weeks - Run All Java Tests` — runs every Java week's tests
     in one go (handy after pulling updates, to confirm nothing broke).

   Pick one, hit ▶. Output shows in the Run tool window at the bottom.

4. **Python weeks (1–9)** aren't part of the Maven project — they're
   plain Python and don't need to be. Two ways to work with them in
   IntelliJ:
   - **With the Python plugin** (bundled in IntelliJ Ultimate; installable
     for free in IntelliJ Community via `Settings > Plugins > Marketplace
     > "Python Community Edition"`): open a week's folder, right-click its
     `src/` folder and choose **Mark Directory as > Sources Root** (this
     is what makes `from <package> import ...` resolve cleanly instead of
     showing a false "unresolved reference"), then right-click the
     `tests/` folder and choose **Run 'pytest in tests'**. IntelliJ will
     prompt you to select a Python interpreter the first time — any
     Python 3.10+ interpreter works, no packages beyond `pytest` are
     needed (`pip install pytest` if you don't have it).
   - **Without any plugin, from a terminal** (always works, no IDE setup
     required): open IntelliJ's built-in terminal (`Alt+F12` /
     `View > Tool Windows > Terminal`), `cd` into the week's folder, and
     run `python -m pytest -q`. This is the same command the reference
     solutions were verified with.

## Working through a week

Each week's folder has its own `README.md` — that's the actual lesson.
Read it top to bottom (**Concepts Refresher** is the real teaching
content, not filler), then look at the code with the README's
**Design & Architecture** section as your map. Run its tests to see the
reference implementation verified correct. Then use the **Try It
Yourself** section at the end — those exercises are unsolved on purpose.

Suggested loop per week:

1. Read the week's `README.md`.
2. Run `Week NN - Run Tests` (or `pytest`) and watch it pass — confirms
   your environment is set up correctly before you dig into the code.
3. Read the source with the tests open side-by-side — the tests are
   usually the fastest way to see what a function is actually supposed
   to do.
4. Do the **Try It Yourself** exercises in a scratch file or a new
   branch — nothing in this repo depends on you not touching the
   reference code, so feel free to experiment directly in it too.
5. Move to the next week.

## If a Run Configuration doesn't show up

IntelliJ sometimes needs a nudge to notice new Maven modules or shared
run configurations after a fresh clone:
`File > Reload All Maven Projects` (via the Maven tool window's refresh
icon) re-imports the modules; restarting IntelliJ picks up anything in
`.idea/runConfigurations/` that didn't load. As a fallback that always
works regardless of IDE state, every Java week can be run directly from
IntelliJ's terminal: `cd <week folder> && mvn clean test`.
