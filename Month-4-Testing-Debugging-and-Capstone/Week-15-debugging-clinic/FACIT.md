# Facit vecka 15 — Try It Yourself

Veckans övningar handlar om att *göra* felsökning, så facit är en
genomgång av vad du ska se i varje steg. Koden finns i paketet
`com.crashcourse.week15.facit`
([`src/main/java/.../facit/`](src/main/java/com/crashcourse/week15/facit/)):

- `BuggyOrderSummary` — buggen från fallstudien, med flit (uppgift 1 och 4).
- `OrderSummary` — den rättade versionen (uppgift 3).
- `BugDemo` — ett program som kör buggen.

Testerna i
[`FacitTest.java`](src/test/java/com/crashcourse/week15/facit/FacitTest.java)
kontrollerar varje påstående nedan. Kör dem med `mvn -q test`.

Facit lägger buggen i en egen klass i stället för att ändra
`PricingDemo`, så att veckans projekt förblir korrekt. När du gör
övningen själv ska du lägga den i `PricingDemo`, som uppgiften säger.

## 1. Lägg in buggen

```java
public int averageFreeUnitsPerItemType(int totalFreeUnits, int distinctItemTypes) {
    return totalFreeUnits / distinctItemTypes;
}
```

och anropa den med `distinctItemTypes = 0`, en order utan
BOGO-rabatter.

## 2. Kör och läs stackspåret

```bash
mvn -q compile
java -cp target/classes com.crashcourse.week15.facit.BugDemo int
```

```
Exception in thread "main" java.lang.ArithmeticException: / by zero
	at com.crashcourse.week15.facit.BuggyOrderSummary.averageFreeUnitsPerItemType(BuggyOrderSummary.java:11)
	at com.crashcourse.week15.facit.BugDemo.main(BugDemo.java:26)
```

Samma form som i fallstudien: först typen och meddelandet, sedan två
rader `at ...`. Den översta raden är där felet kastades, den under är vem
som anropade. Radnumren skiljer sig, som uppgiften förutsåg.

## 3. Hitta och rätta buggen

Metoden, i samma ordning som avsnitt 1 i README:

1. **Läs undantaget.** `ArithmeticException: / by zero` betyder
   heltalsdivision med noll. Det vet du innan du läst någon kod.
2. **Gå till översta raden.** `BuggyOrderSummary.java:11` är raden
   `return totalFreeUnits / distinctItemTypes;`. Det finns bara en division,
   så `distinctItemTypes` måste ha varit 0.
3. **Fråga om det är ett tillåtet läge.** Ja. En order utan
   BOGO-rabatter är helt vanlig. Felet är att metoden *antog* att det alltid
   finns minst en.
4. **Rätta på rätt nivå.** Gör noll till ett definierat fall:

```java
public int averageFreeUnitsPerItemType(int totalFreeUnits, int distinctItemTypes) {
    if (distinctItemTypes == 0) {
        return 0;
    }
    return totalFreeUnits / distinctItemTypes;
}
```

Fel sätt att rätta: att omge anropet med `try { ... } catch
(ArithmeticException e)`. Det döljer symtomet men lämnar den felaktiga
metoden kvar för nästa anropare.

Är 0 rätt svar? Det är ett **beslut**: "inga gratisenheter i snitt" är
rimligt för en rapport. Alternativen är att kasta
`IllegalArgumentException` (om noll aldrig borde förekomma) eller att
returnera `OptionalDouble.empty()` (om "inget snitt finns" ska skiljas från
"snittet är noll"). Det viktiga är att beslutet syns i koden.

Ett test visar en bugg till som är lätt att missa: med `int` blir
`5 / 2` lika med `2`, inte `2,5`. Heltalsdivision kapar decimalerna. För
ett medelvärde är `double` oftast rätt typ.

## 4. Samma bugg med double

```bash
java -cp target/classes com.crashcourse.week15.facit.BugDemo double
```

```
Saved per item type: $NaN
```

Inget undantag och inget stackspår. `0.0 / 0.0` blir `NaN` ("not a
number"), `5.0 / 0.0` blir `Infinity`, och programmet fortsätter. `NaN`
följer med i nästa uträkning (`NaN * 80` är `NaN`) och syns först i
utskriften, flera steg bort från divisionen.

**Var skulle du sätta en brytpunkt?** Det är just problemet: du vet bara
var det *syntes*, inte var det *uppstod*. Du får arbeta baklänges:

- Sätt en brytpunkt vid utskriften och se vilka variabler som redan är
  `NaN`. Följ den variabeln bakåt, ett steg i taget.
- Använd en **villkorad brytpunkt** med villkoret `Double.isNaN(average)`,
  så stannar programmet bara när det intressanta händer.
- Halvera (avsnitt 4 i README): kontrollera värdet mitt i kedjan. Är det
  redan `NaN` finns felet i första halvan.

Det bästa skyddet är att inte hamna där: kontrollera indata i början av
metoden, som rättelsen gör, så att felet antingen hanteras eller kastas
direkt där det uppstår. Ett högljutt fel tidigt är lättare att hitta än ett
tyst fel sent.

## 5. Stega igenom med debuggern

Brytpunkten ska stå på raden i loopen i
`PriceCalculator.calculateFinalPrice`:

```java
total = discount.applyTo(total, item, quantity);
```

**I IntelliJ:** klicka i marginalen vid raden så att en röd prick syns.
Högerklicka på `PricingDemo` och välj *Debug 'PricingDemo.main()'*. När
programmet stannar, öppna *Variables* och tryck *Step Over* (F8) för att
köra en rad i taget. Lägg gärna `total` som *watch*.

**I terminalen med jdb:**

```bash
mvn -q compile
jdb -classpath target/classes com.crashcourse.week15.PricingDemo
```

```
> stop at com.crashcourse.week15.PriceCalculator:21
> run
Breakpoint hit: ... calculateFinalPrice(), line=21
main[1] print total
 total = 240.0
main[1] next
main[1] print total
 total = 216.0
main[1] locals
...
main[1] cont
```

`next` är *step over*, `step` är *step into* (gå in i `applyTo`), `cont`
kör vidare till nästa brytpunkt, och `locals` visar alla variabler.

Det här ska du se, för 3 hörlurar à 80 dollar:

| Steg | Rabatt | `total` efter |
|---|---|---|
| Start | `80.00 * 3` | 240,00 |
| 1 | 10 % rabatt: `240 * 0,9` | 216,00 |
| 2 | 5 dollar av: `216 - 5` | 211,00 |
| 3 | Köp en, få en: `3 / 2 = 1` gratis enhet à 80 | 131,00 |

Programmet skriver sedan `Final price: $131.00`. Lägg märke till steg 3:
BOGO-rabatten räknas på varans **ursprungliga** pris, 80, inte på det
redan nedsatta beloppet. Det är ett medvetet beslut som står i
`BuyOneGetOneDiscount`s kommentar, och det är precis den sortens sak man
upptäcker när man stegar igenom kod i stället för att bara läsa den.
Testet `runningTotalStepByStep` kontrollerar samma fyra värden.
