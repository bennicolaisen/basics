# Facit vecka 1 — Prova själv

Koden finns i [`facit/prova_sjalv.py`](facit/prova_sjalv.py) och testerna
i [`tests/test_facit_prova_sjalv.py`](tests/test_facit_prova_sjalv.py).
I ett riktigt projekt skulle du lägga funktionerna direkt i
`converters.py`; i facit ligger de i en egen fil så att veckans
referenskod står kvar orörd.

Facit till de små övningarna 1.1–1.18 finns i mappen [`facit/`](facit/).

## 1. Kelvin

```python
KELVIN_AT_ZERO_CELSIUS = 273.15

def celsius_to_kelvin(celsius):
    return celsius + KELVIN_AT_ZERO_CELSIUS

def kelvin_to_celsius(kelvin):
    return kelvin - KELVIN_AT_ZERO_CELSIUS
```

Kelvin och Celsius har lika stora steg; skalorna är bara förskjutna 273.15
grader. Därför räcker plus och minus. Talet ligger i en konstant, av samma
skäl som `KM_PER_MILE`: det står på ett ställe och har ett namn.

Bra tester: 0 °C ska bli 273.15 K, 0 K (absoluta nollpunkten) ska bli
-273.15 °C, och fram och tillbaka ska ge samma tal. Använd
`pytest.approx`, eftersom 273.15 är ett decimaltal.

## 2. Från timmar, minuter och sekunder till sekunder

```python
def hms_to_seconds(hours, minutes, seconds):
    return hours * 3600 + minutes * 60 + seconds
```

En timme är 60 · 60 = 3600 sekunder och en minut 60 sekunder. Det bästa
testet kombinerar de två funktionerna: `seconds_to_hms(hms_to_seconds(25,
1, 1))` ska bli `"25:01:01"`. Ett sådant test fångar fel i båda
funktionerna på en gång.

## 3. Hastigheter

```python
def mph_to_kmh(mph):
    return miles_to_km(mph)

def kmh_to_mph(kmh):
    return km_to_miles(kmh)
```

En hastighet är en sträcka per timme. Att gå från mph till km/h är
alltså samma omvandling som från engelska mil till kilometer; "per timme"
ändras inte. Genom att anropa de befintliga funktionerna finns
omvandlingsfaktorn fortfarande på ett enda ställe. Om någon rättar den
blir även hastigheterna rätt.

## 4. Fråga efter hastighet i programmet

Lägg till två rader sist i `main()`:

```python
    kmh = float(input("Hastighet i km/h: "))
    print(f"{kmh} km/h är {kmh_to_mph(kmh):.1f} mph")
```

Mönstret är detsamma som för de andra frågorna: `input` ger text, `float`
gör om den till ett tal, funktionen räknar, och f-strängen med `:.1f`
visar en decimal. Testet i facit ersätter `input` med en funktion som
svarar automatiskt, så att programmet kan köras utan att någon skriver.

## 5. Decimaltal är inte exakta

```python
def test_floats_are_not_exact():
    assert 0.1 + 0.2 != 0.3
    assert 0.1 + 0.2 == 0.30000000000000004

def test_approx_compares_with_a_tolerance():
    assert 0.1 + 0.2 == pytest.approx(0.3)
```

Datorn lagrar decimaltal binärt (med ettor och nollor). Precis som 1/3
inte kan skrivas exakt med decimaler (0.3333…) kan 0.1 inte skrivas exakt
binärt. Felet är mycket litet, men `==` kräver exakt likhet och säger
därför nej. `pytest.approx` godtar en mycket liten skillnad, så testet
kontrollerar att räkningen är rätt i stället för datorns sista decimal.
Tumregel: jämför aldrig decimaltal med `==` i tester.
