# Facit vecka 14 — Try It Yourself

Facit finns i paketet `com.crashcourse.week14.facit`:

- [`Calculator.java`](src/main/java/com/crashcourse/week14/facit/Calculator.java)
  — med `sqrt` (uppgift 1) och `power` omskriven med `Math.pow` (uppgift 4).
- [`FacitTest.java`](src/test/java/com/crashcourse/week14/facit/FacitTest.java)
  — testerna för uppgift 1–5.

Kör allt med `mvn -q test`.

## 1. sqrt med TDD

TDD betyder att testet skrivs **före** koden, i små steg: rött, grönt,
städa.

**Steg 1 — rött.** Skriv det enklaste testet:

```java
@Test
void squareRootOfNine() {
    assertEquals(3.0, calculator.sqrt(9));
}
```

Det kompilerar inte ens, eftersom `sqrt` inte finns. Det räknas som rött.

**Steg 2 — grönt.** Skriv minsta möjliga kod som får testet att gå igenom:

```java
public double sqrt(double x) {
    return Math.sqrt(x);
}
```

**Steg 3 — rött igen.** Nästa beteende: negativa tal ska ge ett fel.

```java
@Test
void negativeInputThrows() {
    IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
        () -> calculator.sqrt(-4));
    assertTrue(ex.getMessage().contains("-4"));
}
```

Testet faller, för `Math.sqrt(-4)` returnerar `NaN` i stället för att kasta.

**Steg 4 — grönt.** Lägg till kontrollen:

```java
if (x < 0) {
    throw new IllegalArgumentException(
        "Cannot take the square root of a negative number, got " + x);
}
```

**Steg 5 — städa.** Behövs något? Inte här; metoden är fyra rader. Facit
lägger sedan till några fler fall, bland annat gränsfallet `sqrt(0)`, med
`@CsvSource`.

Notera jämförelsen `assertEquals(expected, actual, 1e-12)` för de extra
fallen: för decimaltal jämför man med en tolerans, eftersom små
avrundningsfel är normala.

## 2. @MethodSource med en loop

```java
static Stream<Arguments> powersOfTwo() {
    List<Arguments> cases = new ArrayList<>();
    for (int exponent = 0; exponent <= 62; exponent += 2) {
        cases.add(arguments(exponent, (double) (1L << exponent)));
    }
    return cases.stream();
}

@ParameterizedTest(name = "2^{0} = {1}")
@MethodSource("powersOfTwo")
void largePowersOfTwo(int exponent, double expected) {
    assertEquals(expected, calculator.power(2, exponent));
}
```

32 testfall utan att skriva ett enda tal för hand. Det förväntade värdet
räknas ut med `1L << exponent`, "flytta en etta `exponent` steg åt
vänster", vilket ger exakt 2 upphöjt till `exponent` som heltal. Det är ett
**annat** sätt att räkna än det som testas, och därför en riktig kontroll.

## 3. @ValueSource

```java
@ParameterizedTest(name = "2^{0}")
@ValueSource(ints = {0, 1, 2, 3, 8, 16, 31, 100})
void matchesMathPow(int exponent) {
    assertEquals(Math.pow(2, exponent), calculator.power(2, exponent));
}
```

`@ValueSource` ger **ett** värde per körning, så det passar när bara
indata varierar och det förväntade svaret kan räknas ut i testet.

Var uppmärksam på en svaghet: efter uppgift 4 använder `power` själv
`Math.pow`. Då jämför testet `Math.pow` med `Math.pow` och kan aldrig
falla. Ett test som räknar ut svaret på samma sätt som koden bevisar
ingenting. Uppgift 2 undviker det genom att räkna på ett annat sätt.

## 4. power med Math.pow

```java
public double power(double base, int exponent) {
    if (exponent < 0) {
        throw new IllegalArgumentException(
            "Exponent must be non-negative, got " + exponent);
    }
    return Math.pow(base, exponent);
}
```

Hela testsviten passerar utan att något test ändrats. Facit kör veckans
egna `power`-fall igen (`originalCasesStillPass`) mot den nya versionen
för att visa det.

Det är vad "testerna beskriver beteende, inte implementation" betyder:
testerna säger *vad* `power` ska svara, inte *hur* svaret räknas fram. Då
kan koden skrivas om fritt, och testerna talar om ifall något gick sönder.
Hade testerna i stället kontrollerat hur många varv loopen gick, hade de
fallit trots att svaren var rätt.

Kontrollen av negativ exponent måste vara kvar. `Math.pow(2, -1)` ger
`0.5` utan att klaga, så utan kontrollen skulle beteendet ändras, och
testet `negativeExponentStillThrows` skulle falla.

## 5. @Tag("slow") och Surefire

```java
@Test
@Tag("slow")
void manyAdditions() { ... }
```

Surefire, insticksprogrammet som kör testerna i Maven, kan filtrera på
taggar direkt från kommandoraden:

```bash
mvn test -DexcludedGroups=slow   # allt utom långsamma tester
mvn test -Dgroups=slow           # bara långsamma tester
```

Prova själv: facit har 53 tester. Med `-DexcludedGroups=slow` körs 52, med
`-Dgroups=slow` körs 1.

Ska de långsamma testerna alltid hoppas över i en vanlig `mvn test`, läggs
inställningen i `pom.xml`:

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-surefire-plugin</artifactId>
    <version>3.2.5</version>
    <configuration>
        <excludedGroups>slow</excludedGroups>
    </configuration>
</plugin>
```

Facit ändrar inte veckans `pom.xml`, så att alla tester fortfarande körs.
I ett riktigt projekt kör man ofta de snabba testerna vid varje ändring och
alla tester, även de långsamma, på byggservern.
