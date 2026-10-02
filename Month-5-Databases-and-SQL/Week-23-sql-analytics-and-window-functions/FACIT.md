# Facit vecka 23 — Try It Yourself

Varje svar ligger som en egen `.sql`-fil i [`facit/`](facit/). Kör dem
mot veckans databas med:

```bash
python3 facit/kor.py        # alla
python3 facit/kor.py u4     # bara uppgift 4
```

Testerna i [`tests/test_facit.py`](tests/test_facit.py) kontrollerar
varje svar och körs med resten av veckan: `python3 -m pytest -q`.

## 1. De två bästa butikerna per produkt

```sql
WITH units_per_store AS (
    SELECT product_id, store_id, SUM(units) AS units
    FROM daily_sales
    GROUP BY product_id, store_id
),
ranked AS (
    SELECT product_id, store_id, units,
           DENSE_RANK() OVER (PARTITION BY product_id ORDER BY units DESC) AS units_rank
    FROM units_per_store
)
SELECT p.name AS product, c.name AS city, r.units, r.units_rank
FROM ranked AS r
JOIN products AS p ON p.id = r.product_id
JOIN stores   AS s ON s.id = r.store_id
JOIN cities   AS c ON c.id = s.city_id
WHERE r.units_rank <= 2
ORDER BY p.id, r.units_rank, c.name;
```

| product | city | units | units_rank |
|---|---|---|---|
| Umbrella | Gothenburg | 61 | 1 |
| Umbrella | Oslo | 47 | 2 |
| Rain jacket | Stockholm | 18 | 1 |
| Rain jacket | Gothenburg | 17 | 2 |
| Wool socks | Kiruna | 32 | 1 |
| Wool socks | Umeå | 19 | 2 |
| Thermos | Kiruna | 32 | 1 |
| Thermos | Umeå | 4 | 2 |
| Sunglasses | Stockholm | 23 | 1 |
| Sunglasses | Oslo | 18 | 2 |

Tre steg: summera per produkt och butik, ranka inom varje produkt
(`PARTITION BY product_id`), och filtrera på placeringen. Filtret måste
ligga i ett steg *efter* rankningen. En fönsterfunktion räknas ut efter
`WHERE`, så `WHERE DENSE_RANK() OVER (...) <= 2` är inte tillåtet; därför
CTE:n `ranked`.

**Var finns delade placeringar?** Inte bland de två bästa. Den enda finns
längre ned: Umeå och Kiruna sålde 4 regnjackor var och delar sjätte
platsen. Där syns skillnaden mellan funktionerna: med `DENSE_RANK` skulle
nästa butik få plats 7, med `RANK` plats 8. (Kiruna sålde också 32 par
ullsockor och 32 termosar, men det är två olika produkter och alltså inte
en delad placering.)

Lägg också märke till att termosen bara finns i två butiker. En butik som
inte sålde en enda termos har ingen rad i `daily_sales` och rankas inte
alls; den hamnar inte "sist".

## 2. Två ökningar i rad

```sql
WITH daily AS (
    SELECT store_id, sold_on, SUM(revenue_sek) AS revenue_sek
    FROM daily_sales
    GROUP BY store_id, sold_on
),
with_history AS (
    SELECT store_id, sold_on, revenue_sek,
           LAG(revenue_sek, 1) OVER by_day AS one_day_before,
           LAG(revenue_sek, 2) OVER by_day AS two_days_before
    FROM daily
    WINDOW by_day AS (PARTITION BY store_id ORDER BY sold_on)
)
SELECT ...
FROM with_history AS h
...
WHERE h.two_days_before < h.one_day_before
  AND h.one_day_before < h.revenue_sek
ORDER BY c.name, h.sold_on;
```

Åtta butiksdagar, till exempel Göteborg den 23:e (2 043 → 6 531 → 7 327 kr)
och Kiruna den 23:e (1 911 → 2 110 → 5 013 kr).

`LAG(x, 2)` läser värdet två rader bakåt. `WINDOW by_day AS (...)` ger
fönstret ett namn så att det inte behöver skrivas två gånger. De två
första dagarna för varje butik saknar historik (`NULL`), och `NULL < ...`
är inte sant, så de faller bort av sig själva.

**En fälla:** `LAG` läser föregående *rad*, inte föregående *dag*. Om en
butik hade haft en dag helt utan försäljning hade den dagen saknat rad,
och `LAG` hade jämfört med dagen före den i stället. Här sålde alla
butiker något alla dagar (49 butiksdagar), och ett test kontrollerar det.
Annars hade man behövt bygga en fullständig lista över butiksdagar först,
som `q07` gör.

## 3. Intäkt per invånare

```sql
SELECT c.name AS city, c.population,
       ROUND(t.revenue_sek, 2) AS revenue_sek,
       ROUND(1000.0 * t.revenue_sek / c.population, 2) AS revenue_per_1000_inhabitants,
       RANK() OVER (ORDER BY t.revenue_sek / c.population DESC) AS per_inhabitant_rank,
       RANK() OVER (ORDER BY t.revenue_sek DESC)                AS total_revenue_rank
...
```

| city | per 1 000 invånare | rank per invånare | rank total |
|---|---|---|---|
| Kiruna | 927,50 | 1 | 5 |
| Visby | 480,79 | 2 | 7 |
| Umeå | 120,52 | 3 | 6 |
| Malmö | 65,16 | 4 | 4 |
| Gothenburg | 49,95 | 5 | 2 |
| Oslo | 40,28 | 6 | 3 |
| Stockholm | 33,92 | 7 | 1 |

**Rankningen vänds nästan helt.** Stockholm har störst intäkt men minst
per invånare; Kiruna och Visby, med lägst total, säljer mest per
invånare.

Vad det säger om totalsummor: **en total mäter mest storlek.** En butik i
en stad med en miljon invånare har fler kunder att sälja till, så en hög
total säger lite om hur bra butiken går. Att dela med något som mäter
storleken (invånare, butiksyta, antal besökare) gör butikerna jämförbara.
Men nyckeltalet har egna svagheter: Kiruna- och Visbybutikerna säljer
säkert till turister och till hela regionen, inte bara till kommunens
invånare, så "per invånare" överdriver deras försprång. Välj nämnaren
efter frågan du vill besvara.

`1000.0` med decimal gör att divisionen räknas med decimaler. Heltal delat
med heltal kan i vissa databaser ge ett avkortat heltal.

## 4. Söndagskampanjen för paraplyer

Facit jämför söndagen med butikens övriga dagar, och med övriga dagar som
hade **samma väder** som söndagen:

| city | söndagens väder | söndag | snitt övriga dagar | snitt dagar med samma väder | antal sådana dagar |
|---|---|---|---|---|---|
| Gothenburg | rain | 9 | 8,67 | 14,0 | 3 |
| Kiruna | cloud | 2 | 1,5 | 1,5 | 2 |
| Malmö | rain | 11 | 4,83 | 11,0 | 2 |
| Oslo | cloud | 5 | 7,0 | – | 0 |
| Stockholm | cloud | 4 | 6,17 | 5,0 | 1 |
| Umeå | cloud | 3 | 4,0 | 4,0 | 1 |
| Visby | cloud | 3 | 2,83 | 1,0 | 1 |

**Gick kampanjen bra? Det går inte att avgöra med den här datan.**

Jämförelsen med alla övriga dagar ser lovande ut för Malmö (11 mot 4,83),
men det regnade i Malmö på söndagen, och paraplyer säljer när det regnar
(`q07`). Jämfört med Malmös andra regndagar är söndagen exakt som vanligt,
11 mot 11. I Göteborg, som också hade regn, såldes *färre* paraplyer än på
andra regndagar. I de molniga städerna bygger jämförelsen på en eller två
dagar, eller ingen alls (Oslo hade ingen annan molnig dag).

Det man skulle behöva veta:

- **Hur söndagar brukar se ut utan kampanj.** Söndagar kan ha fler eller
  färre kunder än vardagar. Det kräver data från flera veckor.
- **Jämförbara dagar med samma väder**, och fler av dem. Vädret är den
  största påverkan på paraplyförsäljningen och kan dölja eller härma en
  kampanjeffekt.
- **En kontrollgrupp:** butiker som *inte* hade kampanj samma söndag.
  Hade alla butiker kampanj samtidigt går effekten inte att skilja från
  allt annat som hände den dagen.
- **Vad kampanjen kostade.** Paraplyerna såldes för 159,20 kr i stället
  för 199 kr (ett test visar det). För att intäkten ska öka måste
  försäljningen öka med minst 25 %, och för vinsten krävs ännu mer.

Det här är kärnan i analys av affärslogik: en siffra som ser bra ut är
inte ett bevis förrän man har frågat *jämfört med vad?*

## 5. Nederbörd och regnintäkt utan fan-out

```sql
WITH precipitation AS (
    SELECT city_id, ROUND(SUM(precipitation_mm), 1) AS precipitation_mm
    FROM observations
    GROUP BY city_id
),
rain_revenue AS (
    SELECT s.city_id, ROUND(SUM(ds.revenue_sek), 2) AS rain_revenue_sek
    FROM daily_sales AS ds
    JOIN products AS p ON p.id = ds.product_id
    JOIN stores   AS s ON s.id = ds.store_id
    WHERE p.category = 'rain'
    GROUP BY s.city_id
)
SELECT c.name AS city, pr.precipitation_mm, COALESCE(rr.rain_revenue_sek, 0) AS rain_revenue_sek
FROM cities AS c
JOIN precipitation     AS pr ON pr.city_id = c.id
LEFT JOIN rain_revenue AS rr ON rr.city_id = c.id
ORDER BY c.name;
```

Göteborg får 31,4 mm och 27 063,80 kr, Kiruna 10,3 mm och 5 705,40 kr,
och så vidare: samma nederbörd som `q05` i vecka 20.

**Regeln:** summera varje tabell för sig till *en rad per stad* innan de
joinas. Då har varje stad exakt en rad på varje sida, och joinen kan
inte duplicera något.

**Det felaktiga sättet** (`u5b`) joinar först och summerar sedan. Då paras
varje observation (7 per stad) ihop med varje försäljningsrad för
regnprodukter (14 per stad i Göteborg: paraplyer och regnjackor, sju
dagar). Göteborgs nederbörd räknas 14 gånger och blir 439,6 mm, och
intäkten räknas 7 gånger. Inget fel visas, bara orimliga siffror. Det
kallas *fan-out*.

**Hur facit kontrollerar att det inte sker:**

1. Antalet rader är 7, en per stad.
2. Nederbörden jämförs med en enkel summa direkt ur `observations`, utan
   join, och måste vara exakt lika för varje stad. Ett test gör det.
3. Ett test visar att den felaktiga versionen ger högre värden i båda
   kolumnerna.

Den andra kontrollen är den viktiga, och den går att göra med vilken
analysfråga som helst: räkna ut en av siffrorna på det enklaste möjliga
sättet och jämför.
