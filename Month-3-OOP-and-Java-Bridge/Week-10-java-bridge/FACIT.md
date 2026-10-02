# Facit vecka 10 — Try It Yourself

Koden finns i paketet `com.crashcourse.week10.facit`
([`src/main/java/.../facit/`](src/main/java/com/crashcourse/week10/facit/))
och testerna i
[`src/test/java/.../facit/FacitTest.java`](src/test/java/com/crashcourse/week10/facit/FacitTest.java).
De körs med resten av veckans tester: `mvn -q test`.

`Converters` och `TextUtils` är `final` och har privata konstruktorer, så
det går inte att ärva från dem. Facit lägger därför de nya metoderna i
egna klasser (`ConvertersFacit`, `TextUtilsFacit`); i ett riktigt projekt
skulle de stå direkt i originalklasserna.

## 1. Kelvin

```java
public static double fahrenheitToKelvin(double fahrenheit) {
    if (fahrenheit < ABSOLUTE_ZERO_FAHRENHEIT) {
        throw new IllegalArgumentException("below absolute zero: " + fahrenheit + " F");
    }
    return Converters.fahrenheitToCelsius(fahrenheit) + KELVIN_AT_ZERO_CELSIUS;
}
```

Omvandlingen går via Celsius och återanvänder de befintliga metoderna, så
att varje formel bara står på ett ställe. Kelvin har en verklig nedre
gräns, 0 K, och ett värde under den är fysikaliskt omöjligt; därför
avvisas det med `IllegalArgumentException`, Javas motsvarighet till
Pythons `ValueError`.

Testerna jämför decimaltal med en tolerans: `assertEquals(0.0, actual,
1e-9)`. Det tredje argumentet är Javas motsvarighet till `pytest.approx`.

## 2. longestWord

```java
String longest = "";
for (String word : text.trim().split("\\s+")) {
    if (word.length() > longest.length()) {
        longest = word;
    }
}
return longest;
```

Valet vid lika längd: **det ord som kommer först i texten vinner**,
eftersom `longest` bara byts när ett ord är *strikt* längre (`>` och inte
`>=`). Valet står i dokumentationen och låses fast av ett test (`"aa bb
c"` ger `"aa"`). En tom eller blank text ger tom sträng, och `null`
avvisas som i resten av klassen.

`"\\s+"` är ett reguljärt uttryck för "ett eller flera blanktecken". I
Java måste bakstrecket skrivas dubbelt inne i en sträng.

## 3. wordCount med egen avgränsare

```java
public static int wordCount(String text, String delimiter) {
    ...
    for (String part : text.split(Pattern.quote(delimiter))) {
        if (!part.isBlank()) {
            count++;
        }
    }
    return count;
}
```

Det här är **överlagring** (*overloading*): samma namn som
`wordCount(String)` men en annan parameterlista. Kompilatorn väljer metod
utifrån argumenten i anropet.

Två beslut som står i dokumentationen och har tester:

- **Tomma delar räknas inte.** `"Oslo,Umeå,,Visby"` har tre ord, inte fyra.
- **Avgränsaren tolkas bokstavligt.** `String.split` tar egentligen ett
  reguljärt uttryck, där `.` betyder "vilket tecken som helst".
  `split(".")` skulle därför dela vid varje tecken och ge noll ord.
  `Pattern.quote` gör om avgränsaren till ett uttryck som bara matchar
  just den texten.

## 4. Ett typfel som kompilatorn fångar

Till exempel:

```java
double total = "5" + 2.0;
```

Kompilatorn svarar ungefär:

```
error: incompatible types: String cannot be converted to double
```

`"5" + 2.0` är tillåtet i sig: i Java betyder `+` med en sträng
strängsammanfogning, och resultatet blir strängen `"52.0"`. Felet är att
en **sträng** sedan ska sparas i en variabel som är deklarerad som
**double**. Kompilatorn vet typen på båda sidor och vägrar innan
programmet ens körs.

I Python skulle `"5" + 2.0` i stället ge ett `TypeError` först när raden
körs, kanske långt senare och kanske i en del av programmet som sällan
körs. Det är skillnaden mellan statisk och dynamisk typning: Java hittar
felet vid kompilering, Python vid körning.

## 5. Läs ett argument från kommandoraden

```java
static String describe(String[] args) {
    if (args.length == 0) {
        return "Usage: MainWithArgs <degrees Celsius>";
    }
    try {
        double celsius = Double.parseDouble(args[0]);
        return String.format("%.1f C is %.1f F", celsius, Converters.celsiusToFahrenheit(celsius));
    } catch (NumberFormatException e) {
        return "Not a number: " + args[0];
    }
}
```

`args` är en array med orden som skrevs efter programnamnet, precis som
`sys.argv[1:]` i Python (men utan programmets eget namn). Två saker kan
gå fel: inget argument alls (`args.length == 0`; att läsa `args[0]` skulle
ge `ArrayIndexOutOfBoundsException`), och ett argument som inte är ett tal
(`NumberFormatException` från `Double.parseDouble`).

All logik ligger i `describe`, som returnerar texten, och `main` skriver
bara ut den. Samma uppdelning som i Python-veckorna: då kan testerna
anropa `describe` direkt, utan att starta ett program. Kör det så här:

```
mvn -q compile
java -cp target/classes com.crashcourse.week10.facit.MainWithArgs 21.5
```

Testet sätter språkinställningen (`Locale`) till amerikansk engelska,
eftersom `String.format` annars skriver `21,5` med kommatecken på en dator
med svenska inställningar.
