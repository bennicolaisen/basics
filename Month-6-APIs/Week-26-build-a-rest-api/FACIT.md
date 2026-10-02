# Facit vecka 26 — Try It Yourself

Facit ligger i [`facit/`](facit/), uppdelat i samma tre lager som veckans
projekt:

- [`facit/store.py`](facit/store.py) — de nya SQL-funktionerna.
- [`facit/app.py`](facit/app.py) — de nya endpoints och kontrollen av
  API-nyckeln. Allt oförändrat återanvänds från `weather_api.app`.
- [`facit/server.py`](facit/server.py) — servern som läser nyckeln vid
  start och skickar headers vidare.
- [`facit/client.py`](facit/client.py) — vecka 25:s klient med
  `add_observation` (uppgift 5).

Testerna finns i [`tests/test_facit.py`](tests/test_facit.py) och körs med
resten av veckan: `python3 -m pytest -q`. Prova servern:

```bash
export WEATHER_API_KEY=hemligt          # PowerShell: $env:WEATHER_API_KEY="hemligt"
PYTHONPATH=src python3 -m facit.server facit.db --sample
```

## Kontraktet efter alla uppgifter

De nya raderna är markerade med **fet stil**.

| Method | Path | Success | Can fail with |
|---|---|---|---|
| GET | `/cities` | 200, list of cities | |
| POST | `/cities` | 201, the city, `Location` | 400, 401, 409 |
| GET | `/cities/{name}` | 200, the city | 404 |
| **DELETE** | **`/cities/{name}`** | **204, deletes the city *and all its observations*** | **401, 404** |
| **GET** | **`/cities/{name}/summary?from=&to=`** | **200, count, average high, total precipitation** | **400 bad date or from after to, 404** |
| GET | `/cities/{name}/observations?from=&to=` | 200, list | 400, 404 |
| POST | `/cities/{name}/observations` | 201, the observation, `Location` | 400, 401, 404, 409 |
| GET | `/cities/{name}/observations/{date}` | 200, the observation | 404 |
| **PATCH** | **`/cities/{name}/observations/{date}`** | **200, the updated observation** | **400 invalid, 401, 404** |
| DELETE | `/cities/{name}/observations/{date}` | 204, no body | 401, 404 |

**401** gäller alla skrivande anrop (POST, PATCH, DELETE) när servern
startats med en nyckel och anropet saknar rätt `X-API-Key`.

## 1. PATCH

Testerna först. De bestämmer statuskoderna:

| Situation | Svar |
|---|---|
| Några giltiga fält | `200` och hela observationen efter ändringen |
| Tom kropp `{}` | `400`, inget att ändra |
| `observed_on` i kroppen | `400`, datumet går inte att ändra |
| Okänt fält, fel typ, inte JSON | `400` |
| Värden som bryter mot schemat (lägsta över högsta) | `400`, och ingenting ändras |
| Staden eller dagen finns inte | `404` |

Två designbeslut:

- **`observed_on` kan inte ändras**, eftersom datumet är en del av
  adressen: `/cities/Oslo/observations/2026-09-21`. Om det ändrades skulle
  saken plötsligt finnas på en annan adress. Den som vill flytta en
  observation tar bort den och skapar en ny.
- **En tom PATCH är ett fel**, inte en ändring av ingenting. Ett tomt
  objekt är nästan alltid ett misstag hos klienten, och det är bättre att
  säga det.

`409` behövs inte: eftersom datumet inte kan ändras kan en PATCH aldrig
krocka med en annan observation.

SQL:en bygger `SET`-delen av fältnamnen:

```python
columns = [name for name in PATCHABLE_FIELDS if name in changes]
assignments = ", ".join(f"{name} = :{name}" for name in columns)
```

Det är en f-sträng i SQL, vilket vecka 22 varnade för. Här är det säkert
av ett skäl: **namnen kommer från `PATCHABLE_FIELDS`, en fast lista i
programmet**, inte från klienten. Klientens fältnamn har redan kontrollerats
mot listan i `app.py`, och värdena går som vanligt som parametrar.

Schemats `CHECK`-regler kontrolleras på hela raden *efter* ändringen. En
PATCH som bara skickar `{"temp_min_c": 30}` stoppas därför, eftersom dagens
högsta var 14,9. Det får man gratis när reglerna ligger i databasen.

## 2. DELETE /cities/{name}

Schemat har redan bestämt vad som händer med observationerna:

```sql
city_id INTEGER NOT NULL REFERENCES cities (id) ON DELETE CASCADE,
```

**De tas bort tillsammans med staden.** API:et ska säga samma sak som
schemat, så kontraktet säger uttryckligen "deletes the city *and all its
observations*", och testet kontrollerar att Kirunas sju observationer
försvann och att de andra 42 är kvar.

Svaret är `204` utan kropp, som när en observation tas bort, och `404` om
staden inte finns. `405`-svaret för `/cities/{name}` räknar nu upp
`Allow: DELETE, GET`, utan att någon kod för det behövdes; `handle` bygger
listan ur `ROUTES`.

Är kaskad rätt val här? För ett väder-API är det rimligt: observationer
utan stad betyder ingenting. Men det betyder också att ett enda anrop kan
ta bort hundratals rader, vilket är ett skäl till uppgift 4.

## 3. Sammanfattning

```sql
SELECT c.name AS city,
       COUNT(o.id)                                    AS observations,
       ROUND(AVG(o.temp_max_c), 1)                    AS average_high_c,
       ROUND(COALESCE(SUM(o.precipitation_mm), 0), 1) AS total_precipitation_mm
FROM cities AS c
LEFT JOIN observations AS o
       ON o.city_id = c.id
      AND o.observed_on BETWEEN :start AND :end
WHERE c.name = :city
GROUP BY c.id, c.name
```

```bash
curl "http://127.0.0.1:8000/cities/Stockholm/summary?from=2026-09-23&to=2026-09-25"
```

```json
{
  "city": "Stockholm",
  "observations": 3,
  "average_high_c": 13.8,
  "total_precipitation_mm": 9.5,
  "from": "2026-09-23",
  "to": "2026-09-25"
}
```

Beräkningen sker i SQL, inte i Python, och datumvillkoret står i **`ON`**,
inte i `WHERE` (vecka 21, uppgift 3). Då ger ett intervall utan
observationer ändå en rad: antal 0, medelvärde `null` (det finns inget att
räkna ett medelvärde på) och nederbörd 0. Med villkoret i `WHERE` hade
raden försvunnit och API:et hade inte haft något att svara.

`from` och `to` återanvänder veckans `_date_param`, så ett felaktigt datum
ger samma `400` som för observationslistan. Facit lägger till ett fall
till: `from` efter `to` är också `400`. Intervallet skickas tillbaka i
svaret när klienten har angett det, så att svaret går att förstå på egen
hand.

## 4. API-nyckel

**Var hör kontrollen hemma?** I `app.py`, och nyckeln läses i `server.py`.

- **`store.py`** vet ingenting om HTTP, headers eller vem som frågar. Den
  ska kunna användas av ett skript eller ett test utan nyckel.
- **`app.py`** bestämmer API:ets regler: vilka adresser som finns, vilka
  metoder som är tillåtna, vilken statuskod som gäller. "Skrivande anrop
  kräver en nyckel" är en sådan regel, och den kan testas genom att anropa
  `handle` direkt, utan nätverk, som resten av API:et.
- **`server.py`** flyttar bara bytes. Men den är den del som startar
  programmet, så det är där miljövariabeln läses, *en gång*, och skickas
  vidare till `handle` tillsammans med varje förfrågans headers.

```python
if api_key is not None and method in WRITE_METHODS and not _authorized(headers, api_key):
    return Response(
        401,
        {"error": "missing or wrong API key; send it in the X-API-Key header"},
        {"WWW-Authenticate": 'ApiKey header="X-API-Key"'},
    )
```

Detaljer som är värda att lägga märke till:

- **Kontrollen görs först**, före routingen. En klient utan nyckel får
  `401` för varje skrivande anrop och kan inte ens ta reda på vilka
  adresser som finns.
- **`hmac.compare_digest`** jämför nyckeln. En vanlig `==` slutar vid
  första tecknet som skiljer sig, och det tar mätbart olika lång tid.
  Med tillräckligt många försök kan man då gissa fram nyckeln tecken för
  tecken. `compare_digest` tar lika lång tid oavsett.
- **Headernamn är inte skiftlägeskänsliga** i HTTP: `X-API-Key` och
  `x-api-key` är samma header. Testet skickar den med små bokstäver.
- **`401` ska ha en `WWW-Authenticate`-header** som säger hur man
  autentiserar sig. HTTP-standarden kräver det.
- **Saknas miljövariabeln startar servern inte.** Hellre ingen server än
  en server som av misstag är öppen för alla. (Utan nyckel, som i
  testerna, är `handle` öppen, precis som veckans original.)
- **Nyckeln ligger i en miljövariabel**, aldrig i koden. Kod hamnar i git
  och delas; en nyckel i koden är en nyckel som alla med tillgång till
  repot kan läsa.

En API-nyckel över vanlig `http://` skickas i klartext. Ett riktigt API
med nycklar körs alltid över `https://`.

## 5. add_observation i klienten

```python
def add_observation(self, city: str, observation: dict) -> dict:
    headers = {"X-API-Key": self.api_key} if self.api_key else {}
    url = build_url(self.base_url, ["cities", city, "observations"])
    return send_json("POST", url, observation, headers)
```

`send_json` är `get_json`s motsvarighet för metoder med en kropp. Den
skickar JSON med `Content-Type: application/json` och gör om felsvar till
`ApiError` på samma sätt, så att anroparen kan läsa statuskoden:

```python
try:
    client.add_observation("Oslo", observation)
except ApiError as error:
    if error.status == 409:
        print("Den dagen finns redan.")
```

Metoden returnerar observationen **som servern sparade den**, inte den
som skickades. Det är servern som avgör vad som faktiskt lagrades, till
exempel om ett fält fick ett standardvärde.

`build_url` från vecka 25 procentkodar stadsnamnet, så `Malmö` fungerar.
Testerna kör klienten mot facit-servern över riktig HTTP och provar
`400` (ogiltigt väder), `404` (okänd stad), `409` (dagen finns redan) och
`401` (ingen nyckel).

Klienten bor i vecka 25:s mapp, så `facit/client.py` lägger till den
mappen i `sys.path` för att kunna importera den. I ett riktigt projekt
skulle klienten vara ett eget paket som installeras med `pip`, och
servern och klienten skulle kunna utvecklas var för sig så länge båda
följer kontraktet.
