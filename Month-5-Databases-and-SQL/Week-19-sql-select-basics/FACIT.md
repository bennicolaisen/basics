# Facit vecka 19 — Try It Yourself

Varje svar ligger som en egen `.sql`-fil i [`facit/`](facit/). Kör dem
mot veckans databas med:

```bash
python3 facit/kor.py        # alla
python3 facit/kor.py u4     # bara uppgift 4
```

Testerna i [`tests/test_facit.py`](tests/test_facit.py) kontrollerar
varje svar rad för rad och körs med resten av veckan: `python3 -m pytest -q`.

Uppgiften ber dig lägga svaren i `queries/` som `q12_...`. Facit ligger i
en egen mapp så att veckans egna frågor och tester inte påverkas, men SQL:en
är densamma.

## 1. Små svenska städer

```sql
SELECT name, population
FROM cities
WHERE country = 'Sweden'
  AND population < 200000
ORDER BY population DESC;
```

| name | population |
|---|---|
| Umeå | 132235 |
| Visby | 24330 |
| Kiruna | 22423 |

`AND` kräver att **båda** villkoren är sanna. `DESC` vänder ordningen så
att den största kommer först. Talet skrivs utan mellanslag eller
tusentalsavgränsare: `200000`, inte `200 000`.

## 2. AND, OR och parenteser

**a)** Regn i Göteborg, men minst 14 grader:

```sql
SELECT id, observed_on, temp_max_c, conditions
FROM observations
WHERE city_id = 2
  AND conditions = 'rain'
  AND temp_max_c >= 14;
```

Två rader: 22 september (14,1) och 27 september (14,3). "Nådde 14 grader"
betyder 14 eller mer, alltså `>=`.

**b)** Regn eller snö, och kallare än 10 grader:

```sql
WHERE (conditions = 'rain' OR conditions = 'snow')
  AND temp_max_c < 10;
```

Fyra rader: Umeå 23 och 24 september (regn), Kiruna 23 och 24 september
(snö). Kiruna är med, Oslo är inte det, precis som uppgiften förutsåg.

**c)** Utan parentesen blir det fel. `AND` binder hårdare än `OR`, på
samma sätt som `*` binder hårdare än `+` i matte. SQLite läser därför

```sql
WHERE conditions = 'rain' OR conditions = 'snow' AND temp_max_c < 10
```

som

```sql
WHERE conditions = 'rain' OR (conditions = 'snow' AND temp_max_c < 10)
```

Gränsen på 10 grader gäller då bara snö, och **alla** 16 regndagar kommer
med, även Oslos dagar på 11–14 grader: 18 rader i stället för 4. Frågan
ger inget fel, bara fel svar. Tumregel: när `AND` och `OR` blandas,
skriv alltid parenteser, även när de inte behövs. Då ser läsaren vad du
menade. (`conditions IN ('rain', 'snow')` är ett kortare sätt att skriva
samma sak som parentesen.)

## 3. LIKE

**a)**

```sql
SELECT name FROM cities WHERE name LIKE '%a';
```

Bara **Kiruna**. `%` betyder "vilka tecken som helst, hur många som helst",
så `'%a'` är "slutar på a". Umeå slutar på `å`, som är en annan bokstav.

**b)** `name LIKE 'malmö'` matchar Malmö, men `name LIKE 'MALMÖ'` gör det
inte:

| name | lower_case_pattern | upper_case_pattern |
|---|---|---|
| Malmö | 1 | 0 |

Varför? SQLite:s `LIKE` struntar i stora och små bokstäver, men **bara för
de engelska bokstäverna A–Z**. I `'malmö'` skiljer sig bara `m` från `M`,
och det hanteras. I `'MALMÖ'` måste också `Ö` matcha `ö`, och för `å`, `ä`
och `ö` gör SQLite ingen sådan jämförelse. Andra databaser beter sig
annorlunda. Lärdom: lita inte på att `LIKE` hanterar svenska bokstäver
utan att testa det.

## 4. Minst skillnad mellan högsta och lägsta

```sql
SELECT observed_on, city_id, ROUND(temp_max_c - temp_min_c, 1) AS range_c
FROM observations
ORDER BY range_c, observed_on, city_id
LIMIT 3;
```

| observed_on | city_id | range_c |
|---|---|---|
| 2026-09-22 | 6 | 3.1 |
| 2026-09-23 | 6 | 3.1 |
| 2026-09-22 | 2 | 3.3 |

**Delad tredjeplats.** Det händer faktiskt i datan: både Göteborg 22
september och Visby 24 september har skillnaden 3,3. Med bara
`ORDER BY range_c` säger SQL ingenting om vilken av dem som kommer först,
och `LIMIT 3` klipper då godtyckligt. Svaret kan bli olika i en annan
databas, eller efter en uppdatering.

Två sätt att göra det förutsägbart:

1. **Fler sorteringskolumner**, som facit gör. `observed_on, city_id`
   avgör när skillnaden är lika. Då är det alltid samma tre rader.
2. **Ta med alla som delar platsen**, om det är vad frågan egentligen
   vill ha. Då blir svaret fyra rader:

   ```sql
   SELECT observed_on, city_id, ROUND(temp_max_c - temp_min_c, 1) AS range_c
   FROM observations
   WHERE ROUND(temp_max_c - temp_min_c, 1) <= (
       SELECT ROUND(temp_max_c - temp_min_c, 1)
       FROM observations
       ORDER BY 1
       LIMIT 1 OFFSET 2
   )
   ORDER BY range_c, observed_on, city_id;
   ```

   (En fråga inuti en fråga kallas *subquery*. Vecka 21 och 23 går
   igenom det. Vecka 23 visar också `RANK()`, som är gjord för just
   delade placeringar.)

En detalj: sortera på det **avrundade** värdet. Decimaltal är inte exakta
i datorn; `14.1 - 10.8` blir `3.299999999999999`. Här råkar båda
skillnaderna bli exakt samma felaktiga tal, men det är tur. Sorterar man
på oavrundade värden kan ett litet avrundningsfel avgöra ordningen mellan
två värden som borde vara lika.

## 5. Lugnt helgväder

```sql
SELECT id, observed_on, city_id, wind_ms
FROM observations
WHERE observed_on IN ('2026-09-26', '2026-09-27')
  AND wind_ms IS NOT NULL
  AND wind_ms < 3
ORDER BY observed_on, city_id;
```

Tre rader, alla från lördagen: Umeå (2,2), Kiruna (1,8) och Oslo (2,4).

**Varför blir det samma utan `IS NOT NULL`?** För att `NULL < 3` inte är
sant. Det är okänt, och `WHERE` behåller bara rader där villkoret är
**sant**. En rad med okänd vind försvinner alltså ändå. Här finns
dessutom inga saknade vindvärden under helgen (de två saknade är 22 och
24 september), så det skulle inte märkas ens om det gjorde skillnad.

**När blir det skillnad?** När ett `NULL` kan bli sant på något annat sätt:

- Om du byter ut `NULL` mot ett värde, till exempel
  `COALESCE(wind_ms, 0) < 3`. Då räknas en trasig givare som stiltje, och
  raderna med saknad vind kommer med. Ett test visar det.
- Om villkoret innehåller `OR`, till exempel
  `wind_ms < 3 OR conditions = 'sun'`. En solig dag med okänd vind blir då
  sann via den andra delen.
- Om du frågar efter motsatsen. "Dagar som *inte* var lugna" kan inte
  skrivas som bara `wind_ms >= 3`; dagarna med okänd vind faller då bort
  ur båda frågorna. Ska de räknas måste du skriva `OR wind_ms IS NULL`.

Även när `IS NOT NULL` inte behövs gör den frågan tydligare. Den som läser
ser att du har tänkt på saknade värden.
