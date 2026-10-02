# Week 16 — Git & Collaboration: Branches, Merges, Conflicts, PRs

## Purpose

Code you write alone, on one branch, forever, doesn't exist in the real
world. The moment more than one person (or even just past-you and
present-you, working on two things at once) touches the same project, git
stops being "a way to save snapshots" and becomes the tool that makes
working in parallel possible at all — including the part everyone dreads
a little: two changes landing on the exact same lines. This week's project
is small on purpose (`NotesApp`, a console app for jotting down and
finding short notes) because the *point* this week is the git workflow
around it, not the app.

## Objectives

- Understand git's actual model: commits as snapshots, branches as movable
  pointers, `HEAD` as "where you are right now."
- Know the difference between merge and rebase and when each is the right
  tool.
- Create a real merge conflict on purpose, read its conflict markers, and
  resolve it by hand.
- Understand what a pull request is *for* as a review and collaboration
  mechanism, even without an actual remote in this exercise.
- Exercise all of this against `NotesApp`'s real logic (`Note`,
  `NoteStore`) and its JUnit 5 test suite.

## Concepts Refresher

### Git's actual model

- **A commit is a snapshot**, not a diff. Every commit records the
  complete state of every tracked file at that point, plus a pointer to
  its parent commit(s). (Git *displays* diffs between commits for your
  convenience, and stores things efficiently under the hood, but
  conceptually each commit is a full picture of the project at that
  moment.)
- **A branch is just a movable pointer** to one commit — the *tip* of that
  branch. `git checkout -b feature/x` doesn't copy anything; it creates a
  new pointer at your current commit and starts moving *that* pointer
  forward as you commit, leaving the original branch's pointer exactly
  where it was.
- **`HEAD` is "where you currently are"** — normally a pointer to
  whichever branch you have checked out, which is itself a pointer to a
  commit. `git checkout main` moves `HEAD` to point at `main`; committing
  afterward moves `main`'s pointer forward and `HEAD` moves right along
  with it, since `HEAD` is just following the branch.

### Merge vs. rebase

Both combine work from two branches, but they produce different history:

- **`git merge feature`** (run while on `main`) creates a new **merge
  commit** with two parents: the tip of `main` and the tip of `feature`.
  Both branches' full histories stay exactly as they happened, side by
  side, joined by one new commit. Nothing is rewritten — this is the
  safer default, especially on a branch anyone else might also be working
  from.
- **`git rebase main`** (run while on `feature`) takes every commit unique
  to `feature` and **replays** it, one at a time, on top of `main`'s
  current tip — as if you'd started your branch from there in the first
  place. History ends up linear (no merge commit), but every replayed
  commit is technically a *new* commit with a new hash. That's exactly
  why you should never rebase a branch other people have already pulled
  and built on top of — you'd be rewriting commits out from under them.

A reasonable default: merge for combining a finished feature branch back
into a shared branch (what this exercise does); rebase for tidying up your
*own*, still-private branch before anyone else has seen it.

### What a merge conflict actually is

A conflict happens when git tries to combine two branches and finds that
**both changed the same lines of the same file since they diverged** — and
git has no way to know which version (or what combination) you actually
want. Git resolves everything it safely can on its own; only the
genuinely overlapping lines get left for you, marked directly in the file:

```
<<<<<<< HEAD
(the version from the branch you're currently on)
=======
(the version from the branch being merged in)
>>>>>>> feature/add-tag
```

`<<<<<<< HEAD` through `=======` is *your current branch's* version of
those lines; `=======` through `>>>>>>> feature/add-tag` is the *incoming*
branch's version. Resolving a conflict means editing that region down to
what the code should actually be — which might be one side, the other
side, or (as in this week's exercise) a combination of both — and then
removing the marker lines entirely, since they're not valid Java.

### What a pull request is for

A pull request (PR) is a request to merge one branch into another,
opened *before* the merge happens, so other people can review the change
first — read the diff, leave comments on specific lines, request changes,
and only then approve. It's a collaboration and quality gate layered on
top of the plain git mechanics above, not a different way of combining
branches: under the hood, clicking "merge" on a PR runs the same `merge`
(or sometimes rebase, depending on the project's settings) you're about to
do by hand in this exercise. This project has no real remote to open an
actual PR against, but the underlying merge — and the conflict it can
produce — is identical to what you'd hit inside one.

## Design & Architecture

```
com.crashcourse.week16
├── Note         - immutable: id, createdAt, text
├── NoteStore     - in-memory notes + add/list/search/delete + file persistence
└── NotesApp       - console front end (add/list/search/delete/quit)
```

`Note` is a plain, validated value; `NoteStore` owns the collection and
the id/persistence logic; `NotesApp` is a thin loop translating typed
commands into `NoteStore` calls. Kept small deliberately — the git
exercise below is this week's real content.

## How to Build & Run

```bash
mvn clean verify
java -jar target/week16.jar
```

Commands once running: `add`, `list`, `search`, `delete`, `quit` (which
also saves to `notes.txt` in the current directory).

## Testing

```bash
mvn -q clean test
```

Covers `Note`'s validation and `NoteStore`'s id assignment, listing order,
case-insensitive search, deletion (both the found and not-found cases),
and save/load round-tripping — including that loading an existing file
correctly continues the id sequence instead of colliding with it.

## Try It Yourself: the guided merge-conflict exercise

> **Facit (answer key):** every exercise below is solved, tested and explained
> in Swedish in [FACIT.md](FACIT.md). Try each one yourself first, then compare.

This is the actual exercise for the week. Do it inside your own clone of
this project (a scratch copy is fine — this isn't about preserving
history, it's about *causing* a conflict and living through resolving it).
Run `git status` first and make sure your working tree is clean before you
start.

**1. Create a feature branch.**

```bash
git checkout -b feature/add-tag
```

**2. On `feature/add-tag`, apply this change to
`src/main/java/com/crashcourse/week16/Note.java`.** It adds an optional
`tag` field without touching any other file — the existing three-argument
constructor keeps working via delegation, so nothing elsewhere in the
project needs to change.

Replace the constructor and the three accessor methods below it with:

```java
    private final String tag;

    public Note(int id, Instant createdAt, String text) {
        this(id, createdAt, text, null);
    }

    public Note(int id, Instant createdAt, String text, String tag) {
        if (id <= 0) {
            throw new IllegalArgumentException("Note id must be positive, got " + id);
        }
        if (createdAt == null) {
            throw new IllegalArgumentException("createdAt must not be null");
        }
        if (text == null || text.isBlank()) {
            throw new IllegalArgumentException("Note text must not be blank");
        }
        if (text.contains("\n")) {
            throw new IllegalArgumentException("Note text must not contain newlines");
        }
        this.id = id;
        this.createdAt = createdAt;
        this.text = text;
        this.tag = tag;
    }

    public int id() {
        return id;
    }

    public Instant createdAt() {
        return createdAt;
    }

    public String text() {
        return text;
    }

    public String tag() {
        return tag;
    }
```

(Remember to add the `private final String tag;` field declaration next
to the existing three fields — it's included above at the top of the
block for convenience.)

And replace the `toString` method with:

```java
    @Override
    public String toString() {
        return tag == null
            ? "[%d] %s - %s".formatted(id, createdAt, text)
            : "[%d] (%s) %s - %s".formatted(id, tag, createdAt, text);
    }
```

Then commit:

```bash
git add src/main/java/com/crashcourse/week16/Note.java
git commit -m "Add optional tag field to Note"
```

**3. Switch back to `main`** and simulate a teammate's unrelated,
concurrent change to the very same file — a small readability tweak to
drop the timestamp from the display:

```bash
git checkout main
```

Replace `Note.java`'s `toString` method (still the original, untouched
three-argument-only version on this branch) with:

```java
    @Override
    public String toString() {
        return "[%d] %s".formatted(id, text);
    }
```

Commit it:

```bash
git add src/main/java/com/crashcourse/week16/Note.java
git commit -m "Simplify Note's toString to omit the timestamp"
```

**4. Merge the feature branch into `main`.**

```bash
git merge feature/add-tag
```

Git will report a conflict:

```
Auto-merging src/main/java/com/crashcourse/week16/Note.java
CONFLICT (content): Merge conflict in src/main/java/com/crashcourse/week16/Note.java
Automatic merge failed; fix conflicts and then commit the result.
```

Every other change from `feature/add-tag` (the new field, the delegating
constructor, the `tag()` accessor) merges in cleanly on its own — `main`
never touched those lines. Only `toString`'s `return` line conflicts,
because **both branches changed that exact line since they diverged**.
Opening `Note.java` now, you'll see something like:

```java
    @Override
    public String toString() {
<<<<<<< HEAD
        return "[%d] %s".formatted(id, text);
=======
        return tag == null
            ? "[%d] %s - %s".formatted(id, createdAt, text)
            : "[%d] (%s) %s - %s".formatted(id, tag, createdAt, text);
>>>>>>> feature/add-tag
    }
```

**5. Resolve it by hand.** Neither side alone is what you actually want —
`main`'s version drops the timestamp (worth keeping) but knows nothing
about tags; `feature/add-tag`'s version knows about tags but keeps the
timestamp you just decided to drop. Combine both intents and delete the
marker lines entirely:

```java
    @Override
    public String toString() {
        return tag == null
            ? "[%d] %s".formatted(id, text)
            : "[%d] (%s) %s".formatted(id, tag, text);
    }
```

**6. Complete the merge.**

```bash
git add src/main/java/com/crashcourse/week16/Note.java
git commit
```

Git pre-fills a merge commit message for you (`Merge branch
'feature/add-tag'`) — accepting it as-is is fine.

**7. Verify.** Run the test suite again:

```bash
mvn -q clean test
```

Everything should still pass unchanged — the existing tests never
reference `tag`, and the delegating three-argument constructor kept every
existing call site compiling throughout. Then, on your own, add at least
one new test for the tagged constructor and `tag()` accessor, and confirm
`toString()` produces the combined format you resolved the conflict to.

## Reflection

Notice what git did and didn't need help with: every line only one branch
touched merged automatically, with no input from you at all — git is
genuinely good at that part. The one line both branches changed is the
*only* place a human had to make a judgment call, because only a human
could know that the "right" answer was neither side alone, but a
combination of both. That's the actual shape of merge conflicts in
practice: rare relative to how much code merges cleanly, but exactly the
moments where two people's independent intentions need someone to
reconcile them on purpose.
