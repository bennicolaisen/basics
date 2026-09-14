# Week 14 — JUnit 5 In Depth

## Purpose

Week 11's tests were mostly `@Test` and `assertEquals`, enough to get by.
This week is about actually knowing the tool: writing tests that document
their own intent, cover many inputs without copy-pasting near-identical
methods, verify that failure happens exactly when it should, and are
organized well enough that a hundred of them are still navigable. It's also
about the workflow professional testing enables — writing the test
*before* the code, and letting it drive the design.

## Objectives

The code in this project demonstrates:

- A small, fully correct `Calculator` (`add`, `subtract`, `multiply`,
  `divide`, `power`) as the subject under test.
- `@Test` with `@DisplayName` for human-readable test names.
- `@BeforeEach` for shared setup that runs fresh before every test.
- `@ParameterizedTest` with both `@CsvSource` and `@MethodSource`, covering
  many input/output pairs without duplicating test methods.
- `assertThrows` for verifying that the right exception is thrown for bad
  input (division by zero, a negative exponent).
- `assertAll` for grouping several related assertions so a failure report
  shows *all* of them, not just the first one that failed.
- `@Nested` classes organizing the suite by which method is under test.
- The red-green-refactor TDD loop, explained as a worked example.

## Concepts Refresher

### The AAA pattern

Almost every good test — in any language, any framework — has the same
three-part shape:

- **Arrange**: set up whatever the test needs (inputs, a fresh object under
  test, any fixtures).
- **Act**: do the one thing being tested — call the method.
- **Assert**: check that the result is what it should be.

```java
@Test
void addsTwoPositiveNumbers() {
    Calculator calculator = new Calculator();   // Arrange
    double result = calculator.add(2, 3);        // Act
    assertEquals(5, result);                      // Assert
}
```

Keeping these three parts visually distinct (even just by a blank line, as
above) makes a test readable at a glance — you can tell what's being set
up, what's being exercised, and what's being checked, without reading
every line closely. A test that interleaves them tends to be testing too
many things at once.

### What a good assertion message buys you

`assertEquals(expected, actual)` already tells you *that* something was
wrong when a test fails. A **message** — `assertEquals(expected, actual,
"withdrawal should reduce balance by the withdrawn amount")` — tells you
*why it matters*, right in the failure output, without having to go read
the test body to remember what it was even checking. This project favors
descriptive `@DisplayName`s over inline assertion messages for that same
purpose (see `CalculatorTest` — every test's *name* already says what it
verifies), but both tools solve the same problem: making a red test
failure legible without extra digging.

### Why parameterized tests beat copy-pasted test methods

Compare these two ways of testing the same five addition cases:

```java
// Five near-identical methods - the interesting part (the numbers) is
// buried in a sea of repeated boilerplate, and adding a sixth case means
// copy-pasting a whole method again.
@Test void addsTwoPositives() { assertEquals(5, calculator.add(2, 3)); }
@Test void addsNegativeAndPositive() { assertEquals(1, calculator.add(-2, 3)); }
@Test void addsTwoZeros() { assertEquals(0, calculator.add(0, 0)); }
// ...and so on
```

```java
// One method, five cases - adding a sixth is one more line, not one more
// method, and every case is visible in one place.
@ParameterizedTest(name = "{0} + {1} = {2}")
@CsvSource({
    "2, 3, 5",
    "-2, 3, 1",
    "0, 0, 0"
})
void addsCorrectly(double a, double b, double expected) {
    assertEquals(expected, calculator.add(a, b));
}
```

`@CsvSource` is the right choice when the cases fit comfortably as plain
text. `@MethodSource` is the right choice when the cases are more natural
to build as real Java values (see `DivideTests.divisionCases()` in this
project's tests) — both accomplish the same goal of separating *the test
logic* (written once) from *the test data* (however much of it you want).

### The red-green-refactor TDD loop

Test-Driven Development inverts the usual order: you write a test for
behavior that **doesn't exist yet**, watch it fail, then write the
smallest amount of code that makes it pass, then clean up. Concretely, in
three repeatable steps:

1. **Red** — write a test for a behavior that doesn't exist yet. Run it.
   It fails — and you check *why* it failed, to make sure it's failing for
   the right reason (the behavior is missing), not some unrelated reason
   (a typo, a compile error).
2. **Green** — write the *minimum* code needed to make that test pass.
   Not the most elegant version, not the general version — just enough to
   turn the failure into a pass.
3. **Refactor** — now that the test is passing and can catch you if you
   break it, clean the code up: better names, remove duplication, simplify
   — re-running the test after each change to confirm it still passes.

**Worked example: adding `modulo(a, b)` to `Calculator` via TDD.**

Suppose `Calculator` doesn't have a `modulo` method yet, and we want one
that behaves like Java's `%` operator but rejects a zero divisor the same
way `divide` does.

*Red.* Write the test first, before the method exists:

```java
@Test
@DisplayName("modulo returns the remainder of a divided by b")
void computesRemainder() {
    assertEquals(1, calculator.modulo(7, 3));
}
```

Running this right now doesn't just fail — it doesn't even **compile**,
because `Calculator.modulo(...)` doesn't exist. That's still useful
information: it confirms the test is exercising code that genuinely
doesn't exist yet, not accidentally passing by calling something else.

*Green.* Add the smallest implementation that makes it pass:

```java
public double modulo(double a, double b) {
    return a % b;
}
```

Re-run the test. It compiles now, and passes — `7 % 3` is `1`. Notice
what's *missing* on purpose: no zero-check yet, because no test has
demanded one yet. That's the discipline TDD asks for — don't write
behavior a test hasn't required.

*Red again.* Add the next requirement as a new failing test:

```java
@Test
@DisplayName("modulo throws ArithmeticException when the divisor is zero")
void throwsOnZeroDivisor() {
    assertThrows(ArithmeticException.class, () -> calculator.modulo(5, 0));
}
```

Run it — it fails, because `modulo` currently just returns `NaN` for
`5 % 0` (that's how Java's `%` behaves on doubles) rather than throwing.
Failing for the right reason again: the behavior genuinely isn't there.

*Green again.* Make it pass:

```java
public double modulo(double a, double b) {
    if (b == 0) {
        throw new ArithmeticException("Division by zero");
    }
    return a % b;
}
```

Both tests pass now.

*Refactor.* Looking at the finished `modulo`, its zero-check is now
identical to `divide`'s. Whether that's worth extracting into a shared
private helper is a judgment call at this size — but that's precisely the
kind of question refactoring exists to ask, with two passing tests in
place to confirm the refactor didn't break anything.

That loop — fail for the right reason, do the minimum to pass, then
clean up with tests as a safety net — is what "Try It Yourself" below asks
you to run yourself, for a different method.

## Design & Architecture

```
com.crashcourse.week14
└── Calculator   - add, subtract, multiply, divide, power
```

Deliberately one class: the point this week is the *test suite* next to
it, not the production code's structure.

```
src/test/java/com/crashcourse/week14
└── CalculatorTest
    ├── AddTests        (@Nested)
    ├── SubtractTests    (@Nested)
    ├── MultiplyTests     (@Nested)
    ├── DivideTests        (@Nested)
    └── PowerTests          (@Nested)
```

Each `@Nested` class groups every test for one `Calculator` method
together, so the suite's structure mirrors the class under test — failures
are easy to locate, and it's obvious at a glance which method is
under-tested. `@BeforeEach` lives once on the outer `CalculatorTest` and
applies to every nested class automatically, so each test — no matter
which nested class it's in — gets its own fresh `Calculator`.

## How to Build & Run

```bash
mvn clean verify
```

There's no standalone entry point this week — the "output" of this
project is the test run itself.

## Testing

```bash
mvn -q clean test
```

Covers every `Calculator` method with parameterized cases (multiple inputs
per method via `@CsvSource`/`@MethodSource`), `divide`'s and `power`'s
exception paths via `assertThrows`, a grouped-assertion example via
`assertAll`, and nested organization via `@Nested`.

## Try It Yourself

1. **Using the TDD loop described above, add a `sqrt(double)` method to
   `Calculator` that throws `IllegalArgumentException` for negative input
   — write the failing tests first.** Write a test for the happy path
   (`sqrt(9)` is `3`), watch it fail to compile, implement the minimum to
   make it pass, then write a second test for the negative-input case,
   watch *that* fail, and implement the check. Only then consider whether
   anything needs refactoring.
2. Add a `PowerTests` case using `@MethodSource` instead of `@CsvSource`
   for exponents large enough that writing them as a CSV string feels
   awkward (e.g. building the arguments with a loop).
3. Add an `@ParameterizedTest` using `@ValueSource` (a JUnit annotation not
   used elsewhere in this project) to test `power(2, exponent)` against a
   list of exponents, computing the expected value with `Math.pow` inside
   the test instead of hardcoding it.
4. `Calculator.power` currently loops explicitly. Once you're comfortable
   with the test suite, try rewriting it using `Math.pow` and confirm the
   full suite still passes without changing a single test — a concrete
   demonstration of what "the tests describe behavior, not implementation"
   means in practice.
5. Add a `@Tag("slow")` to one test (pick any, treat it as a stand-in for
   an expensive one) and look up how to configure Maven Surefire to
   exclude tests with that tag from a normal `mvn test` run.

## Reflection

The `modulo` walkthrough above only needed two tests to fully specify its
behavior — the happy path and the one edge case that mattered. TDD doesn't
ask you to anticipate every conceivable input up front; it asks you to
write one test for the next piece of behavior you actually need, watch it
fail correctly, then make it pass. The discipline is in the *order*
(test before code) and the *size of the step* (smallest change that turns
red to green) — not in writing an exhaustive test suite before writing any
code at all.
