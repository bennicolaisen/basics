# Facit vecka 24 — Try It Yourself

Facit ligger i [`facit/`](facit/):

- [`facit/schema.sql`](facit/schema.sql) — hela schemat med uppgift 1–4
  gjorda. Varje ändring är märkt med "Uppgift N".
- [`facit/stock_check.sql`](facit/stock_check.sql) — frågan som bevisar
  att lagret stämmer (uppgift 3).
- [`facit/shop.py`](facit/shop.py) — de nya funktionerna. Resten
  återanvänds från `shop_rules.shop`.

Testerna finns i [`tests/test_facit.py`](tests/test_facit.py) och körs med
resten av veckan: `python3 -m pytest -q`.

## 1. Återbetalning (refunded)

Nytt tillståndsdiagram (uppgift 2 lägger till `invoiced`, se nedan):

```
open ──► paid ──► shipped
  │        │
  │        └────► refunded
  └────► cancelled
```

Tre ändringar i schemat:

1. **`CHECK` på `orders.status`** får det nya värdet `'refunded'`.
2. **`orders_status_flow`** får en ny pil:
   `OR (OLD.status = 'paid' AND NEW.status IN ('shipped', 'refunded'))`.
   Eftersom triggern listar vad som är *tillåtet* stoppades `refunded`
   automatiskt tills pilen lades till.
3. **`orders_cancel_returns_stock`** ska också lämna tillbaka varorna vid
   återbetalning.

**Minst ändring** behöver den tredje: bara villkoret i `WHEN`, inte
kroppen. Koden som lämnar tillbaka varorna är redan rätt.

```sql
-- före
WHEN NEW.status = 'cancelled' AND OLD.status <> 'cancelled'
-- efter
WHEN NEW.status IN ('cancelled', 'refunded') AND OLD.status NOT IN ('cancelled', 'refunded')
```

Den andra halvan av villkoret är viktig: den gör att varorna bara lämnas
tillbaka **en gång**, även om någon sätter samma status igen. Ett test
kontrollerar det. I facit heter triggern `orders_return_stock`, och den
skriver en lagerrörelse i stället för att ändra lagret direkt (uppgift 3).

Testerna visar att bara en betald order kan återbetalas (inte en öppen,
skickad eller avbokad) och att `refunded` är ett sluttillstånd.

## 2. Kunder och kreditgräns

**Först ett problem med uppgiften.** I veckans flöde går en order
`open → paid → shipped`: en skickad order är alltid betald. "Skickade men
obetalda ordrar" finns alltså inte, och en kreditgräns skulle inte ha
något att begränsa. Kredit betyder att kunden får varorna *innan* hen
betalar. Facit lägger därför till en väg för det, en faktura:

```
open ──► paid ──► shipped
  │        │         ▲
  │        └──► refunded
  ├──► invoiced ─────┘    skickad mot faktura; 'shipped' när fakturan är betald
  └──► cancelled
```

Regeln blir: **en order får bara faktureras om kundens obetalda fakturor
plus den här ordern ryms inom kundens kreditgräns.** Att betala direkt
fungerar som förut, oavsett gräns.

```sql
CREATE TABLE IF NOT EXISTS customers (
    name              TEXT PRIMARY KEY,
    credit_limit_sek  REAL NOT NULL CHECK (credit_limit_sek >= 0)
);

CREATE TRIGGER IF NOT EXISTS orders_credit_limit
BEFORE UPDATE OF status ON orders
WHEN NEW.status = 'invoiced' AND OLD.status <> 'invoiced'
 AND (SELECT COALESCE(SUM(total_sek), 0) FROM order_totals
      WHERE customer = NEW.customer AND status = 'invoiced')
   + (SELECT total_sek FROM order_totals WHERE order_id = NEW.id)
   > COALESCE((SELECT credit_limit_sek FROM customers WHERE name = NEW.customer), 0)
BEGIN
    SELECT RAISE(ABORT, 'credit limit exceeded');
END;
```

**Constraint, trigger eller vy?** En **trigger**:

- En `CHECK`-regel ser bara den rad som skrivs. Den här regeln behöver
  summera *andra* ordrar och läsa en annan tabell.
- En vy kan *visa* hur mycket varje kund är skyldig (facit har en sådan,
  `customer_credit`), men en vy kan inte stoppa något.
- En trigger kan läsa vad som helst och avbryta ändringen.

Triggern använder vyn `order_totals` för beloppen, så rabatten räknas på
samma sätt i kreditkontrollen som överallt annars. En kund som inte finns
i `customers` har gränsen 0 och kan inte handla mot faktura alls, men kan
betala direkt. Testerna täcker gränsfallet (exakt på gränsen är tillåtet),
att en betald faktura frigör kredit, och att en tom order inte kan
faktureras (`orders_pay_needs_lines` gäller nu båda vägarna).

## 3. Lagerrörelser

Uppgiften vill att varje ändring av `products.stock` loggas med en orsak.
Det svåra är *orsaken*: en trigger på `products` ser bara att lagret
ändrades, inte varför. Facit vänder därför på det:

**Rörelserna är sanningen, och lagret följer dem.**

```sql
CREATE TABLE IF NOT EXISTS stock_movements (
    id          INTEGER PRIMARY KEY,
    product_id  INTEGER NOT NULL REFERENCES products (id),
    change      INTEGER NOT NULL CHECK (change <> 0),
    reason      TEXT    NOT NULL CHECK (reason IN ('delivery', 'order', 'cancellation', 'refund'))
);

-- Varje rörelse ändrar lagret. Det är det ENDA stället som gör det.
CREATE TRIGGER IF NOT EXISTS stock_movements_change_stock
AFTER INSERT ON stock_movements
BEGIN
    UPDATE products SET stock = stock + NEW.change WHERE id = NEW.product_id;
END;
```

Den som ändrar lagret skriver en rörelse, och vet därmed orsaken:

- `order_lines_take_stock` skriver `-quantity` med orsaken `'order'`.
- `orders_return_stock` skriver `+quantity` med `'cancellation'` eller
  `'refund'`.
- `receive_delivery` i Python skapar produkten med tomt lager och skriver
  en rörelse med `'delivery'`.

Två vakter ser till att ingen kan gå runt rörelserna:

- `products_start_empty`: en ny produkt måste börja med lagret 0.
- `products_stock_matches_movements`: om lagret efter en ändring inte är
  lika med summan av rörelserna avbryts ändringen. En direkt
  `UPDATE products SET stock = 99` stoppas därför med
  `stock can only change through stock_movements`.

`CHECK (stock >= 0)` finns kvar som sista försvar. En rörelse som skulle
göra lagret negativt stoppas, och eftersom rörelsen och lagerändringen
hör till samma sats försvinner båda.

**Beviset** (`facit/stock_check.sql`):

```sql
SELECT p.sku,
       p.stock,
       COALESCE(SUM(m.change), 0)           AS sum_of_movements,
       p.stock - COALESCE(SUM(m.change), 0) AS difference
FROM products AS p
LEFT JOIN stock_movements AS m ON m.product_id = p.id
GROUP BY p.id, p.sku, p.stock
ORDER BY p.sku;
```

Kolumnen `difference` ska vara 0 för varje produkt. `LEFT JOIN` och
`COALESCE` gör att en produkt utan rörelser också kontrolleras (den måste
då ha lagret 0).

## 4. Två rabattnivåer

Ändringen sker på **ett** ställe, vyn `order_totals` i schemat:

```sql
CASE
    WHEN subtotal_sek >= 2500 THEN subtotal_sek * 0.15
    WHEN subtotal_sek >= 1000 THEN subtotal_sek * 0.10
    ELSE 0
END AS discount_sek
```

Ordningen spelar roll: `CASE` väljer den första grenen som är sann, så den
högsta gränsen måste stå först. Annars skulle en order på 3 000 kr få 10 %.

**Hur många filer?** En fil med regeln (`schema.sql`), plus testerna och
kommentaren högst upp i schemat som räknar upp reglerna. Ingen Python-kod
behöver ändras, eftersom `shop.py`, demon och kreditkontrollen alla läser
rabatten ur vyn.

Om rabatten i stället hade räknats ut i Python på tre ställen (i
kassan, på kvittot och i en rapport) hade alla tre behövt ändras, och
glömmer man ett får kunden en summa i kassan och en annan på kvittot.
Ingenting varnar för det. Det är vinsten med att definiera en beräkning en
gång.

**En fälla:** veckans schema skapar vyn med `CREATE VIEW IF NOT EXISTS`. I
en databas som redan finns gör det ingenting, och den gamla rabatten
gäller kvar. Facit använder därför `DROP VIEW IF EXISTS order_totals;`
följt av `CREATE VIEW`, så att varje gång databasen öppnas får den den
aktuella definitionen. Ett test öppnar en gammal databasfil och ser att
rabatten blir 15 %. (Tabeller och triggrar har samma problem, men de går
inte att byta lika lätt: en ny `CHECK` på `orders` kräver att tabellen
byggs om, och en befintlig databas behöver en ingående lagerrörelse per
produkt innan vakten i uppgift 3 kan slås på. Sådana ändringar kallas
*migreringar* och skrivs som egna skript.)

## 5. En regel som inte ska ligga i databasen

**"När en order har betalats ska kunden få ett mejl med orderbekräftelse."**

Den ska ligga i programmet, av två skäl:

1. **Databasen kan inte prata med omvärlden.** En trigger kan inte skicka
   mejl, och ska inte kunna det.
2. **Ett mejl går inte att ångra.** En trigger körs inne i en
   transaktion. Om transaktionen rullas tillbaka efteråt, till exempel för
   att en annan regel slår till, finns ordern inte, men mejlet har redan
   gått iväg. Programmet ska skicka mejlet först *efter* att
   transaktionen har lyckats.

Andra regler som hör hemma i programmet: om betalningsleverantören har
godkänt kortet (informationen finns inte i databasen), vilket språk ett
felmeddelande ska visas på, och kampanjer som "fri frakt i helgen", som
ändras ofta och styrs av marknadsavdelningen. En bra tumregel: databasen
garanterar att datan **aldrig är fel**; programmet bestämmer **vad som ska
hända** och **hur det berättas** för användaren.
