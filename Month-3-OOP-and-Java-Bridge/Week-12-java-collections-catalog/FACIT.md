# Facit vecka 12 — Try It Yourself

Facit ligger i paketet `com.crashcourse.week12.facit`
([`src/main/java/.../facit/`](src/main/java/com/crashcourse/week12/facit/)):

- `Library` — veckans bibliotek med uppgift 1, 2, 4 och 5 gjorda.
- `CopiesLibrary` — uppgift 3. Den ändrar hur hela klassen lagrar böcker,
  så den får en egen klass i stället för att blandas ihop med resten.
- `Book` — uppgift 5 (naturlig ordning efter år).
- `DuplicateIsbnException` — oförändrad.

Testerna finns i
[`src/test/java/.../facit/FacitTest.java`](src/test/java/com/crashcourse/week12/facit/FacitTest.java)
och körs med `mvn -q test`.

## 1. findByYearRange

```java
public List<Book> findByYearRange(int from, int to) {
    if (from > to) {
        throw new IllegalArgumentException("from (" + from + ") must not be after to (" + to + ")");
    }
    List<Book> matches = new ArrayList<>();
    for (Book book : booksByIsbn.values()) {
        if (book.getYear() >= from && book.getYear() <= to) {
            matches.add(book);
        }
    }
    Collections.sort(matches);
    return matches;
}
```

**Båda gränserna ingår** (`>=` och `<=`). Det är vad de flesta menar med
"böcker från 1950 till 1960", och det gör att `findByYearRange(1965, 1965)`
betyder "böcker från 1965". Testerna låser fast beslutet, med fall precis
på gränserna; annars kan någon senare byta `<=` mot `<` utan att märka det.

Två ytterligare beslut:

- `from > to` är nästan säkert ett misstag hos den som anropar, så metoden
  kastar ett fel i stället för att tyst returnera en tom lista.
- Resultatet sorteras efter år. En `HashMap` har ingen bestämd ordning, och
  en lista som kommer i slumpvis ordning är svår både att läsa och att
  testa.

## 2. Författare, sedan titel

```java
private static final Comparator<Book> BY_AUTHOR_THEN_TITLE =
        Comparator.comparing(Book::getAuthor, String.CASE_INSENSITIVE_ORDER)
                .thenComparing(Book::getTitle, String.CASE_INSENSITIVE_ORDER);
```

Läs den som en mening: "jämför författare utan hänsyn till stora och små
bokstäver; om de är lika, jämför titel på samma sätt". `thenComparing`
används bara när den första jämförelsen ger oavgjort. Komparatorn är ett
`static final`-fält eftersom den är densamma varje gång; den behöver inte
byggas om vid varje anrop.

## 3. Flera exemplar av samma bok

```java
private final Map<String, List<Book>> booksByIsbn = new HashMap<>();
```

Ändringen i typen sprider sig till nästan varje metod. Det är typiskt: att
byta datastruktur är ett beslut om hela klassen.

**addBook.** Ett ISBN som redan finns är inte längre ett fel, utan ett
exemplar till. Dubblettkontrollen försvinner därför, men något behöver ta
dess plats: om ett nytt exemplar har samma ISBN men en *annan* titel är
datan fel. Facit kastar då `IllegalArgumentException`:

```java
List<Book> copies = booksByIsbn.get(book.getIsbn());
if (copies == null) {
    copies = new ArrayList<>();
    booksByIsbn.put(book.getIsbn(), copies);
} else if (!sameEdition(copies.get(0), book)) {
    throw new IllegalArgumentException(...);
}
copies.add(book);
```

**removeBook.** Tar bort *ett* exemplar. Den viktiga detaljen: när det sista
exemplaret försvinner måste nyckeln tas bort ur mappen. Annars ligger en tom
lista kvar, och `findByIsbn` skulle krascha på `copies.get(0)`.

```java
copies.remove(copies.size() - 1);
if (copies.isEmpty()) {
    booksByIsbn.remove(isbn);
}
```

**size.** Det finns nu två svar på "hur många böcker?": antal exemplar
(`size`) och antal olika titlar (`titleCount`). Facit har båda, så att den
som anropar måste välja.

**findByAuthor.** Ska tre exemplar av *Dune* ge tre träffar? Facit säger
nej: varje bok en gång. Det är ett beslut, inte en självklarhet; ett
utlåningssystem kunde vilja se alla exemplar.

(Ett alternativ är `Map<String, Integer>` med ett antal per ISBN plus en
separat `Map<String, Book>`. Listan är bättre om exemplaren senare ska få
egna egenskaper, till exempel skick eller vem som lånat dem.)

## 4. allAuthors — räknad eller sparad?

```java
public Set<String> allAuthors() {
    Set<String> authors = new TreeSet<>();
    for (Book book : booksByIsbn.values()) {
        authors.add(book.getAuthor());
    }
    return Collections.unmodifiableSet(authors);
}
```

Författarna räknas fram ur böckerna vid varje anrop. Fördelen är att de
**aldrig kan bli fel**: tas den sista boken av en författare bort,
försvinner författaren automatiskt. Ett eget fält hade behövt uppdateras i
`addBook` och `removeBook`, och den dagen någon glömmer det visar
biblioteket författare som inte finns. `TreeSet` ger dem i bokstavsordning
och tar bort dubbletter.

**Räkna fram** när informationen redan finns i datan och det går tillräckligt
snabbt. **Spara i ett eget fält** när informationen inte går att räkna fram,
eller när uträkningen är för dyr att göra ofta.

**Varför sparas `genres` separat?** För att den informationen *inte finns*
i böckerna: `Book` har inget genrefält. Dessutom ska en genre kunna finnas
innan biblioteket har någon bok i den. Biblioteket bestämmer sina kategorier
först och köper böcker sedan. Ett test visar en genre utan böcker.

## 5. Naturlig ordning efter år

```java
@Override
public int compareTo(Book other) {
    return Integer.compare(this.year, other.year);
}
```

och i `Library`:

```java
public List<Book> booksSortedByYear() {
    List<Book> books = new ArrayList<>(booksByIsbn.values());
    Collections.sort(books);
    return books;
}
```

**Vad förlorar man?** Flera saker:

- **Titelsorteringen måste skrivas uttryckligen.** `Collections.sort` på en
  lista böcker betyder nu "efter år". Den som vill ha titelordning måste
  skicka med en `Comparator` (se `booksSortedByTitle` i facit). Det fanns
  bara en naturlig ordning, och den är upptagen.
- **Befintlig kod byter beteende utan att något syns.** Veckans `Main`
  anropar `Collections.sort(naturalOrder)` och skriver "natural (title)
  order". Efter ändringen kompilerar den fortfarande, men sorterar efter år.
  Kompilatorn kan inte varna, för typerna är desamma.
- **"Lika" blir väldigt grovt.** `compareTo` säger att två böcker från samma
  år är lika, fast de har olika ISBN och alltså inte är `equals`. Samlingar
  som bygger på `compareTo`, till exempel `TreeSet` och `TreeMap`, tror då
  att den ena boken är en dubblett och slänger den. Ett test visar att en
  `TreeSet` med två böcker från 1965 bara får storlek 1. (Samma risk fanns
  med titelordningen, för två utgåvor kan ha samma titel, men det händer
  mer sällan.) Lösningen är en sista jämförelse som skiljer allt som inte är
  `equals`, till exempel `.thenComparing(Book::getIsbn)`.

Slutsats: låt den naturliga ordningen vara den som nästan alla vill ha, och
använd separata `Comparator`-objekt för resten. Original-`Library` med
`Comparator.comparingInt(Book::getYear)` var alltså det bättre valet.
