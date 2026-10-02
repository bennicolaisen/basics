# Facit vecka 13 — Try It Yourself

Facit är hela parsern med alla fem uppgifter gjorda, i paketet
`com.crashcourse.week13.facit`
([`src/main/java/.../facit/`](src/main/java/com/crashcourse/week13/facit/)).
`ParseError` och `BatchParseResult` är oförändrade kopior. Testerna finns i
[`src/test/java/.../facit/FacitTest.java`](src/test/java/com/crashcourse/week13/facit/FacitTest.java)
och körs med `mvn -q test`.

## 1. Ett femte fält: salary

Tre ställen ändras:

**`CsvRecord`** får fältet, en getter och en kontroll i konstruktorn. Fältet
ska också med i `equals`, `hashCode` och `toString`; det är lätt att glömma.

```java
// !(salary >= 0) är sant både för negativa tal och för NaN.
if (!(salary >= 0) || Double.isInfinite(salary)) {
    throw new IllegalArgumentException("Salary must be a non-negative number, got " + salary);
}
```

Varför inte bara `salary < 0`? För att `Double.parseDouble("NaN")` och
`Double.parseDouble("Infinity")` **lyckas**. `NaN` ("not a number") är
varken större än, mindre än eller lika med något, så `NaN < 0` är falskt
och NaN skulle slinka igenom. `!(salary >= 0)` fångar det.

**`CsvRecordParser`** väntar sig nu fem fält, och parsar det femte:

```java
double salary;
try {
    salary = Double.parseDouble(rawSalary);
} catch (NumberFormatException e) {
    throw new InvalidSalaryException("Salary must be a number, got \"%s\" ...", e);
}
```

**Testerna** täcker de nya felfallen: negativ lön, lön som inte är ett tal,
`NaN` och `Infinity`, och en rad i det gamla formatet med bara fyra fält.
Noll är tillåtet (gränsfallet), och det testas också.

## 2. En undantagsklass per felkategori

```
MalformedRecordException
├── EmptyLineException
├── WrongColumnCountException
├── InvalidAgeException
├── InvalidSalaryException
└── InvalidFieldException      (namn, e-post eller avdelning)
```

Alla ärver från `MalformedRecordException`, så kod som inte bryr sig om
*vilket* fel det var ändras inte alls: `BatchParser` fångar fortfarande
bara basklassen. Den som vill kan nu skriva:

```java
try {
    record = CsvRecordParser.parseLine(line);
} catch (InvalidSalaryException e) {
    // till exempel: skicka raden till löneavdelningen för kontroll
} catch (MalformedRecordException e) {
    // allt annat
}
```

Ordningen spelar roll: den mer specifika `catch` måste stå först.

En detalj: i originalet kontrollerades en negativ ålder först i
`CsvRecord`s konstruktor, som kastar `IllegalArgumentException`. För att
den ska bli ett `InvalidAgeException` kontrollerar facit åldern (och lönen)
i parsern innan posten skapas. Då vet parsern att ett fel från konstruktorn
måste gälla namn, e-post eller avdelning.

**Är det en förbättring här?** Ärligt talat: knappast. I det här projektet
behandlas alla fel på samma sätt; de skrivs ut med radnummer och
meddelande, och ingen kod fångar en underklass för sig. Fem nya klasser
utan någon som använder skillnaden är ceremoni. Underklasser blir värda
besväret först när någon anropare faktiskt **gör något olika** beroende på
felet. Tills dess räcker ett tydligt meddelande. Det är en bra tumregel för
undantag i allmänhet: skapa en ny typ när någon behöver fånga just den.

## 3. Filter med Predicate

```java
public static BatchParseResult parseFile(Path path, Predicate<CsvRecord> filter) throws IOException {
    return parseFile(path, filter, false);
}
```

och inne i loopen:

```java
CsvRecord record = CsvRecordParser.parseLine(line);
if (filter.test(record)) {
    records.add(record);
}
```

Filtret används **efter** att raden har parsats, och bara i `try`-delen. En
trasig rad når aldrig filtret och hamnar som förut bland felen. Ett test
visar det: med ett filter som säger nej till allt finns felet ändå kvar.

`Predicate<CsvRecord>` är ett interface med en metod, `test`, som svarar
ja eller nej. Den som anropar skickar med en lambda:

```java
BatchParser.parseFile(file, r -> r.department().equals("Engineering"));
```

Alla varianter av `parseFile` anropar samma metod längst ned. Den gamla
`parseFile(path)` blir `parseFile(path, record -> true, false)`, ett filter
som släpper igenom allt. Då finns loopen bara på ett ställe.

## 4. En rapport till fil

```java
public static List<String> lines(BatchParseResult result) { ... }

public static void write(BatchParseResult result, Path path) throws IOException {
    Files.write(path, lines(result), StandardCharsets.UTF_8);
}
```

Exempel på en rapport:

```
Parse report
Records parsed: 1
Lines failed: 2
Errors:
  line 2: Expected 5 comma-separated fields ...
  line 4: Age must be a whole number, got "x" ...
```

Uppdelningen i två metoder är poängen. `lines` räknar fram innehållet och
kan testas utan någon fil alls. `write` gör bara själva skrivandet. Att
hålla isär "räkna ut" och "skriva ut" gör båda delarna enklare att testa.

`write` kastar `IOException` vidare i stället för att fånga det. Metoden
vet inte vad som är rätt att göra om disken är full; det vet den som
anropar.

## 5. Strikt läge för tomma rader

```java
if (line.isBlank()) {
    if (strict) {
        errors.add(new ParseError(lineNumber, "Line is blank"));
    }
    continue;
}
```

`parseFile(path, false)` beter sig som originalet, och ett test kontrollerar
att det ger exakt samma poster som `parseFile(path)`. `parseFile(path, true)`
rapporterar den tomma raden med radnummer, och de andra raderna parsas som
vanligt.

En `boolean`-parameter är enkel men har en nackdel: i anropet
`parseFile(file, true)` syns inte vad `true` betyder. I större kod används
därför ofta en `enum`, till exempel `BlankLines.SKIP` och
`BlankLines.REPORT`, som läses som text vid anropet.
