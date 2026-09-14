# Week 13 — Exceptions, Defensive Programming, Resilient Parsing

## Purpose

Real input is never as clean as the examples in a textbook. A CSV file a
user hands you will have a blank line in it, or a typo where a number
should be, or the wrong number of columns on line 4,317 of 5,000. This week
is about the machinery Java gives you for that reality — exceptions — and,
more importantly, about a design decision every program that processes a
batch of anything eventually has to make: when one item in the batch is
bad, do you stop everything, or do you note the problem and keep going?
Both are correct answers, depending on context, and this project builds
both so the difference is concrete rather than theoretical.

## Objectives

The code in this project demonstrates:

- A custom **checked** exception (`MalformedRecordException`) and why it is
  checked on purpose, not by default.
- Constructor validation on an immutable POJO (`CsvRecord`) that makes an
  invalid instance impossible to create.
- **Fail-fast** parsing of a single line (`CsvRecordParser`), which throws
  immediately with a message naming the exact problem.
- **Resilient batch** parsing of a whole file (`BatchParser`), which
  collects both the records that parsed and the lines that didn't, instead
  of aborting on the first bad line.
- `try`/`catch`/`finally` and try-with-resources used for their actual
  purpose, not just as syntax to memorize.

## Concepts Refresher

### Checked vs. unchecked exceptions

Java has two families of things you can `throw`:

- **Unchecked exceptions** (`RuntimeException` and its subclasses, like
  `IllegalArgumentException` or `NumberFormatException`) don't have to be
  declared or caught. The compiler lets you ignore them completely — if
  they happen at runtime and nothing catches them, the program crashes.
  They're for programming mistakes: passing `null` where it's not allowed,
  indexing past the end of an array. The fix for those is to fix the
  calling code, not to catch the exception.
- **Checked exceptions** (`Exception` and its subclasses, *excluding*
  `RuntimeException`) are different: if a method's signature says
  `throws SomeCheckedException`, every caller is **forced**, at compile
  time, to either catch it or declare that it throws it too. The compiler
  will not let you forget about it.

That compiler-enforced attention is the entire point of making
`MalformedRecordException` checked instead of unchecked. A malformed line
in a CSV file isn't a bug in *this* program — it's an entirely expected
possibility of reading data that came from somewhere else. When
`CsvRecordParser.parseLine(...)` declares `throws MalformedRecordException`,
every single caller is forced to decide, right there at the call site, what
happens when a line is bad. They can't accidentally forget, the way you
easily could with an unchecked exception that only shows up the first time
someone actually feeds it bad data in production. `BatchParser` is that
decision, made concrete: it catches the exception per line and keeps going.
A different caller might legitimately choose to let it propagate instead —
checked exceptions don't dictate the choice, they just make sure a choice
gets made.

By contrast, `CsvRecord`'s constructor throws the *unchecked*
`IllegalArgumentException` when, say, `age` is negative. That's deliberate
too: those checks guard a contract on `CsvRecord` itself ("you may never
have an instance in an invalid state"), not a fact about external input,
and requiring every piece of code anywhere in a program that ever
constructs a `CsvRecord` to declare or catch something would be noise, not
safety. `CsvRecordParser` catches that `IllegalArgumentException` internally
and re-throws it as the checked `MalformedRecordException`, because *from
its caller's point of view*, the record came from external, possibly-bad
input — the checked/unchecked distinction follows *who the exception is
for*, not just *what went wrong*.

### `try`/`catch`/`finally`

```java
try {
    riskyThing();
} catch (SomeException e) {
    // runs only if riskyThing() threw a SomeException (or a subclass)
} finally {
    // always runs — whether the try block finished normally, threw an
    // exception that was caught above, or threw one that wasn't
}
```

`finally` is for cleanup that has to happen no matter what — closing a
file, releasing a lock — because a `return` or an uncaught exception inside
`try`/`catch` would otherwise skip past it.

### try-with-resources

Before try-with-resources existed, closing a resource safely meant writing
this by hand, every time:

```java
BufferedReader reader = Files.newBufferedReader(path);
try {
    // use reader
} finally {
    reader.close();
}
```

Try-with-resources does that for you:

```java
try (BufferedReader reader = Files.newBufferedReader(path)) {
    // use reader
}
```

Anything declared in the parentheses that implements `AutoCloseable` gets
its `close()` called automatically when the block exits — normally *or* via
an exception — without you writing a `finally` block. `BatchParser` uses
exactly this pattern to guarantee the file is closed even if something
unexpected happens while reading it.

### Collect-and-continue vs. fail-fast

The core design point of this project is that **both** of these are
correct, depending on scope:

- `CsvRecordParser.parseLine(...)` is about **one** record. If it's bad,
  there is nothing sensible to return, so it throws immediately — the
  caller finds out right away and decides what to do.
- `BatchParser.parseFile(...)` is about a **whole file** of records. If
  line 42 is bad, aborting the entire file means the 41 good records
  before it, and every good record after it, get thrown away too. For a
  batch, "note the problem, keep the good data, report everything at the
  end" is almost always more useful than "stop at the first error." The
  same underlying exception is used both ways — the difference is entirely
  in what the *caller* of the parsing logic decides to do with it.

## Design & Architecture

```
com.crashcourse.week13
├── MalformedRecordException   - checked exception: one bad line
├── CsvRecord                   - immutable, self-validating record
├── CsvRecordParser              - fail-fast: one line -> one CsvRecord
├── ParseError                   - line number + message, for batch reporting
├── BatchParseResult             - a whole file's outcome: records + errors
└── BatchParser                  - resilient: one file -> BatchParseResult
```

`CsvRecord` cannot exist in an invalid state — its constructor validates
every field and throws `IllegalArgumentException` if any of them are
unacceptable, so once you're holding a `CsvRecord`, no further defensive
checks are needed anywhere else in the program. `CsvRecordParser` sits in
front of it, translating the raw text concerns (wrong column count,
non-numeric age) and `CsvRecord`'s own validation failures alike into one
consistent, checked `MalformedRecordException` with a message that always
names the specific problem. `BatchParser` is the only class that catches
that exception — everywhere else, letting it propagate is the right
behavior.

Expected line format: `name,age,email,department` — e.g.
`Alice,30,alice@example.com,Engineering`.

## How to Build & Run

```bash
mvn clean verify
java -jar target/week13.jar path/to/data.csv
```

`BatchParser.main` prints every successfully parsed record, followed by
every line that failed and why.

## Testing

Unit tests (JUnit 5) live under `src/test/java` and exercise:

- `CsvRecordParserTest` — a well-formed line; trimming of surrounding
  whitespace; and one test per malformed case (wrong column count,
  non-numeric age, negative age, blank name, invalid email, empty line),
  each asserting that the exception's message actually names the specific
  problem, not just "invalid line".
- `BatchParserTest` — an empty file; a file of only good lines; blank
  lines being skipped rather than reported; and a file mixing good and bad
  lines, asserting the good ones parsed correctly *and* the bad ones are
  reported with the correct line number, without either side being lost.

```bash
mvn -q clean test
```

## Try It Yourself

1. Add a fifth CSV field, `salary`, which must parse as a non-negative
   `double`. Update `CsvRecord`, `CsvRecordParser`, and write new tests for
   the failure cases you introduce.
2. Add a `MalformedRecordException` subclass per failure category (e.g.
   `WrongColumnCountException`, `InvalidAgeException`) so callers can
   `catch` specific problems differently if they want to — then decide for
   yourself whether that's actually an improvement here, or unnecessary
   ceremony for this project's size.
3. Change `BatchParser.parseFile` to also accept a `Predicate<CsvRecord>`
   filter, only keeping records that satisfy it — without changing how
   malformed lines are handled.
4. Write a method that takes a `BatchParseResult` and a `Path`, and writes
   a small text report to that file summarizing how many records parsed,
   how many failed, and the full list of errors.
5. Currently a blank line is silently skipped. Make that behavior
   configurable — add an overload of `parseFile` that takes a `boolean
   strict` flag, where `strict = true` reports a blank line as an error
   instead of skipping it. Write tests for both behaviors.

## Reflection

`CsvRecordParser` and `BatchParser` both call the exact same underlying
validation logic, yet behave completely differently on bad input — one
throws immediately, the other never lets a single bad line stop it. That
isn't two competing designs where one is "right"; it's the same tool aimed
at two different scopes. Recognizing which scope you're in — "I need to
know right now whether this one thing is valid" versus "I'm processing a
batch and one bad item shouldn't cost me all the good ones" — is a design
judgment call you'll keep making throughout Month 4, and it's exactly the
kind of decision a checked exception forces you to make consciously
instead of by accident.
