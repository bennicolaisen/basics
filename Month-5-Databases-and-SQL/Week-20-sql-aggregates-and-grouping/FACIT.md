# Facit vecka 20 — Try It Yourself

Varje svar ligger som en egen `.sql`-fil i [`facit/`](facit/). Kör dem
mot veckans databas med:

```bash
python3 facit/kor.py        # alla
python3 facit/kor.py u3     # bara uppgift 3
```

Testerna i [`tests/test_facit.py`](tests/test_facit.py) kontrollerar
varje svar och körs med resten av veckan: `python3 -m pytest -q`.

## 1. Medeltemperatur per dag

```sql
SELECT observed_on,
       ROUND(AVG(temp_max_c), 1) AS avg_high_c,
       COUNT(*)                  AS cities_reporting
FROM observations
GROUP BY observed_on
ORDER BY observed_on;
```

| observed_on | avg_high_c | cities_reporting |
|---|---|---|
| 2026-09-21 | 14.3 | 7 |
| 2026-09-22 | 13.2 | 7 |
| 2026-09-23 | 11.7 | 7 |
| 2026-09-24 | 11.1 | 7 |
| 2026-09-25 | 12.7 | 7 |
| 2026-09-26 | 14.4 | 7 |
| 2026-09-27 | 12.4 | 7 |

`GROUP BY observed_on` gör en grupp per datum, och `AVG` och `COUNT`
räknas för varje grupp för sig. Alla sju städer rapporterade varje dag
(Köpenhamn har inga observationer alls).

**Kallast i genomsnitt var torsdagen 24 september**, 11,1 grader. Facit
har också en fråga som svarar direkt (`u1b`): sortera på medelvärdet och
ta första raden.

```sql
ORDER BY AVG(temp_max_c)
LIMIT 1;
```

## 2. Torra och blöta dagar sida vid sida

```sql
SELECT city_id,
       SUM(CASE WHEN precipitation_mm = 0 THEN 1 ELSE 0 END) AS dry_days,
       SUM(CASE WHEN precipitation_mm > 0 THEN 1 ELSE 0 END) AS wet_days
FROM observations
GROUP BY city_id
ORDER BY city_id;
```

| city_id | dry_days | wet_days |
|---|---|---|
| 1 | 3 | 4 |
| 2 | 1 | 6 |
| 3 | 2 | 5 |
| 4 | 3 | 4 |
| 5 | 2 | 5 |
| 6 | 3 | 4 |
| 7 | 3 | 4 |

Knepet: `CASE` gör om varje rad till en etta eller en nolla, och `SUM`
räknar ettorna. Två `CASE` med olika villkor ger två räkningar i samma
grupp. Kolumnerna blir 7 tillsammans för varje stad, eftersom de två
villkoren (`= 0` och `> 0`) tillsammans täcker alla dagar och aldrig samma
dag. Göteborg hade bara en torr dag.

Det kortare `SUM(precipitation_mm = 0)` fungerar också i SQLite, eftersom
en jämförelse där blir 1 eller 0. `CASE` fungerar i alla databaser och
säger tydligare vad som räknas.

## 3. WHERE eller HAVING?

Frågan gäller **hela veckan** för varje stad ("veckans lägsta
dagstemperatur"), alltså ett värde som räknas fram per grupp. Därför hör
villkoret hemma i `HAVING`:

```sql
SELECT city_id, MIN(temp_max_c) AS lowest_high_c
FROM observations
GROUP BY city_id
HAVING MIN(temp_max_c) > 13
ORDER BY city_id;
```

Svar: Göteborg (13,5), Malmö (14,7) och Visby (13,6).

Med samma gräns i `WHERE` (`u3b`) kommer också Stockholm (1) och Oslo (7)
med. Varför? `WHERE` körs **före** grupperingen och tar bort enskilda
rader. Stockholms kalla dag, 12,9 grader, försvinner innan `MIN` räknas,
så `MIN` ser bara de varma dagarna och svarar 13,2. Frågan blir då "den
kallaste av de dagar som var över 13 grader", och det är förstås alltid
över 13.

Tumregel: `WHERE` väljer **rader**, `HAVING` väljer **grupper**. Villkor
med `MIN`, `MAX`, `SUM`, `AVG` eller `COUNT` hör nästan alltid hemma i
`HAVING`.

## 4. COUNT(DISTINCT ...)

```sql
SELECT city_id, COUNT(DISTINCT conditions) AS kinds_of_weather
FROM observations
GROUP BY city_id
HAVING COUNT(DISTINCT conditions) >= 3
ORDER BY city_id;
```

Alla sju städer hade tre sorters väder: sol, moln och regn, utom Kiruna
som hade snö i stället för regn. Filtret tar alltså inte bort någon.
Det är värt att kontrollera att ett filter som "inte gör något" ändå
fungerar: med `>= 4` blir resultatet tomt, och ett test visar det.

`COUNT(*)` hade gett 7 för varje stad (sju dagar). `DISTINCT` inne i
parentesen gör att varje sorts väder räknas en gång.

## 5. Saknade värden som noll

```sql
SELECT city_id,
       ROUND(AVG(COALESCE(wind_ms, 0)), 2) AS avg_wind_missing_as_zero,
       ROUND(AVG(wind_ms), 2)              AS avg_wind_known_only
FROM observations
GROUP BY city_id
ORDER BY city_id;
```

`COALESCE(wind_ms, 0)` betyder "`wind_ms`, eller 0 om den saknas".

Medelvärdena skiljer sig för **Umeå (4)**, 3,40 mot 3,97, och **Kiruna
(5)**, 3,21 mot 3,75: de två städer som har en trasig givare. För Umeå
räknar den första kolumnen (summan av sex mätningar) / 7, den andra
(summan av sex mätningar) / 6. Att räkna en okänd vind som 0 är att låtsas
att det var vindstilla en dag då ingen vet hur det blåste, och det drar
ner medelvärdet.

**I en väderrapport:** det korrekta medelvärdet, 3,97, det som bara räknar
kända mätningar. Helst med en notering om underlaget, "baserat på 6 av 7
dagar", vilket är just vad `q08` visar med kolumnen `wind_readings`. Att
`AVG` hoppar över `NULL` är alltså en fördel här, inte ett fel.
