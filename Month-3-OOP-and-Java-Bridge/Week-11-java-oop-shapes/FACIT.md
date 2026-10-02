# Facit vecka 11 — Try It Yourself

Övningarna ändrar veckans klasser. Facit är därför **hela projektet som
det ser ut när alla fem övningar är gjorda**, i paketet
`com.crashcourse.week11.facit`
([`src/main/java/.../facit/`](src/main/java/com/crashcourse/week11/facit/)).
Jämför filerna en och en med originalen i `com.crashcourse.week11` för
att se exakt vad som ändrats; `Circle`, `Rectangle` och `Triangle` är
oförändrade. Testerna finns i
[`src/test/java/.../facit/FacitTest.java`](src/test/java/com/crashcourse/week11/facit/FacitTest.java)
och körs med `mvn -q test`.

## 1. Square

```java
public class Square extends Rectangle {
    public Square(double side) {
        super(side, side);
    }
}
```

`super(side, side)` anropar `Rectangle`s konstruktor med samma värde för
bredd och höjd. Area, omkrets, kontrollen av att sidan är positiv och
`toString` ärvs; ingen formel skrivs två gånger.

**Påverkar det `ShapeInventory`?** Nej, inte alls. `ShapeInventory`
arbetar bara med typen `Shape`, och en `Square` *är* en `Rectangle`, som
*är* en `AbstractShape`, som *är* en `Shape`. Att nya former kan läggas
till utan att någon befintlig kod ändras är just poängen med polymorfism.

(En klassisk diskussion: är en kvadrat verkligen en rektangel? Här ja,
eftersom formerna inte kan ändras efter att de skapats. Om `Rectangle`
hade haft en `setWidth`-metod skulle en `Square` kunna hamna med olika
bredd och höjd, och arvet bli fel. Det är ett skäl till att göra objekt
oföränderliga när det går.)

## 2. smallestByArea utan upprepning

```java
private static final Comparator<Shape> BY_AREA = Comparator.comparingDouble(Shape::area);

public Shape largestByArea() {
    return extremeByArea(BY_AREA);
}

public Shape smallestByArea() {
    return extremeByArea(BY_AREA.reversed());
}

private Shape extremeByArea(Comparator<Shape> order) {
    return shapes.stream()
            .max(order)
            .orElseThrow(() -> new NoSuchElementException("inventory is empty"));
}
```

Den gemensamma hjälpmetoden tar **ordningen** som parameter. Den största
enligt omvänd ordning är den minsta, så `max` med `reversed()` räcker.
Felhanteringen för en tom samling står på ett ställe. Hjälpmetoden är
`private` eftersom den är en detalj i klassen, inte en del av vad klassen
erbjuder.

## 3. En default-metod i interfacet

```java
public interface Shape {
    double area();
    double perimeter();

    default boolean isLargerThan(Shape other) {
        return area() > other.area();
    }
}
```

En `default`-metod har en färdig kropp i interfacet, och varje klass som
implementerar interfacet får den automatiskt.

**Vad vinner man jämfört med att lägga metoden i `AbstractShape`?** Att
den gäller **alla** `Shape`, inte bara de som råkar ärva från
`AbstractShape`. En klass i Java kan bara ärva från en klass men
implementera många interface, så det finns former som inte kan ärva från
`AbstractShape`. Ett av testerna visar det med en form som implementerar
`Shape` direkt och ändå får `isLargerThan`. Metoden behöver dessutom inget
tillstånd, bara `area()`, som alla former har; därför passar den i
interfacet.

## 4. Comparable

```java
public abstract class AbstractShape implements Shape, Comparable<Shape> {
    @Override
    public int compareTo(Shape other) {
        return Double.compare(area(), other.area());
    }
    ...
}
```

`compareTo` ska returnera ett negativt tal om `this` kommer före `other`,
noll om de är lika och ett positivt tal annars. `Double.compare` gör
exakt det; att skriva `(int) (area() - other.area())` är ett vanligt fel,
eftersom en skillnad på 0,4 avrundas till 0 och formerna då räknas som
lika.

Med en naturlig ordning kan listan sorteras utan `Comparator`:
`Collections.sort(copy)`. Vecka 12 går igenom `Comparable` och
`Comparator` på djupet.

## 5. totalArea med en stream

```java
public double totalAreaWithStream() {
    return shapes.stream().mapToDouble(Shape::area).sum();
}
```

Läs den som "för varje form: ta arean, och summera". `Shape::area` är en
*metodreferens*, ett kortare sätt att skriva `shape -> shape.area()`.
Testet visar att resultatet är detsamma som med loopen, även för en tom
samling (summan av inget är 0).

**När vilken stil?** Streams passar när operationen är en kedja av
"omvandla, filtrera, sammanfatta", som här; de läses som en mening om
*vad* som räknas ut. En vanlig loop är tydligare när varje varv gör flera
saker, behöver avbrytas mitt i, eller när du vill sätta en brytpunkt och
stega igenom (vecka 15). Prestandan är i praktiken densamma för så här
små samlingar.
