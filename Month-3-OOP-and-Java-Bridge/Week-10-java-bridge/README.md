# Week 10 — The Java Bridge

## Purpose

Everything so far has been Python: dynamically typed, interpreted,
run with `python3 file.py`. From here on the course is Java — a
statically typed, compiled language, built with Maven. That's a real
shift, not just new syntax for old ideas, and trying to write Java like
"Python with semicolons" is where most of the friction comes from. This
week is a deliberately small bridge: familiar logic (temperature and
distance conversion, word counting, palindrome checking — straight from
Month 1) re-expressed in Java, so the *language and tooling* are the only
new thing, not also the *problem*.

## Objectives

- Set up and build a real Maven project (`pom.xml`, `mvn compile`,
  `mvn test`).
- Write and call `static` methods on a class, mirroring the plain
  functions Month 1 used.
- Write `public static void main(String[] args)` and explain every word
  in that signature.
- Use primitive types (`double`, `int`, `boolean`) and a reference type
  (`String`) correctly, and know which is which.
- Port a small set of Python functions to Java, one-to-one, including the
  same edge cases in their tests.

## Concepts Refresher

This is the most important section this week — read it before the code.

### Dynamic typing (Python) vs. static typing (Java)

In Python, a variable is just a name that currently points at some value;
it can point at a different *kind* of value later, and nothing checks
that until the program actually runs:

```python
x = 5
x = "now I'm a string"   # totally legal, Python doesn't care
x = celsius_to_fahrenheit(x)  # crashes here, at RUNTIME, when x is a string
```

In Java, every variable has a type that's fixed when the code is written,
and the compiler checks it **before the program ever runs**:

```java
double x = 5;
x = "now I'm a string";  // will not compile — error caught before running anything
```

This is the single biggest mental shift this week: a whole category of
bugs ("I passed the wrong kind of thing") that Python would only catch
when that line actually executes, Java catches the moment you try to
build the project — often before you've even run it once.

### Compiling vs. interpreting

Python code is read and executed line-by-line by the Python interpreter
directly from the `.py` file — there's no separate "build" step. Java
source (`.java`) is **compiled** first, by `javac`, into bytecode
(`.class` files) that the Java Virtual Machine (JVM) then runs. `mvn
compile` runs `javac` for you, over every file in `src/main/java`,
according to the settings in `pom.xml`. This project's tests run through
`mvn test`, which compiles the code (main and test sources) and then
executes the test classes — if the code doesn't compile, nothing runs at
all, not even a partial result. That's a real, immediate consequence of
static typing: a type error is a **compile-time** failure, not something
you discover three functions deep at runtime.

### `public static void main(String[] args)`, piece by piece

Every runnable Java program needs exactly one method with this exact
shape somewhere (see `Main.java`):

- **`public`** — visible from outside the class; the JVM launcher needs to
  call it from outside, so it can't be more restricted than that.
- **`static`** — belongs to the class itself, not to any particular
  instance. The JVM calls `Main.main(...)` without ever constructing a
  `Main` object first, so this method has to exist independent of any
  instance.
- **`void`** — returns nothing. A program's exit code is signaled a
  different way (e.g. `System.exit(code)`), not via a return value here.
- **`main`** — the exact name the JVM looks for as the entry point. Not a
  convention you could rename — it's a hard requirement.
- **`String[] args`** — command-line arguments, as an array of strings.
  Empty (`length == 0`) if none were given; this project's `Main` doesn't
  use `args`, but the parameter must still be declared for the JVM to
  recognize this as *the* entry point.

### Primitive types vs. reference types, and two different `null`s

Java has two categories of type:

- **Primitives** — `int`, `double`, `boolean`, `char`, and a few others.
  These hold their value directly; a `double` variable *is* a number, not
  a pointer to one somewhere else. A primitive **cannot be `null`** —
  `double x = null;` will not compile. A primitive always has some
  concrete value.
- **Reference types** — everything else: `String`, arrays, and every
  class you or the JDK define, including boxed wrappers like `Integer`
  (an object wrapper around a primitive `int`, needed when you need a
  number to behave like an object — e.g. inside a collection, which Week
  12 covers). A reference-type variable holds a *reference* to an object
  somewhere in memory — or it can hold `null`, meaning "refers to
  nothing."

Python's `None` looks similar to Java's `null` — both mean "no value" —
but they're not the same idea underneath. In Python, *every* variable can
be `None`, because every Python variable is really a reference (Python has
no primitive/reference distinction at the language level — everything is
an object). In Java, whether `null` is even possible depends on the
variable's declared type: a `double` can never be `null`, only a
reference-typed variable like `String` or `Integer` can be. This is part
of why Java's type system catches more at compile time — the compiler
already knows, for every variable, whether "no value" is even a
possibility for it.

### What `pom.xml` is doing

You'll use a `pom.xml` every week from here on, so it's worth
understanding now rather than treating it as boilerplate to copy. Look at
this project's `pom.xml` alongside this list:

- `<groupId>`/`<artifactId>`/`<version>` — the project's coordinates;
  identify it uniquely, the way a package name does in other ecosystems.
- `<properties>` — `maven.compiler.source`/`target` pin the Java *language
  version* the code is written against and compiled for (17, here) —
  Maven passes these straight to `javac`.
- `<dependencies>` — external code this project needs. Here, just
  `junit-jupiter`, `scope test` — meaning it's only on the classpath while
  compiling and running tests, not when the program itself runs.
- `<build><plugins>` — tools that do the actual work of a build:
  `maven-compiler-plugin` compiles the code at the pinned Java version,
  `maven-surefire-plugin` runs the JUnit tests, and `maven-jar-plugin`
  packages the compiled code into a runnable `.jar`, configured here with
  a `mainClass` so `java -jar ...` knows which class's `main` to run.

## Design & Architecture

```
src/main/java/com/crashcourse/week10/
├── Converters.java   — static unit-conversion methods (ported from Week 1)
├── TextUtils.java    — static text utilities (ported from Week 3)
└── Main.java          — entry point demonstrating both
src/test/java/com/crashcourse/week10/
├── ConvertersTest.java
└── TextUtilsTest.java
```

`Converters` and `TextUtils` are split the same way the Python originals
were split into separate modules — each class holds one topic's worth of
static methods, none of them needing any instance state, so there's
nothing to construct: call them directly as `Converters.kmToMiles(5)`.
`Main` is the one place that ties them together into runnable output,
mirroring the role a small `if __name__ == "__main__":` block or a
`cli.py` played in the Python weeks.

## How to Build & Run

```bash
cd Month-3-OOP-and-Java-Bridge/Week-10-java-bridge
mvn -q clean package
java -jar target/week10-java-bridge.jar
```

Or, to just compile and run the tests without packaging a jar:

```bash
mvn -q clean test
```

## Testing

JUnit 5 tests live under `src/test/java`, mirroring the pytest tests from
Month 1 Weeks 1 and 3 for the ported functions, re-expressed in JUnit
idiom (`@Test`, `assertEquals` with an explicit delta for floating-point
comparisons, `assertThrows`):

- `ConvertersTest` — known reference points (0°C/32°F, 100°C/212°F),
  round-trip conversions (`celsiusToFahrenheit` then back;
  `kmToMiles` then back), and a known km/mile equivalence.
- `TextUtilsTest` — word counting including collapsed whitespace and the
  empty-string edge case, palindrome checks including case sensitivity by
  default, the `ignoreCase` overload, the empty-string edge case, and
  `null` rejection via `IllegalArgumentException` for both methods.

```bash
mvn -q clean test
```

## Try It Yourself

> **Facit (answer key):** every exercise below is solved, tested and explained
> in Swedish in [FACIT.md](FACIT.md). Try each one yourself first, then compare.

1. Add `fahrenheitToKelvin`/`kelvinToFahrenheit` to `Converters`, with
   tests for absolute zero (0 K = -459.67°F).
2. Add a `TextUtils.longestWord(String text)` that returns the longest
   whitespace-separated word (decide, and document, what happens on a
   tie).
3. Add a second `wordCount` overload that takes a custom delimiter
   `String` instead of assuming whitespace — this is more overloading
   practice, same idea as `isPalindrome`'s two forms.
4. Deliberately write a line that would be a dynamic-typing bug in Python
   (e.g. add a `String` to a `double`) and try to compile it — read the
   compiler error message closely and explain in your own words what it's
   telling you.
5. Extend `Main` to read a value from `args[0]` (a command-line argument)
   instead of a hardcoded number, and handle the case where no argument
   was given.
