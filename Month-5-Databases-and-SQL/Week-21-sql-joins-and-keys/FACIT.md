# Facit vecka 21 — Try It Yourself

Varje svar ligger som en egen `.sql`-fil i [`facit/`](facit/). Kör dem
mot veckans databas med:

```bash
python3 facit/kor.py        # alla
python3 facit/kor.py u3     # bara uppgift 3
```

Testerna i [`tests/test_facit.py`](tests/test_facit.py) kontrollerar
varje svar och körs med resten av veckan: `python3 -m pytest -q`.

## 1. Städer och observationer per land

```sql
SELECT c.country,
       COUNT(DISTINCT c.id) AS cities,
       COUNT(o.id)          AS observations
FROM cities c
LEFT JOIN observations o ON o.city_id = c.id
GROUP BY c.country
ORDER BY c.country;
```

| country | cities | observations |
|---|---|---|
| Denmark | 1 | 0 |
| Norway | 1 | 7 |
| Sweden | 6 | 42 |

Två fällor, en för varje kolumn:

- **Städerna.** Efter joinen finns en rad per *observation*, inte per
  stad: Stockholm förekommer sju gånger. `COUNT(c.id)` ger därför 42 för
  Sverige. `COUNT(DISTINCT c.id)` räknar varje stad en gång. Ett test visar
  det felaktiga talet.
- **Danmark.** Med vanlig `JOIN` försvinner Köpenhamn helt, eftersom den
  inte har någon observation att para ihop med. `LEFT JOIN` behåller den,
  med `NULL` i alla observationskolumner. `COUNT(o.id)` hoppar över `NULL`
  och ger 0. `COUNT(*)` hade räknat raden och gett 1.

## 2. Snödagar per stad, utan CASE

```sql
SELECT c.name,
       COUNT(o.id) AS snow_days
FROM cities c
LEFT JOIN observations o
       ON o.city_id = c.id
      AND o.conditions = 'snow'
GROUP BY c.id, c.name
ORDER BY c.name;
```

Kiruna får 2, alla andra 0, även Köpenhamn. Knepet är att villkoret om snö
står i **`ON`**, inte i `WHERE`. Då paras varje stad bara ihop med sina
snödagar, och en stad utan snödagar får en rad med `NULL` som `COUNT(o.id)`
räknar som 0. Uppgift 3 visar vad som händer om villkoret flyttas.

`GROUP BY c.id, c.name` grupperar på id:t, som säkert är unikt, och tar med
namnet för att kunna visa det.

## 3. ON eller WHERE

Den första frågan ger **9 rader**, den andra **2**.

Förklaringen är ordningen som en fråga logiskt utförs i:

1. `FROM` och `JOIN ... ON` bygger ihop tabellerna.
2. `WHERE` filtrerar resultatet.
3. `SELECT` väljer kolumner.

**Villkoret i `ON`** är en del av steg 1. Det bestämmer vilka
observationer som får paras ihop med en stad. Städer utan någon snödag
behålls ändå, för det är vad `LEFT JOIN` lovar, med `NULL` i
`observed_on`. Kiruna ger två rader och de sju andra städerna en rad var:
9 rader.

**Villkoret i `WHERE`** körs i steg 2, efter joinen. Då har varje stad
redan parats ihop med alla sina observationer, och `WHERE` slänger allt
som inte är snö. Raden för Köpenhamn har `o.conditions = NULL`, och
`NULL = 'snow'` är inte sant, så den försvinner också. Kvar blir Kirunas
två rader. En `LEFT JOIN` med ett villkor på den högra tabellen i `WHERE`
blir i praktiken en vanlig `JOIN`.

Tumregel: villkor som ska *begränsa vad som paras ihop* skrivs i `ON`.
Villkor som ska *ta bort rader ur resultatet* skrivs i `WHERE`.

## 4. Varmare än dagen innan

```sql
SELECT c.name,
       today.observed_on,
       yesterday.temp_max_c                              AS high_day_before_c,
       today.temp_max_c                                  AS high_c,
       ROUND(today.temp_max_c - yesterday.temp_max_c, 1) AS rise_c
FROM observations today
JOIN observations yesterday
  ON yesterday.city_id = today.city_id
 AND yesterday.observed_on = date(today.observed_on, '-1 day')
JOIN cities c ON c.id = today.city_id
WHERE ROUND(today.temp_max_c - yesterday.temp_max_c, 1) >= 2
ORDER BY today.observed_on, c.name;
```

| name | observed_on | high_day_before_c | high_c | rise_c |
|---|---|---|---|---|
| Kiruna | 2026-09-25 | 2.7 | 5.4 | 2.7 |
| Stockholm | 2026-09-26 | 14.6 | 17.4 | 2.8 |

En **self-join** använder samma tabell två gånger, med två alias för två
roller: `today` och `yesterday`. `date(today.observed_on, '-1 day')` räknar
ut gårdagens datum som text, `'2026-09-25'` blir `'2026-09-24'`, och det
jämförs med `yesterday.observed_on`.

Skillnaden avrundas innan den jämförs med 2. Annars kan en skillnad som
borde vara exakt 2,0 bli 1,9999999 i datorn och falla bort.

**Varför syns aldrig 21 september?** Dagen innan, 20 september, finns inte
i datan. En vanlig `JOIN` behåller bara rader som har en partner, så
måndagens observationer har ingen `yesterday` att paras ihop med och
försvinner. Med `LEFT JOIN` skulle de vara kvar med `NULL` som gårdagens
temperatur, men `NULL >= 2` är inte sant, så de skulle ändå filtreras bort.

## 5. Vädervarningar

En ny tabell som pekar på `cities`, eftersom en varning gäller en stad:

```sql
CREATE TABLE warnings (
    id         INTEGER PRIMARY KEY,
    city_id    INTEGER NOT NULL REFERENCES cities (id),
    level      TEXT    NOT NULL CHECK (level IN ('yellow', 'orange', 'red')),
    message    TEXT    NOT NULL,
    starts_on  TEXT    NOT NULL,  -- 'YYYY-MM-DD', första dagen
    ends_on    TEXT    NOT NULL,  -- 'YYYY-MM-DD', sista dagen (ingår)
    CHECK (starts_on <= ends_on)
);
```

Designbeslut:

- **`city_id` är en främmande nyckel** till `cities`, precis som i
  `observations`. Varningen lagrar inte stadens namn; det hämtas med en
  join. (SQLite kontrollerar främmande nycklar bara när
  `PRAGMA foreign_keys = ON` är påslaget. Vecka 22 gör det.)
- **Datumen lagras som ISO-text**, så att `<=` och `BETWEEN` fungerar som
  datumjämförelser (se vecka 19).
- **`CHECK`** stoppar ogiltiga nivåer och en varning som slutar innan den
  börjar. Ett test visar att databasen säger nej. Vecka 24 går igenom
  `CHECK` på djupet.
- **En stad kan ha flera varningar**, till exempel både vind och regn.
  Därför är varningarna en egen tabell och inte några kolumner i `cities`.

Frågan "städer med en aktiv varning den 23 september":

```sql
SELECT c.name, w.level, w.message
FROM warnings w
JOIN cities c ON c.id = w.city_id
WHERE '2026-09-23' BETWEEN w.starts_on AND w.ends_on
ORDER BY c.name;
```

`BETWEEN` tar med båda ändpunkterna, vilket passar eftersom `ends_on` är
den sista dagen som varningen gäller. Med exempeldatan i facit-filen blir
svaret Göteborg (orange), Kiruna och Visby (gul). Stockholms varning tog
slut den 22:a och Oslos börjar den 24:e, så de kommer inte med. Vill du ha
varje stad bara en gång, även om den har två varningar, använder du
`SELECT DISTINCT c.name`.
