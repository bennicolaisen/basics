# Week 15 — Debugging Clinic

## Purpose

Every program you write from here on will eventually do something you
didn't expect. The difference between a frustrating afternoon and a
five-minute fix is almost never talent — it's method. This week has no new
syntax to learn; it's entirely about the process of finding out *why* code
is wrong once you already know *that* it's wrong: reading what Java is
actually telling you, using a debugger instead of guessing, and narrowing
down a problem systematically when you don't even know where to look yet.

## Objectives

- Read a Java stack trace top to bottom and extract the useful information
  from it before looking at any code.
- Follow a worked case study: a realistic bug, its exact output, and the
  reasoning that finds and fixes it.
- Understand, at a conceptual level, what an IDE debugger's breakpoints,
  step over/into/out, and watches actually do for you.
- Use bisection — commenting out half a pipeline, or `git bisect` — as a
  strategy for when you have no idea where a bug even lives.
- Apply all of the above to a small, correct `InventoryPricing` system
  (`Item`, `Discount` strategies, `PriceCalculator`).

## Concepts Refresher

This week, this section **is** the project — a genuine debugging
methodology, not a supplement to code that teaches itself.

### 1. Reading a stack trace, top to bottom

A stack trace looks intimidating mostly because of its length, not its
difficulty. Take this one apart:

```
Exception in thread "main" java.lang.ArithmeticException: / by zero
    at com.crashcourse.week15.OrderSummary.averageFreeUnitsPerItemType(OrderSummary.java:23)
    at com.crashcourse.week15.PricingDemo.main(PricingDemo.java:15)
```

Read it in this order, not top-to-bottom for meaning (even though it's
printed top-to-bottom):

1. **The exception type and message, on the first line** — read this
   *before* looking at any code. `ArithmeticException: / by zero` already
   tells you the entire shape of the bug: somewhere, an `int` was divided
   by another `int` that turned out to be `0`. You don't need to read a
   single line of source to know that much.
2. **The frames, top to bottom, until you reach code you wrote.** Each
   `at package.Class.method(File.java:line)` line is one call on the stack
   at the moment the exception was thrown. The *first* frame
   (`OrderSummary.averageFreeUnitsPerItemType`, line 23) is where the
   exception was actually thrown — that's almost always where your
   attention belongs first. Frames further down (`PricingDemo.main`) show
   who *called* the code that failed — useful for understanding how you
   got there, but not where the bug itself lives.
3. **Distinguish "yours" from "library/JDK" frames.** If a stack trace
   includes frames like `java.util.ArrayList.get(...)` or
   `java.base/java.util.Objects.requireNonNull(...)`, those are almost
   never where the *bug* is — they're where the *symptom* surfaced. The
   actual mistake is virtually always in the nearest frame above them that
   is *your* code. A `NullPointerException` thrown inside
   `java.util.ArrayList` means your code handed `ArrayList` something it
   shouldn't have, not that `ArrayList` itself is broken.

The exception type alone narrows things enormously before you've read any
code:

| Exception | Usually means |
|---|---|
| `NullPointerException` | Something you expected to be non-null was `null` |
| `ArrayIndexOutOfBoundsException` | An index was `< 0` or `>= length` |
| `ArithmeticException: / by zero` | Integer division where the divisor was `0` |
| `ClassCastException` | An object was cast to a type it isn't actually an instance of |
| `NumberFormatException` | Text that isn't a valid number was parsed as one |

### 2. Worked case study: a discount that divides by a count that can be zero

Suppose a later feature request asked for an order-level summary: given a
whole cart, report the *average* number of free units per distinct item
type, across every `BuyOneGetOneDiscount` line in the order. A first pass
at that method might look like this (this is **illustrative code shown
here for the case study only** — it is not part of the actual project,
which stays correct throughout):

```java
// Hypothetical, buggy code - NOT part of this project's shipped source.
class OrderSummary {
    int averageFreeUnitsPerItemType(int totalFreeUnits, int distinctItemTypes) {
        return totalFreeUnits / distinctItemTypes;
    }
}
```

Called from `PricingDemo.main` with an order that happens to have zero
BOGO-discounted item types in it (`distinctItemTypes == 0`), running the
program produces exactly the stack trace shown in section 1:

```
Exception in thread "main" java.lang.ArithmeticException: / by zero
    at com.crashcourse.week15.OrderSummary.averageFreeUnitsPerItemType(OrderSummary.java:23)
    at com.crashcourse.week15.PricingDemo.main(PricingDemo.java:15)
```

Walking through the reasoning:

1. **Read the exception first.** `ArithmeticException: / by zero` — this
   is integer division by zero, full stop. Before reading a single line of
   `OrderSummary`, we already know: somewhere, an `int` divisor was `0`.
2. **Go to the top frame.** `OrderSummary.java:23` is
   `averageFreeUnitsPerItemType`. There's exactly one division in that
   method: `totalFreeUnits / distinctItemTypes`. Since the exception is
   division-by-zero, `distinctItemTypes` must have been `0` on this call.
3. **Ask why that's possible.** Was `distinctItemTypes == 0` supposed to
   be reachable? Looking at the caller, yes — an order with no BOGO
   discounts applied at all is completely ordinary, not a corrupted state.
   The method's *contract* was wrong: it silently assumed at least one
   discounted item type would always be present.
4. **Fix at the right level.** The fix isn't to catch
   `ArithmeticException` after the fact — it's to make "zero discounted
   item types" a defined, valid case instead of an implicit assumption:

   ```java
   int averageFreeUnitsPerItemType(int totalFreeUnits, int distinctItemTypes) {
       if (distinctItemTypes == 0) {
           return 0;
       }
       return totalFreeUnits / distinctItemTypes;
   }
   ```

Notice this bug *did* throw and *did* produce a stack trace — but a
close cousin of it wouldn't have. If `totalFreeUnits` and
`distinctItemTypes` had instead been `double`s, `0.0 / 0.0` evaluates to
`NaN` and `5.0 / 0.0` evaluates to `Infinity` — **no exception is thrown at
all**, the program just keeps running with a garbage number silently
baked into it, likely surfacing far from where it actually went wrong.
That's a second, harder category of bug worth recognizing: some mistakes
crash loudly, and some just quietly produce the wrong answer. The former
is a debugging exercise in reading a trace; the latter almost always needs
the next two techniques below.

### 3. Using an IDE debugger

Every mainstream Java IDE (IntelliJ, VS Code with the Java extension,
Eclipse) offers the same core toolkit, even though the exact keys and
panels differ:

- **Breakpoints** — mark a line where execution should pause. Set one
  where you suspect the problem is, run in debug mode instead of run
  mode, and the program halts right before that line executes, with every
  variable in scope visible and inspectable.
- **Step over** — run the current line and move to the next line *in the
  same method*, without diving into any method it calls.
- **Step into** — if the current line calls another method, jump inside
  that method and pause at its first line. Use this when you suspect the
  bug is *inside* that call.
- **Step out** — finish executing the rest of the current method
  immediately and pause right after it returns to its caller. Use this
  once you've confirmed the current method is fine and want to get back
  out of it quickly.
- **Watches** — expressions (a variable, a field, a small calculation) the
  debugger re-evaluates and displays every time execution pauses, so you
  don't have to keep hovering over the same variable by hand.

The value of a debugger over sprinkling `System.out.println` everywhere is
that it lets you *ask new questions on the fly*, mid-run, without editing
code and restarting — you can inspect anything in scope, not just what you
thought in advance to print.

### 4. Bisection debugging

Sometimes you don't know which of several suspects is even responsible.
Bisection means cutting the search space in half, repeatedly, rather than
checking things one at a time from the start:

- **Manually, in a pipeline of steps:** if a chain of transformations
  (e.g. several discounts applied in sequence) produces a wrong final
  result, temporarily comment out the second half of the chain and check
  the intermediate result. Wrong already? The bug is in the first half.
  Correct so far? The bug is in the second half. Repeat inside whichever
  half is guilty until only one suspect line remains.
- **With `git bisect`, across commits:** if code that worked last week is
  broken today, and you don't know which of the last twenty commits broke
  it, `git bisect start`, mark the current commit `bad` and a known-good
  older commit `good`. Git checks out the commit halfway between them; you
  test it and tell git `bisect good` or `bisect bad`; git narrows the
  range by half again. In `log2(20) ≈ 5` tests instead of up to 20, you
  land on the exact commit that introduced the bug.

Both versions of bisection share the same idea: don't scan linearly
through everything you can think of — cut the remaining possibilities in
half at every step.

## Design & Architecture

```
com.crashcourse.week15
├── Item                    - id, name, basePrice (immutable, validated)
├── Discount                - strategy interface: applyTo(total, item, qty)
├── PercentageDiscount        - implements Discount: % off
├── FlatAmountDiscount         - implements Discount: fixed amount off
├── BuyOneGetOneDiscount        - implements Discount: every 2nd unit free
├── PriceCalculator              - applies a list of Discounts in sequence
└── PricingDemo                   - runnable entry point for debugger practice
```

`Discount` is a small strategy interface so `PriceCalculator` never needs
to know which kind of discount it's applying — it just calls `applyTo` on
each one in order, passing along the running total. Each concrete discount
validates its own configuration at construction time (e.g.
`PercentageDiscount` rejects a value outside 0–100), so a `Discount`
instance is always internally valid the same way `Item` is. This is the
project deliberately using the interface/implementation pattern from Week
11 for something with real, testable logic.

## How to Build & Run

```bash
mvn clean verify
java -jar target/week15.jar
```

Running the jar prints a small worked pricing example. It's a good target
for the debugger exercise below: set a breakpoint inside
`PriceCalculator.calculateFinalPrice`, run in debug mode, and step through
each discount being applied.

## Testing

```bash
mvn -q clean test
```

Covers `Item`'s validation, each `Discount` implementation's math
(including edge cases like an odd unit left unpaired for
`BuyOneGetOneDiscount`, and a flat discount larger than the running
total), and `PriceCalculator`'s sequencing of multiple discounts together,
plus its own input validation.

## Try It Yourself

> **Facit (answer key):** every exercise below is solved, tested and explained
> in Swedish in [FACIT.md](FACIT.md). Try each one yourself first, then compare.

This week's exercise is genuinely hands-on: don't just read the case
study above, reproduce it yourself.

1. Make a local copy of this project (or work on a branch). Deliberately
   introduce the bug from the case study: add an `OrderSummary` class with
   the buggy `averageFreeUnitsPerItemType` method shown above, and call it
   from `PricingDemo.main` with `distinctItemTypes = 0`.
2. Run it and confirm you get the exact stack trace shape shown in the
   case study (the line numbers will differ — that's fine).
3. Using the stack-trace-reading method from section 1, without looking
   back at the case study's fix, find and fix the bug yourself.
4. Now introduce the *other* variant mentioned in section 2: change
   `totalFreeUnits` and `distinctItemTypes` to `double`, and construct a
   `0.0 / 0.0` case. Confirm nothing throws, and that you instead get
   `NaN` printed somewhere downstream. Notice how much harder this is to
   localize than the version that threw — where would you even set a
   breakpoint if you didn't already know the answer?
5. Set an actual breakpoint (in your IDE, or `jdb` if you want the
   command-line experience) inside `PriceCalculator.calculateFinalPrice`,
   run `PricingDemo` in debug mode, and step through one discount being
   applied to a running total, watching the total change with each step.
