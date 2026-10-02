# Facit vecka 25 — Try It Yourself

Facit ligger i [`facit/`](facit/):

- [`facit/client.py`](facit/client.py) — `warmest_day` (uppgift 1) och
  `get_json` med nya försök (uppgift 2).
- [`facit/open_meteo.py`](facit/open_meteo.py) — maxvind i m/s (uppgift 3).
- [`facit/cli.py`](facit/cli.py) — kommandot `compare` (uppgift 4).

Testerna finns i [`tests/test_facit.py`](tests/test_facit.py) och körs med
resten av veckan: `python3 -m pytest -q`. Open-Meteo testas utan nätverk,
med ett svar i samma form som det riktiga API:et ger, precis som veckans
egna tester.

## 1. warmest_day

Testet först:

```python
def test_warmest_day(base_url):
    client = FacitWeatherClient(base_url)
    assert client.warmest_day("Kiruna")["observed_on"] == "2026-09-21"
```

Sedan koden:

```python
def warmest_day(self, city: str) -> dict:
    observations = self.observations(city)
    if not observations:
        raise ValueError(f"{city} has no observations")
    return max(observations, key=lambda observation: observation["temp_max_c"])
```

**En förfrågan eller flera? En.** `/cities/{name}/observations` skickar
alla observationer på en gång, och att hitta den största i en lista är
snabbt i Python. Att fråga en dag i taget skulle ge sju förfrågningar över
nätverket, var och en med sin väntetid, för samma information. Tumregel:
**varje förfrågan kostar tid, så hämta det du behöver i så få som
möjligt.** Ett test räknar förfrågningarna och kräver exakt en.

`max(..., key=...)` jämför på `temp_max_c` och lämnar den första vid
lika, alltså den tidigaste dagen eftersom API:et sorterar på datum.
Köpenhamn har inga observationer; då ger `max` på en tom lista ett
obegripligt fel, så metoden säger själv vad som är fel. En okänd stad
ger API:ets eget `404`.

## 2. Nya försök vid tillfälliga fel

```python
def get_json(url, timeout=5.0, retries=0, retry_delay=1.0, sleep=time.sleep):
    for attempt in range(retries + 1):
        try:
            return original.get_json(url, timeout=timeout)
        except ApiError as error:
            if error.status < 500 or attempt == retries:
                raise
        except ConnectionError:
            if attempt == retries:
                raise
        sleep(retry_delay)
```

**Varför behandlas 4xx och 5xx olika?**

- **4xx** betyder att *frågan* är fel: en stad som inte finns (`404`), ett
  datum i fel format (`400`). Samma fråga igen får samma svar. Ett nytt
  försök gör bara att användaren väntar längre och att servern får mer
  att göra.
- **5xx**, eller inget svar alls, betyder att något gick fel *hos servern
  eller på vägen*: den startar om, är överbelastad, nätverket hackar. Det
  kan fungera om en sekund.

`retries=2` betyder två *nya* försök, alltså högst tre förfrågningar. Efter
sista försöket kastas felet vidare, så den som anropar får veta att det
inte gick. Standardvärdet är 0, så befintlig kod beter sig som förut.

I riktiga program väntar man ofta allt längre för varje försök (1, 2, 4
sekunder; *exponential backoff*), så att tusen klienter som försöker igen
samtidigt inte sänker en server som håller på att komma tillbaka.

**Hur testar man 5xx?** Med en egen liten server som svarar med en
förbestämd lista statuskoder. Facits tester har en, `ScriptedServer`, som
till exempel svarar `503`, `500` och sedan `200`. Testerna räknar hur många
förfrågningar servern fick. Väntan är en parameter (`sleep`), så testerna
kan skicka in en funktion som bara antecknar hur länge den *skulle* ha
väntat, i stället för att faktiskt vänta.

## 3. Maxvind från Open-Meteo

```python
DAILY_VARIABLES = ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "wind_speed_10m_max"]
```

**Enheten:** Open-Meteo anger vindhastighet i **km/h** om man inte ber om
något annat. Resten av kursen använder m/s. Två sätt att lösa det, och
facit gör båda:

1. **Be om m/s.** Parametern `wind_speed_unit=ms` i URL:en.
2. **Kontrollera ändå.** Svaret talar om enheten i `daily_units`. Facit
   läser den och räknar om km/h till m/s (dela med 3,6, eftersom 1 km/h är
   1 000 m på 3 600 s). Om enheten är något helt annat säger facit ifrån
   med ett fel i stället för att visa fel siffror.

```python
WIND_TO_MS = {"m/s": 1.0, "km/h": 1 / 3.6}

unit = payload.get("daily_units", {}).get("wind_speed_10m_max", "km/h")
if unit not in WIND_TO_MS:
    raise ValueError(f"unexpected wind speed unit: {unit!r}")
```

Lärdom: lita inte blint på att ett API svarar som du bad om. Om svaret
talar om sin enhet, läs den.

Observera att `wind_speed_10m_max` är dagens **högsta** vind (10 meter
över marken), medan övnings-API:ets `wind_ms` är ett **medelvärde**. De
heter nästan samma sak men är inte samma mått, och kan inte jämföras
rakt av.

## 4. compare

```bash
# terminal 1
python -m api_client.practice_api
# terminal 2, från veckans mapp
PYTHONPATH=src python3 -m facit.cli compare Kiruna 2026-09-24
```

```
Kiruna, 2026-09-24
                    observed  Open-Meteo
high °C                  2.7         3.5
low °C                  -3.8        -2.0
precipitation mm         2.9         4.0
wind m/s                   -         9.3
(observed wind is the daily mean; Open-Meteo's is the daily maximum)
```

(Siffrorna i Open-Meteo-kolumnen kommer från testernas påhittade svar;
med nätverk får du riktiga värden.)

**Vad behöver du veta om varje stad?**

- **Koordinater.** Open-Meteo vill ha latitud och longitud, inte ett
  namn. Övnings-API:et har bara namn, land och folkmängd, så facit har en
  egen tabell, `CITY_COORDINATES`. (Ett riktigt program skulle slå upp dem
  med en *geokodnings*-tjänst; Open-Meteo har en sådan.)
- **Vilken dag som går att fråga om.** Open-Meteos prognos täcker från
  92 dagar bakåt (parametern `past_days`) till 16 dagar framåt. Övnings-
  datan är från september 2026, så facit räknar ut hur många dagar bakåt
  datumet ligger och ber om just det. Ett datum utanför intervallet ger ett
  tydligt fel.
- **Tidszon.** "Den 24 september" börjar vid olika tidpunkter på olika
  ställen. `timezone=auto` gör att Open-Meteo räknar dygnet i stadens egen
  tidszon, så att samma dag jämförs.

Att jämförelsen skrivs som en egen funktion, `compare`, med Open-Meteo-
anropet som parameter, gör att testerna kan ge den ett påhittat
Open-Meteo-svar och köra den mot det riktiga övnings-API:et utan
internet.

## 5. DELETE med curl

```bash
curl -i -X DELETE http://127.0.0.1:8000/cities/Kiruna
```

```
HTTP/1.0 405 Method Not Allowed
Server: BaseHTTP/0.6 Python/3.11.15
Date: Fri, 02 Oct 2026 07:20:00 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 47
Allow: GET

{
  "error": "this API is read-only: use GET"
}
```

`-X DELETE` väljer metoden, `-i` visar statusraden och alla headers.

- **Headern som säger vad klienten får göra i stället är `Allow: GET`.**
  `405 Method Not Allowed` betyder "adressen finns, men inte den här
  metoden", och HTTP-standarden kräver att ett `405`-svar har en
  `Allow`-header som räknar upp metoderna som fungerar.
- **Om API:et kunde ta bort städer, men staden inte fanns,** skulle svaret
  vara **`404 Not Found`**. Skillnaden är viktig: `405` säger att
  *metoden* inte går att använda på adressen, `404` att *saken* inte finns.

Ett test skickar samma `DELETE` från Python och kontrollerar status,
header och felmeddelande.
