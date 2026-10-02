# Week 11 — Java OOP: Interfaces, Abstract Classes, and Polymorphism

## Purpose

Week 9 built objects in Python; Week 10 rebuilt small pieces of earlier
logic in Java's syntax. This week is where Java's *type system* around
objects actually gets used: interfaces, abstract classes, and inheritance
as a language-enforced contract rather than a convention. A small
hierarchy of shapes is the classic example for a reason — `Circle`,
`Rectangle`, and `Triangle` are obviously different in how they compute
area and perimeter, but obviously the same in *that* they can, which is
exactly the situation interfaces and abstract classes exist to model.

## Objectives

- Define a `Shape` interface (`area()`, `perimeter()`) and understand why
  it's an interface rather than a class.
- Define `AbstractShape`, an abstract class that implements `Shape`,
  shares real implementation (`toString()`) across all subclasses, and
  still leaves `area()`/`perimeter()` for each subclass to fill in.
- Implement `Circle`, `Rectangle`, and `Triangle`, each extending
  `AbstractShape`, including input validation in constructors (the
  triangle inequality for `Triangle`).
- Build `ShapeInventory`, a class that operates on a `List<Shape>` purely
  through the `Shape` interface, never caring which concrete class each
  element actually is.
- See polymorphism happen for real: one loop, one method call
  (`shape.area()`), three different implementations running depending on
  what object is actually behind the `Shape` reference at runtime.

## Concepts Refresher

### Interface vs. abstract class

Both let you say "every X can do Y" — but they differ in what they're
allowed to contain, and Java forces you to pick based on that:

| | Interface | Abstract class |
|---|---|---|
| Method bodies | No (until Java 8's `default`, not used here) | Yes, freely |
| Instance fields (state) | No | Yes |
| Constructors | No | Yes |
| A class can have how many? | Implement as many interfaces as it wants | Extend exactly one |

`Shape` is an interface because there is genuinely nothing shared to
implement — a circle's area formula and a triangle's have nothing in
common. `AbstractShape` is an abstract class because `toString()` *is*
genuinely shared, real, working code, and abstract classes are the only
one of the two that can hold a real method body. The rule of thumb this
project demonstrates: reach for an interface to declare a pure contract
with no shared state or code; reach for an abstract class the moment you
have actual logic or fields to share across subclasses, on top of a
contract.

Java only lets a class `extends` one other class (no multiple
inheritance of state), which is exactly why `AbstractShape` can't also be
a second class `Circle` needed to extend for some other reason — but a
class can `implements` as many interfaces as it wants, since interfaces
carry no state to create ambiguity about.

### Inheritance (IS-A) vs. Week 9's composition (HAS-A)

`Circle extends AbstractShape` means **Circle IS-A AbstractShape** (and,
transitively, IS-A `Shape`): every `Circle` really is usable anywhere a
more general `AbstractShape` or `Shape` is expected, because it inherits
and fulfills that whole contract. Compare Week 9's `Bank`, which **HAS-A**
collection of `BankAccount`s — a `Bank` is not a kind of `BankAccount`,
it just holds and delegates to some. Both relationships are real tools;
picking the wrong one is a common design mistake. A quick test: if "B is
a kind of A" sounds natural and B should be usable *anywhere* A is
expected, that's inheritance. If it only sounds natural as "B has one or
more A", that's composition.

### Polymorphism, concretely

Look at `ShapeInventory.totalArea()`:

```java
double total = 0.0;
for (Shape shape : shapes) {
    total += shape.area();
}
```

`shapes` is declared as `List<Shape>`. Every loop iteration, `shape` is
*typed* as `Shape` — but at runtime it's actually referring to a real
`Circle`, `Rectangle`, or `Triangle` object. When `shape.area()` runs,
the JVM looks at the *actual* object behind that reference and calls
*that* class's `area()` — `Circle`'s formula for circles,
`Rectangle`'s for rectangles, and so on — even though the code calling
it only ever mentions `Shape`. This is **dynamic dispatch**: which
method body actually runs is decided at runtime, based on the real
object, not at compile time based on the declared variable type. That's
what "polymorphism" means here — one piece of code (`shape.area()`)
behaves differently depending on what's really behind `shape`, without
an `if`/`else` or a type check anywhere in sight.

If this feels familiar from Python — it should. Python let you write
`shape.area()` for *any* object with an `area()` method, no interface
declared anywhere, no `implements` keyword, nothing — that's **duck
typing** ("if it walks like a duck and quacks like a duck..."): Python
doesn't check that `shape` is any particular type at all, it just tries
to call `.area()` and fails at runtime if that method doesn't exist. Java
gets you to the same *outcome* (code that works uniformly across
different types) but via the opposite mechanism: the `Shape` interface
is declared up front, and the compiler guarantees every `Shape` really
does have an `area()` method — checked before the program runs, not
discovered by trying and possibly failing at runtime.

## Design & Architecture

```
src/main/java/com/crashcourse/week11/
├── Shape.java             — interface: area(), perimeter()
├── AbstractShape.java     — abstract class implementing Shape, shares toString()
├── Circle.java            — extends AbstractShape
├── Rectangle.java         — extends AbstractShape
├── Triangle.java          — extends AbstractShape, validates triangle inequality
├── ShapeInventory.java    — List<Shape>-backed collection with aggregate ops
└── Main.java              — small runnable demo
src/test/java/com/crashcourse/week11/
├── CircleTest.java
├── RectangleTest.java
├── TriangleTest.java
└── ShapeInventoryTest.java
```

The chain `Shape` → `AbstractShape` → `{Circle, Rectangle, Triangle}`
exists specifically so `ShapeInventory` can hold all three concrete types
in one `List<Shape>` and operate on them uniformly. `ShapeInventory`
never imports `Circle`, `Rectangle`, or `Triangle` — it only knows
`Shape`, which is the whole design point: adding a fourth shape later
requires zero changes to `ShapeInventory`.

## How to Build & Run

```bash
cd Month-3-OOP-and-Java-Bridge/Week-11-java-oop-shapes
mvn -q clean package
java -jar target/week11-java-oop-shapes.jar
```

## Testing

```bash
mvn -q clean test
```

Covered:

- `Circle`/`Rectangle`: area and perimeter formulas against known values,
  rejection of non-positive dimensions.
- `Triangle`: area via Heron's formula on a known 3-4-5 right triangle,
  perimeter, and — the important edge case — construction rejecting both
  a clearly invalid triangle and a *degenerate* one where the triangle
  inequality holds with exact equality (`1 + 2 == 3`).
- `ShapeInventory`: `totalArea()` summing across mixed shape types,
  `largestByArea()` (including on an empty inventory), `sortedByArea()`
  returning a new ascending list without disturbing the original
  insertion order, and rejecting a `null` shape.
- An explicit polymorphism test: a `List<Shape>` mixing all three
  concrete types, summing `area()` purely through the `Shape` interface
  reference.

## Try It Yourself

> **Facit (answer key):** every exercise below is solved, tested and explained
> in Swedish in [FACIT.md](FACIT.md). Try each one yourself first, then compare.

1. Add a `Square` — but implement it as a `Rectangle` subclass that
   forces `width == height` in its constructor, rather than duplicating
   the area/perimeter formulas. Does this change anything about how
   `ShapeInventory` uses it?
2. Add a `smallestByArea()` to `ShapeInventory` without duplicating the
   logic in `largestByArea()` — can both be expressed in terms of one
   shared private helper?
3. Give `Shape` a `default` method (Java 8+ lets interfaces have method
   bodies for these) — for example `default boolean isLargerThan(Shape
   other)`. What does using `default` here buy you over putting the same
   method on `AbstractShape` instead?
4. Make `AbstractShape` implement `Comparable<Shape>` (by area), then sort
   an inventory with `Collections.sort` instead of `ShapeInventory`'s own
   `Comparator`-based method. (Week 12 covers `Comparable` in depth — this
   is a preview.)
5. Write a version of `ShapeInventory.totalArea()` using
   `shapes.stream().mapToDouble(Shape::area).sum()` instead of the
   explicit loop, and confirm it behaves identically. When would you
   prefer one style over the other?
