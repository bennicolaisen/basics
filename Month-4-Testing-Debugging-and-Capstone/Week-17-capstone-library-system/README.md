# Week 17 — Capstone: Library Management System

## Purpose

This is where Months 1 through 4 stop being separate topics and become one
program. Recursion and data structures gave you the tools to build things;
OOP gave you a way to organize them into collaborating objects instead of
one long script; Java gave you static typing and a compiler that enforces
contracts; exceptions and testing gave you ways to make failure explicit
and correctness verifiable. A Library Management System — items that can
be checked out, members with limits, a catalog that has to enforce rules
consistently — is small enough to build in a week and real enough to need
every one of those tools at once.

## Objectives

- An interface (`Borrowable`) and an abstract base class (`LibraryItem`)
  working together, with three concrete subclasses (`Book`, `DVD`,
  `Magazine`) each contributing type-specific fields and a type-specific
  loan period.
- Collections and generics: `Map<String, LibraryItem>` and
  `Map<String, Member>` as the catalog and membership; `List<LibraryItem>`
  for a member's borrowed items and for overdue reporting.
- Three custom exceptions, two checked and one unchecked, each chosen
  deliberately and justified in code comments.
- A `Library` orchestrator class that coordinates `Member` and
  `LibraryItem` without either of them knowing about the other directly.
- A full JUnit 5 test suite: happy paths for every item type, every
  exception's trigger condition, borrowing-limit enforcement, and overdue
  detection.

## Concepts Refresher

Most of what this project uses was taught in earlier weeks — interfaces
and abstract classes in Week 11, the Collections Framework in Week 12,
checked vs. unchecked exceptions in Week 13, JUnit 5 in Week 14. This
section is deliberately light: the point of a capstone is composing
familiar pieces, not re-explaining any one of them from scratch.

**Interface vs. abstract class, applied here.** `Borrowable` is an
interface because "can be checked out and returned" is a capability, not
an identity — nothing here needs it standing alone, but it's what lets
`Library` treat every item type identically without caring which one it
is. `LibraryItem` is an abstract class, not an interface, because unlike
`Borrowable`'s pure capability, it carries real shared *state* (`id`,
`title`, `available`, `currentBorrower`, `dueDate`) and a real shared
*implementation* of `checkOut`/`returnItem` that every subclass gets for
free — exactly the situation an abstract class is for for, and an
interface (pre-Java-8 default methods aside) isn't.

**Custom exceptions, chosen deliberately.** All three trigger conditions
here are ordinary parts of running a library, not programming bugs — but
they still split two ways. `ItemNotAvailableException` and
`BorrowingLimitExceededException` are checked, because they're outcomes a
caller (a UI, a librarian's terminal, another service) must actively
decide how to handle at the moment `checkOut` is called — exactly the
Week 13 reasoning for `MalformedRecordException`. `MemberNotFoundException`
is unchecked, because in practice it almost always means a caller passed
a wrong or stale id — closer to `IllegalArgumentException` territory, and
every caller in this project handles it identically (report it and stop)
regardless of where it happens, so forcing it through every intermediate
`throws` clause would be ceremony without benefit. Read each exception
class's Javadoc for the full reasoning.

## Design & Architecture

```
com.crashcourse.week17
├── Borrowable                     - interface: checkOut(Member), returnItem(), isAvailable()
├── LibraryItem (abstract)          - id, title, availability + checkout bookkeeping; implements Borrowable
│   ├── Book                         - + author, isbn                  (21-day loan)
│   ├── DVD                          - + runtimeMinutes                (7-day loan)
│   └── Magazine                     - + issueNumber                   (14-day loan)
├── Member                          - id, name, borrowingLimit, borrowedItems
├── MemberNotFoundException          - unchecked: bad/stale member id
├── ItemNotAvailableException         - checked: item missing or already checked out
├── BorrowingLimitExceededException    - checked: member is already at their limit
├── Library                          - orchestrator: catalog + members, checkOut/returnItem/overdueItems
└── LibraryDemo                      - small runnable walkthrough of the happy path
```

### How the layers collaborate

Three layers, each with one job:

1. **`LibraryItem` and its subclasses** own everything about *one item's*
   own state: is it available, who has it, when is it due. `checkOut` and
   `returnItem` are implemented exactly once, in the abstract base class —
   `Book`, `DVD`, and `Magazine` only add what's genuinely different about
   them (fields, and their own `loanPeriodDays()`), which is the entire
   point of putting the shared behavior in an abstract class instead of
   copying it into all three.
2. **`Member`** owns everything about *one person's* own state: who they
   are, and which items they currently hold. It exposes
   `hasReachedBorrowingLimit()` as a read-only question but keeps
   `addBorrowedItem`/`removeBorrowedItem` package-private — only `Library`
   is allowed to change what a member is holding, which is what keeps a
   member's list from ever drifting out of sync with the items' own
   `available` flags.
3. **`Library`** is the only class that talks to both of the above at
   once. `checkOut(memberId, itemId)` looks up both by id (throwing
   `MemberNotFoundException` or `ItemNotAvailableException` if either
   lookup fails), checks the member's limit
   (`BorrowingLimitExceededException` if it's reached), and only then
   calls `item.checkOut(member)` and `member.addBorrowedItem(item)`
   together — the two halves of "this checkout happened" never happen
   independently. `overdueItems(LocalDate today)` takes "today" as a
   parameter rather than calling `LocalDate.now()` internally, specifically
   so tests (and any future caller) can ask "what would be overdue on this
   date" without needing real elapsed time to pass — see
   `LibraryTest.OverdueItems` for exactly that.

`Member` never imports `LibraryItem`'s checkout logic, and `LibraryItem`
never imports `Library`. Neither one needs to. That separation — state
belongs to the object it describes, coordination belongs to a dedicated
orchestrator above both — is a design principle worth carrying into any
program with more than a handful of classes.

**Where this leads next.** `Library` here does synchronous,
single-threaded coordination between `Member`s and `LibraryItem`s — one
orchestrator, sitting above two kinds of participant objects that don't
talk to each other directly. Everything happens on one thread, in a
strict sequence, with no possibility of two `checkOut` calls racing each
other. Removing that assumption, so that the same coordination stays
correct when *multiple threads* call it at once, is the subject of
concurrency (`synchronized`, monitors, `wait()`/`notifyAll()` in Java),
which is beyond this course. Week 22 meets the same problem from the
database side: there, a transaction is what keeps two changes from
interleaving.

## How to Build & Run

```bash
mvn clean verify
java -jar target/week17.jar
```

`LibraryDemo` checks a book and a DVD out to one member, demonstrates a
`BorrowingLimitExceededException` on a third attempt, and returns an item.

## Testing

```bash
mvn -q clean test
```

Covers:

- **Item validation and type-specific behavior** (`LibraryItemTypesTest`)
  — valid construction, each type's required fields, and each type's
  distinct `loanPeriodDays()`.
- **Checkout/return lifecycle** (`LibraryItemLifecycleTest`) — that
  `checkOut` sets availability/borrower/due-date correctly, that a second
  `checkOut` on the same item throws, and that `returnItem` clears every
  field it set.
- **`Member`** — validation, and `hasReachedBorrowingLimit()`'s behavior
  below, at, and after going back below the limit.
- **`Library`** (`LibraryTest`) — happy-path checkout for all three item
  types; every one of the three custom exceptions' trigger conditions;
  that a return frees up room for another checkout; and `overdueItems`
  correctly including an item past its due date while excluding one not
  yet due and one never checked out at all.

## Try It Yourself

> **Facit (answer key):** every exercise below is solved, tested and explained
> in Swedish in [FACIT.md](FACIT.md). Try each one yourself first, then compare.

1. Add a fourth `LibraryItem` subtype (e.g. `AudioBook`, with a
   `narrator` field and its own loan period) — no changes to `Library`,
   `Member`, or any exception class should be necessary. If you find
   yourself needing to change one of them, that's a sign something in
   this design is less polymorphic than it looks — figure out what.
2. Add a `renew(memberId, itemId)` method to `Library` that extends an
   already-checked-out item's due date by its `loanPeriodDays()` again,
   throwing an appropriate exception if the item isn't currently checked
   out by that member.
3. Add a `holds` feature: a member can place a hold on a currently
   unavailable item, and `returnItem` should make it available to the
   first member on the hold queue instead of the general catalog. This
   will likely need a new small class — decide what it should own.
4. `overdueItems` currently returns every overdue item in the whole
   catalog. Add a `overdueItemsForMember(String memberId, LocalDate today)`
   overload.
5. This project enforces one member limit for all item types combined.
   Extend it so `Library` can enforce a *separate* limit per item type
   (e.g. "at most 3 books, but only 1 DVD, at a time") — decide where that
   configuration should live.

## Reflection

Every exception in this project is checked or unchecked on purpose, not
by convention. `MalformedRecordException` back in Week 13 set the pattern:
checked when the caller must consciously decide how to respond, unchecked
when the failure is closer to "the caller made a mistake" than "the
program encountered an ordinary business outcome." Applying that same
question to three different exceptions in one class here —
`ItemNotAvailableException` and `BorrowingLimitExceededException` checked,
`MemberNotFoundException` not — is the kind of judgment call that doesn't
have one universally correct answer, only a defensible one you can
justify. That's the actual skill Month 4 was building toward: not
memorizing which exceptions are checked in the JDK, but being able to
make - and explain - that choice yourself, on a class you designed.
