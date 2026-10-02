# Facit vecka 17 — Try It Yourself

Facit är hela systemet med alla fem uppgifter gjorda, i paketet
`com.crashcourse.week17.facit`
([`src/main/java/.../facit/`](src/main/java/com/crashcourse/week17/facit/)).

| Fil | Ändring |
|---|---|
| `AudioBook` | ny (uppgift 1) |
| `HoldQueue` | ny (uppgift 3) |
| `BorrowingPolicy` | ny (uppgift 5) |
| `Library` | uppgift 2–5, plus en rättad bugg |
| `LibraryItem` | en ny metod, `extendDueDate` (uppgift 2) |
| övriga | oförändrade kopior |

Testerna, grupperade per uppgift, finns i
[`src/test/java/.../facit/FacitTest.java`](src/test/java/com/crashcourse/week17/facit/FacitTest.java)
och körs med `mvn -q test`.

## 1. AudioBook

```java
public final class AudioBook extends LibraryItem {
    private static final int LOAN_PERIOD_DAYS = 14;
    private final String narrator;
    private final int durationMinutes;
    ...
    @Override
    public int loanPeriodDays() {
        return LOAN_PERIOD_DAYS;
    }
}
```

Ingen annan klass behövde ändras. `Library`, `Member` och undantagen
pratar bara med `LibraryItem`, och allt som skiljer sorterna åt
(låneperioden) är en abstrakt metod som varje sort fyller i själv. Det är
polymorfism som fungerar: ny sort, ny klass, inget annat.

**Var designen mindre polymorf än den ser ut?** På ett ställe, och det
syns i uppgift 5. Så fort en regel gäller *vissa sorter* ("högst 1 DVD")
är det frestande att skriva `if (item instanceof DVD)` i `Library`. Då
måste `Library` ändras för varje ny sort, och polymorfismen är borta.
Facit undviker det genom att låta regeln vara data, nycklad på klassen
(se uppgift 5). Kommentaren i `Borrowable` räknar också upp `Book`, `DVD`
och `Magazine`. Det är bara text, men den blir inaktuell; sådana listor
ska man undvika i kommentarer.

## 2. renew

```java
public LocalDate renew(String memberId, String itemId)
        throws MemberNotFoundException, ItemNotAvailableException {
    Member member = requireMember(memberId);
    LibraryItem item = requireBorrowedBy(member, itemId);

    HoldQueue queue = holds.get(itemId);
    if (queue != null && queue.hasWaiting()) {
        throw new ItemNotAvailableException("... cannot be renewed: other members are waiting for it");
    }
    item.extendDueDate();
    return item.dueDate();
}
```

och i `LibraryItem`:

```java
void extendDueDate() {
    this.dueDate = dueDate.plusDays(loanPeriodDays());
}
```

Förfallodatumet ändras inne i `LibraryItem`, eftersom det är där fältet
finns. Metoden är paketprivat (ingen `public`), så bara `Library` kan
anropa den, efter att ha kontrollerat vem som lånar. Samma mönster som
`Member.addBorrowedItem`.

Nya datumet räknas från det **gamla förfallodatumet**, inte från i dag.
Det är vad uppgiften säger ("by its `loanPeriodDays()` again"), och det
gör att man inte förlorar dagar på att förnya tidigt.

**Vilka undantag?**

- Exemplaret är inte utlånat, eller utlånat till någon annan:
  `IllegalStateException`. Det följer hur `returnItem` redan gjorde: att
  förnya något man inte har lånat är ett fel av den som anropar.
- Någon står i kö för exemplaret: `ItemNotAvailableException`, som är
  checked. Det är ett helt vanligt utfall som anroparen måste hantera
  ("du kan inte förnya, någon väntar"), alltså samma resonemang som för
  att exemplaret är utlånat. Den här regeln uppstår först när uppgift 3
  finns, men den hör till förnyelsen.

## 3. Reservationer (holds)

Den nya klassen är `HoldQueue`, en kö **per exemplar**:

```java
public final class HoldQueue {
    private final Deque<Member> waiting = new ArrayDeque<>();
    private Member reservedFor;
    ...
}
```

**Vad den äger:** vilka som väntar, i turordning, och vem exemplaret just
nu är reserverat för. **Vad den inte äger:** om exemplaret är utlånat och
om medlemmen har nått sin gräns. Det vet redan `LibraryItem` och `Member`,
och `Library` samordnar som förut. `Library` håller en
`Map<String, HoldQueue>` från exemplar-id till kö.

Flödet:

1. Bob ställer sig i kö med `placeHold("MEM2", "B1")` medan Alice har boken.
2. Alice lämnar tillbaka. `returnItem` anropar `queue.itemReturned()`, och
   boken blir **reserverad för Bob**, den som stod först.
3. Någon annan som försöker låna får `ItemNotAvailableException`
   ("reserved for another member").
4. Bob lånar som vanligt med `checkOut`. Reservationen tas bort.

Varför reserverad och inte direkt utlånad till Bob? För att Bob kanske har
nått sin lånegräns, och för att man i verkligheten måste hämta boken. Med
en reservation går Bob igenom samma kontroller som alla andra. Ett test
visar en medlem med reservation som ändå stoppas av sin lånegräns.

Reglerna i `placeHold`: man kan inte reservera något som går att låna
direkt, något man redan lånar, eller samma exemplar två gånger. Däremot
går det att reservera ett exemplar som är ledigt men reserverat för någon
annan.

Saker facit inte gör, men ett riktigt system skulle behöva: avboka en
reservation, och låta en reservation gå ut om den inte hämtas inom några
dagar.

## 4. overdueItemsForMember

```java
public List<LibraryItem> overdueItemsForMember(String memberId, LocalDate today) {
    Member member = requireMember(memberId);
    return member.borrowedItems().stream()
        .filter(item -> isOverdue(item, today))
        .toList();
}

private static boolean isOverdue(LibraryItem item, LocalDate today) {
    return !item.isAvailable() && item.dueDate() != null && today.isAfter(item.dueDate());
}
```

Villkoret för "förfallen" fanns tidigare inne i `overdueItems`. Nu ligger
det i en hjälpmetod som båda använder, så att de aldrig kan börja tycka
olika. Metoden letar i medlemmens egna lån i stället för i hela katalogen.

`isAfter` gör att ett lån som ska lämnas *i dag* inte räknas som försenat.
Det finns ett test för exakt det gränsfallet. Testerna skickar in ett
datum (`today`) i stället för att använda dagens datum, vilket gör dem
pålitliga; det är skälet till att metoden tar `today` som parameter.

## 5. Gräns per sort

**Var ska inställningen ligga?** Tre kandidater:

- **I varje sort** (`DVD` har ett `MAX_AT_ONCE`): nej. Gränsen är inte en
  egenskap hos en DVD; ett annat bibliotek kunde ha en annan regel.
- **I `Member`**: bara om olika medlemmar ska ha olika gränser per sort,
  till exempel ett barnkort. Det säger uppgiften inget om.
- **I biblioteket, som en regel**: ja. Facit samlar reglerna i en liten
  klass, `BorrowingPolicy`, och ger den till `Library` när biblioteket
  skapas.

```java
Library library = new Library(new BorrowingPolicy()
        .limit(Book.class, 3)
        .limit(DVD.class, 1));
```

I `checkOut`, efter kontrollen av den totala gränsen:

```java
OptionalInt typeLimit = policy.limitFor(item.getClass());
if (typeLimit.isPresent() && countOfType(member, item.getClass()) >= typeLimit.getAsInt()) {
    throw new BorrowingLimitExceededException(
        "Member " + memberId + " may borrow at most " + typeLimit.getAsInt()
            + " " + item.getClass().getSimpleName() + " at a time");
}
```

Gränserna är nycklade på **klassen** (`DVD.class`), så `Library`
innehåller ingen `instanceof` och behöver inte ändras när en ny sort
läggs till. `AudioBook` har ingen egen gräns förrän någon sätter en; då
gäller bara den totala gränsen. Medlemmens totala gräns finns kvar som
förut. Båda reglerna gäller, och den som slår till först avgör.
`new Library()` utan regler fungerar precis som originalet.

## En bugg som facit rättar

Originalets `returnItem` kontrollerar att exemplaret är utlånat, men inte
**till vem**. Om Bob lämnar tillbaka Alices bok blir boken ledig, medan
den ligger kvar i Alices lista över lån. `Member` och `LibraryItem` är då
oense, vilket är precis vad klassens kommentarer säger aldrig ska hända.

Facit samlar kontrollen i `requireBorrowedBy`, som både `returnItem` och
`renew` använder: exemplaret måste vara utlånat till just den medlemmen,
annars `IllegalStateException`. Testet
`cannotReturnSomeoneElsesLoan` visar det. Buggen hittades när `renew`
skrevs, eftersom den behövde exakt samma kontroll. Att skriva en ny
funktion är ofta det som avslöjar ett hål i en gammal.
