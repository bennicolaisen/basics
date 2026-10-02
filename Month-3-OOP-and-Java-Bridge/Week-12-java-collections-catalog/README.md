# Week 12 — The Collections Framework, Generics, and Ordering

## Purpose

Real programs constantly need "a bunch of things" — books in a library,
accounts in a bank, shapes in an inventory — and Java's Collections
Framework (`List`, `Set`, `Map`, and friends) is the standard toolkit for
that. This week closes out Month 3 by putting generics, and the two ways
Java lets you order objects (`Comparable` and `Comparator`), to real use
in a small book catalog — the last piece needed before Month 4's testing
and capstone work leans on all of it together.

## Objectives

- Implement `Comparable<Book>` for one natural ordering (by title), and
  use a `Comparator` for a second, different ordering (by year) without
  touching `Book` itself.
- Override `equals`/`hashCode` correctly and consistently, based on a
  single identifying field (ISBN), and see why that consistency matters
  for correct behavior in a `HashSet`/`HashMap`.
- Use a custom checked exception (`DuplicateIsbnException`) for a
  domain rule a plain exception type wouldn't name clearly.
- Use `List`, `Set`, and `Map` each for the job they're actually suited
  to, inside one small `Library` class.
- Understand what `<Book>` in `List<Book>` (generics) actually buys you
  at compile time.

## Concepts Refresher

### Generics: compile-time type safety for collections

Before generics existed (pre-Java 5), a collection held plain `Object`s,
and you had to cast every time you took something out:

```java
List raw = new ArrayList();       // a "raw type" — avoid this
raw.add(new Book(...));
raw.add("oops, a String");        // compiles fine — nothing stops this
Book b = (Book) raw.get(1);       // compiles fine, CRASHES at runtime (ClassCastException)
```

`List<Book>` tells the compiler "this list holds `Book`s and nothing
else." Now `raw.add("oops, a String")` on a `List<Book>` **will not
compile** — the same category of error Week 10 discussed for static
typing generally, caught before the program runs instead of crashing
with a `ClassCastException` somewhere downstream. `<Book>` is a **type
parameter**: it lets one class (`ArrayList`) be reused generically for
any element type, while still giving you full compile-time checking for
whichever specific type you plug in. Every collection in this project
(`Map<String, Book>`, `List<Book>`, `Set<String>`) uses this same
mechanism.

### `Comparable` vs. `Comparator`

Both exist to answer "which of these two comes first?", but they differ
in *where* that logic lives and *how many* orderings you can have:

- **`Comparable<T>`** — implemented *by* the class itself
  (`Book implements Comparable<Book>`), via one method,
  `compareTo(T other)`. This defines the type's **one** "natural"
  ordering. `Book`'s natural order is by title. Once defined,
  `Collections.sort(books)` and a `TreeSet<Book>` both use it
  automatically, with no extra argument needed.
- **`Comparator<T>`** — a *separate* object, defined wherever you need
  it, outside the class. You can have as many `Comparator`s as you have
  orderings you care about. `Library.booksSortedByYear()` uses
  `Comparator.comparingInt(Book::getYear)` to sort by year — a
  completely different ordering from `Book`'s natural (title) one,
  without changing `Book` at all:

  ```java
  books.sort(Comparator.comparingInt(Book::getYear));  // Comparator: by year
  Collections.sort(books);                              // Comparable: by title (natural)
  ```

Rule of thumb: a class gets **one** `Comparable` if it has one obvious
default ordering; reach for a `Comparator` — as many as you need, defined
right where you need them — for every other ordering.

### `equals`/`hashCode`, and why they're a matched pair

`Book.equals()` compares ISBN only — two books with the same ISBN are the
same book, even with different titles recorded (a data-entry
correction, a different printing). `hashCode()` is overridden to match:
it's built from the *same* field (`Objects.hash(isbn)`). This pairing is
not optional. `HashMap`/`HashSet` use `hashCode()` first, to find which
internal bucket an object belongs in, and only then use `equals()` to
check candidates within that bucket. If two equal objects had different
hash codes, a `HashSet` could put them in different buckets and never
realize they're "the same" — `contains()` could wrongly return `false`
for an object that *is* logically in the set. That's why the contract is
strict: **equal objects must have equal hash codes** (the reverse isn't
required — unequal objects are allowed to collide on hash code, just
less efficiently).

### A practical map: `List` vs. `Set` vs. `Map`

| | Ordered / indexed? | Duplicates? | This project's use |
|---|---|---|---|
| `List<T>` | Yes, by insertion (or sorted, explicitly) | Yes | Results of `findByAuthor`, `booksSortedByYear` — sequences where order and count both matter |
| `Set<T>` | No inherent order (unless `TreeSet`) | No — duplicates collapse via `equals`/`hashCode` | `Library.genres` — a genre is either registered or it isn't; there's nothing to count or order |
| `Map<K, V>` | Keyed access, not positional | Keys unique, values can repeat | `Library`'s internal `booksByIsbn` — O(1) lookup and duplicate detection by the one field (ISBN) that should be unique |

The question to ask when picking one: *do I need to look things up by a
key* (→ `Map`), *does order/duplication matter* (→ `List` if yes to
either), *or am I only ever asking "is X in here?"* (→ `Set`).

## Design & Architecture

```
src/main/java/com/crashcourse/week12/
├── Book.java                  — title/author/isbn/year, Comparable<Book>, equals/hashCode on isbn
├── DuplicateIsbnException.java
├── Library.java                — Map<String,Book> + List/Set operations over it
└── Main.java
src/test/java/com/crashcourse/week12/
├── BookTest.java
└── LibraryTest.java
```

`Book` knows nothing about `Library` — it's a self-contained value type
with its own natural ordering and identity rules. `Library` is the
collection-heavy class: it owns the `Map<String, Book>` (the source of
truth, keyed by ISBN), and every other view of the catalog
(`findByAuthor`, `booksSortedByYear`, `allBooks`) is derived from that
map on demand rather than kept as separate, potentially-inconsistent
copies.

## How to Build & Run

```bash
cd Month-3-OOP-and-Java-Bridge/Week-12-java-collections-catalog
mvn -q clean package
java -jar target/week12-java-collections-catalog.jar
```

## Testing

```bash
mvn -q clean test
```

Covered:

- `Book`: `equals`/`hashCode` based on ISBN alone (same ISBN, different
  other fields, still equal — and interchangeable as `HashSet` members),
  natural (title) ordering both directly and via a `TreeSet`, and
  constructor validation.
- `Library`: adding and removing books, `DuplicateIsbnException` on a
  repeated ISBN (and confirming the original registration survives
  untouched), `findByAuthor` (case-insensitive, possibly multiple
  matches), `booksSortedByYear` using its `Comparator` versus
  `Collections.sort` using `Book`'s natural `Comparable` order (shown to
  give genuinely different results), and genre registration through
  `Set<String>` (including that re-registering a genre doesn't grow the
  set).

## Try It Yourself

> **Facit (answer key):** every exercise below is solved, tested and explained
> in Swedish in [FACIT.md](FACIT.md). Try each one yourself first, then compare.

1. Add `Library.findByYearRange(int from, int to)` returning a
   `List<Book>`. Decide (and test) whether the bounds are inclusive.
2. Add a second natural-language ordering option:
   `Library.booksSortedByAuthorThenTitle()`, using
   `Comparator.comparing(...).thenComparing(...)`.
3. Change `booksByIsbn` from `Map<String, Book>` to
   `Map<String, List<Book>>` to allow multiple *copies* of the same ISBN
   to be tracked (e.g. a library owning three copies of the same book).
   What has to change in `addBook`, `removeBook`, and the duplicate check?
4. Add a `Set<String> allAuthors()` to `Library`, built from the current
   books rather than tracked separately (unlike `genres`, which is
   registered explicitly) — when would you prefer "derived from data" over
   "tracked as its own field," and why does `genres` use the latter here?
5. Make `Book` implement `Comparable<Book>` by year instead of title, and
   update `Library.booksSortedByYear()` to use `Collections.sort` with no
   `Comparator` at all. What's lost by not having a separate `Comparator`
   anymore if you later also want a title-based sort?
