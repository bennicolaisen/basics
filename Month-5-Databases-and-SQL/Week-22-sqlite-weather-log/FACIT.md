# Facit vecka 22 — Try It Yourself

Övningarna ändrar schemat, `store.py` och CLI:t. Facit ligger i
[`facit/`](facit/) och innehåller bara det som ändrats:

- [`facit/schema.sql`](facit/schema.sql) — schemat utan `ON DELETE CASCADE`
  och med en ny tabell, `warnings` (uppgift 3 och 4).
- [`facit/store.py`](facit/store.py) — de nya och ändrade funktionerna
  (uppgift 1–4). Resten importeras från `weather_log.store`.
- [`facit/cli.py`](facit/cli.py) — CLI:t med `rename-city` och ett tydligt
  besked när en stad inte kan tas bort (uppgift 2 och 3).

Testerna finns i [`tests/test_facit.py`](tests/test_facit.py) och körs
med resten av veckan: `python3 -m pytest -q`. Prova CLI:t med en **ny**
databasfil:

```bash
PYTHONPATH=src python3 -m facit.cli facit.db init
PYTHONPATH=src python3 -m facit.cli facit.db rename-city Visby Gotland
PYTHONPATH=src python3 -m facit.cli facit.db delete-city Kiruna
```

## 1. Lägg till eller ersätt (upsert)

```python
def record_or_replace(conn, observation):
    with conn:
        cursor = conn.execute(
            """
            INSERT INTO observations
                (city_id, observed_on, temp_max_c, temp_min_c, precipitation_mm, wind_ms, conditions)
            SELECT id, :observed_on, :temp_max_c, :temp_min_c, :precipitation_mm, :wind_ms, :conditions
            FROM cities
            WHERE name = :city
            ON CONFLICT (city_id, observed_on) DO UPDATE SET
                temp_max_c       = excluded.temp_max_c,
                temp_min_c       = excluded.temp_min_c,
                precipitation_mm = excluded.precipitation_mm,
                wind_ms          = excluded.wind_ms,
                conditions       = excluded.conditions
            """,
            asdict(observation),
        )
        if cursor.rowcount == 0:
            raise ValueError(f"unknown city: {observation.city!r}")
```

`ON CONFLICT (city_id, observed_on)` pekar på schemats regel
`UNIQUE (city_id, observed_on)`. Om raden skulle bryta mot den görs i
stället en `UPDATE` av raden som redan finns. `excluded` är namnet på
raden som *försökte* läggas till, så `excluded.temp_max_c` är det nya
värdet.

**Varför inte SELECT först, och sedan INSERT eller UPDATE?** Två skäl. Det
blir tre satser i stället för en. Och om två program skriver samtidigt kan
det andra hinna lägga till raden mellan ditt `SELECT` och ditt `INSERT`, så
att ditt `INSERT` kraschar. Med en enda sats sköter databasen det.

Testerna visar att antalet rader inte växer, att andra dagar och städer
inte påverkas, och att ersättningen fortfarande måste följa schemat (en
negativ nederbörd stoppas, och den gamla raden finns kvar).

## 2. rename-city

Testerna skrevs först, och de bestämmer beteendet:

- Ett ledigt namn: staden byter namn och behåller sina observationer.
- Ett upptaget namn: ett tydligt fel, `CityNameTakenError`, och
  **ingenting ändras**.
- Ett okänt gammalt namn eller ett tomt nytt namn: `ValueError`.

```python
def rename_city(conn, old, new):
    if not new or not new.strip():
        raise ValueError("the new name must not be blank")
    try:
        with conn:
            cursor = conn.execute("UPDATE cities SET name = ? WHERE name = ?", (new, old))
    except sqlite3.IntegrityError:
        raise CityNameTakenError(f"there is already a city called {new!r}") from None
    if cursor.rowcount == 0:
        raise ValueError(f"unknown city: {old!r}")
```

**Vilket lager bestämmer?** Alla tre, med olika uppgifter:

- **Databasen** avgör *om* namnet är upptaget. `name TEXT NOT NULL UNIQUE`
  gäller för alla program som skriver i filen, och även när två skriver
  samtidigt. Att först fråga `SELECT ... WHERE name = ?` och sedan
  uppdatera har samma lucka som i uppgift 1.
- **`store.py`** översätter databasens fel (`IntegrityError: UNIQUE
  constraint failed: cities.name`) till ett fel som säger vad som hände
  i programmets egna ord, `CityNameTakenError`. Det ärver från
  `ValueError`, så kod som redan fångar `ValueError` fungerar som förut.
- **CLI:t** bestämmer bara hur det visas för användaren:
  `cannot rename: there is already a city called 'Oslo'`.

## 3. Ingen kaskad

I schemat tas `ON DELETE CASCADE` bort:

```sql
city_id INTEGER NOT NULL REFERENCES cities (id),
```

Utan det är standardbeteendet att vägra: när `PRAGMA foreign_keys = ON`
är påslaget kan en stad inte tas bort så länge någon rad pekar på den.
SQLite svarar då med `IntegrityError: FOREIGN KEY constraint failed`.

`delete_city` fångar det felet och tar reda på *varför*:

```python
except sqlite3.IntegrityError:
    observations, warnings = conn.execute(...).fetchone()
    raise CityInUseError(
        f"{name} still has {observations} observation(s) and {warnings} warning(s); "
        "delete those first if the city really should go"
    ) from None
```

CLI:t visar:

```
cannot delete: Kiruna still has 7 observation(s) and 0 warning(s); delete those first if the city really should go
```

Meddelandet säger tre saker: **att** det inte gick, **varför**, och **vad
användaren kan göra**. Varningar räknas också, eftersom tabellen från
uppgift 4 pekar på `cities` på samma sätt.

**Viktigt om befintliga databaser:** `CREATE TABLE IF NOT EXISTS` gör
ingenting om tabellen redan finns. En databasfil som skapades med veckans
schema har alltså kvar `ON DELETE CASCADE`, även om programmet nu läser
facit-schemat. Att ändra en främmande nyckel i en befintlig SQLite-tabell
kräver att tabellen byggs om: skapa en ny tabell, kopiera raderna, ta bort
den gamla och byt namn. Sådana ändringar av en databas som redan används
kallas *migreringar*. Prova därför facit med en ny fil.

## 4. Varningar

```sql
CREATE TABLE IF NOT EXISTS warnings (
    id         INTEGER PRIMARY KEY,
    city_id    INTEGER NOT NULL REFERENCES cities (id),
    level      TEXT    NOT NULL CHECK (level IN ('yellow', 'orange', 'red')),
    message    TEXT    NOT NULL CHECK (trim(message) <> ''),
    starts_on  TEXT    NOT NULL CHECK (date(starts_on) IS starts_on),
    ends_on    TEXT    NOT NULL CHECK (date(ends_on) IS ends_on),
    CHECK (starts_on <= ends_on)
);
```

Utöver reglerna uppgiften kräver (nivån, och att en varning inte slutar
innan den börjar) kontrollerar facit att texten inte är tom och att
datumen verkligen är datum i formatet `YYYY-MM-DD`, med samma knep som
`observed_on` i veckans schema. Ett parametriserat test provar varje regel.

```python
def active_warnings(conn, on_date):
    return conn.execute(
        """
        SELECT c.name, w.level, w.message, w.starts_on, w.ends_on
        FROM warnings AS w
        JOIN cities AS c ON c.id = w.city_id
        WHERE ? BETWEEN w.starts_on AND w.ends_on
        ORDER BY c.name, w.starts_on
        """,
        (on_date,),
    ).fetchall()
```

Datumet är en **parameter** (`?`), aldrig inklistrat i SQL-texten. Ett test
skickar in injektionstexten som datum och får en tom lista tillbaka.
`add_warning` använder samma `INSERT ... SELECT` som `record`, så stadens
namn slås upp och kontrolleras i samma sats.

## 5. SQL-injektion

Den sårbara versionen:

```python
def unsafe_city_observations(conn, city):
    return conn.execute(
        "SELECT o.observed_on FROM observations AS o "
        f"JOIN cities AS c ON c.id = o.city_id WHERE c.name = '{city}'"
    ).fetchall()
```

Med `city = "' OR '1'='1"` blir SQL-texten

```sql
... WHERE c.name = '' OR '1'='1'
```

`'1'='1'` är alltid sant, så **alla** observationer kommer tillbaka, för
alla städer. Användarens text har blivit en del av frågan.

Facit följer uppgiften: den sårbara funktionen finns inte i någon
programfil. Den lever bara inne i ett test (`TestInjection`), som bevis på
att attacken fungerar mot en f-sträng. Testet bredvid skickar samma text
till den riktiga `city_observations`, som använder en parameter och får
en tom lista: texten behandlas som ett stadsnamn, och ingen stad heter så.
Veckans eget injektionstest i `test_store.py` använder samma indata.

Lärdomen gäller alltid, inte bara i SQLite: **sätt aldrig in text utifrån
i SQL med f-strängar, `+` eller `%`.** Använd parametrar (`?` eller
`:namn`). Det enda som inte kan vara en parameter är namn på tabeller och
kolumner; de ska i så fall väljas ur en fast lista i programmet, aldrig
tas direkt från användaren.
