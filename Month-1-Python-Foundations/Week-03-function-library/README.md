# Vecka 3 — Funktioner på djupet

## Syfte

Funktioner är det viktigaste verktyget för att hålla ordning i ett
program. Ett program med en enda lång följd av rader blir snabbt omöjligt
att läsa, ändra och testa. Med funktioner delar du upp ett problem i små
delar som var och en gör en sak, har ett namn som säger vad, och kan
testas för sig. Den här veckan lär du dig allt du behöver om funktioner
för resten av kursen: standardvärden, namngivna argument, var variabler
"finns", dokumentation, att avvisa ogiltiga värden, och att skriva egna
tester. Veckans projekt är ett litet bibliotek med funktioner för
statistik och text, och ett avskräckande exempel på hur det ser ut utan
dem.

## Mål

När veckan är klar kan du:

- ge parametrar standardvärden och anropa funktioner med namngivna argument
- förklara skillnaden mellan lokala variabler och variabler utanför en
  funktion, och varför `return` är rätt sätt att få ut ett svar
- skriva dokumentationstexter (docstrings) och typannoteringar
- avvisa ogiltiga värden med `raise ValueError` och testa att det sker
- dela upp ett stort problem i små funktioner som använder varandra
- importera från Pythons standardbibliotek och från dina egna filer
- skriva egna tester med `assert`, `pytest.approx` och `pytest.raises`

## Genomgång

Övningarna finns i `ovningar/` och kontrolleras med
`python -m pytest kontroll -k 05` (byt 05 mot övningens nummer).

### Steg 1: Repetition och funktioner som anropar funktioner

En funktion tar emot **argument** via sina **parametrar**, gör något och
**returnerar** ett svar:

```python
def area(width, height):
    return width * height
```

En funktion kan anropa andra funktioner, och svaret från en funktion kan
skickas direkt in i en annan:

```python
def is_even(number):
    return number % 2 == 0

def is_odd(number):
    return not is_even(number)

print(round(area(2.5, 3.3), 1))    # area räknas först, sedan round
```

Att bygga nya funktioner av gamla gör att varje regel står på ett enda
ställe. Om `is_even` hade ett fel skulle du bara behöva rätta det där, och
`is_odd` skulle bli rätt samtidigt.

**Öva:** övning 3.6 och 3.7.

### Steg 2: Standardvärden och namngivna argument

En parameter kan få ett **standardvärde** (*default*), som används om
anroparen inte skickar något:

```python
def greet(name, greeting="Hej"):
    return f"{greeting}, {name}!"

greet("Bo")             # "Hej, Bo!"
greet("Bo", "Tjena")    # "Tjena, Bo!"
```

Parametrar med standardvärde måste stå **efter** dem utan.

Argument kan skickas i ordning (**positionella** argument) eller med namn
(**namngivna** argument, *keyword arguments*). Namngivna argument gör
anropet tydligare och låter dig hoppa över parametrar du är nöjd med:

```python
def format_temperature(value, unit="C", decimals=1):
    return f"{round(value, decimals)} °{unit}"

format_temperature(21.46)                  # "21.5 °C"
format_temperature(21.46, decimals=2)      # "21.46 °C"   (unit behåller "C")
```

Du har redan använt namngivna argument: `round(x, ndigits=2)` och
`print("a", "b", sep="-")`.

**Öva:** övning 3.1, 3.4 och 3.10.

### Steg 3: None och funktioner utan return

En funktion som aldrig når ett `return` (eller som bara skriver `return`)
returnerar ett specialvärde: **`None`**, som betyder "inget värde".

```python
def say_hello(name):
    print(f"Hej, {name}!")

result = say_hello("Bo")    # skriver ut Hej, Bo!
print(result)               # None
```

Det är vanligt att få `None` av misstag, när man skrivit `print` i stället
för `return`. Ser du `None` där du väntade dig ett svar, leta efter en
funktion som saknar `return`. Kontrollerna i `kontroll/` säger till
exempel "returnerade None" när en övning inte är löst.

För att fråga om något är `None` skriver man `if result is None:`.

### Steg 4: Var finns variablerna? (räckvidd)

En variabel som skapas inne i en funktion, eller en parameter, är
**lokal**: den finns bara medan funktionen körs, och syns inte utanför.

```python
def add_vat(price):
    total = price * 1.25    # total är lokal
    return total

add_vat(100)
print(total)    # NameError: name 'total' is not defined
```

Det är en fördel: du kan använda namn som `total` och `count` i många
funktioner utan att de krockar.

Det betyder också att en funktion inte kan ändra en variabel utanför
genom att ändra sin parameter:

```python
count = 0

def add_one(count):
    count = count + 1    # ändrar bara den lokala count

add_one(count)
print(count)    # fortfarande 0
```

Rätt sätt är att **returnera** det nya värdet och låta den som anropar
spara det: `count = add_one(count)`. Funktioner som bara tar in
argument och returnerar ett svar, utan att ändra något utanför, är
lättast att förstå och testa.

Konstanter, som `KM_PER_MILE` i vecka 1, skapas utanför funktionerna och
kan **läsas** inifrån dem. Det är okej eftersom de aldrig ändras.

**Öva:** övning 3.5.

### Steg 5: Dokumentation och typannoteringar

Den första raden i en funktion kan vara en **docstring**, en text inom
`"""` som förklarar vad funktionen gör:

```python
def percent(part: float, whole: float) -> float:
    """Hur många procent part är av whole, avrundat till en decimal."""
    return round(part / whole * 100, 1)
```

`: float` efter en parameter och `-> float` efter parentesen är
**typannoteringar** (*type hints*). De berättar vilken typ som förväntas
in och vad som kommer ut. Python kontrollerar dem inte när programmet
körs, men de gör koden lättare att läsa och VS Code använder dem för att
hjälpa dig. Exempel:

| Annotering | Betyder |
|---|---|
| `name: str` | text |
| `count: int` | heltal |
| `price: float` | decimaltal (heltal godtas också) |
| `ok: bool` | `True` eller `False` |
| `numbers: list[float]` | en lista med decimaltal |
| `-> None` | returnerar inget |

Från och med nu har koden i kursen typannoteringar.

### Steg 6: Avvisa ogiltiga värden

En funktion bör kontrollera sina argument i början och **kasta ett fel**
om den inte kan ge ett vettigt svar:

```python
def mean(numbers: list[float]) -> float:
    if len(numbers) == 0:
        raise ValueError("mean() behöver minst ett tal")
    return sum(numbers) / len(numbers)
```

Varför inte returnera 0? För att 0 ser ut som ett riktigt svar. Ett
program som räknar medeltemperaturen för en vecka utan mätningar och får
0 °C kommer glatt att använda det. Ett `ValueError` stoppar programmet på
rätt ställe med ett meddelande som säger vad som var fel.

Det har en sida till: kontrollera ogiltiga värden **en gång**, där de
kommer in, i stället för överallt i programmet.

**Öva:** övning 3.8, 3.9, 3.15 och 3.16.

### Steg 7: Dela upp ett problem

Ett stort problem blir lätt om man delar upp det i små. Ta "räkna ut
priset för en kundvagn med rabatt":

```python
def subtotal(prices: list[float]) -> float:
    return sum(prices)

def apply_discount(amount: float, percent: float) -> float:
    return amount - amount * percent / 100

def total_price(prices: list[float], discount_percent: float = 0) -> float:
    return round(apply_discount(subtotal(prices), discount_percent), 2)
```

Tecken på att en funktion borde delas upp:

- Den är längre än vad som får plats på skärmen.
- Du behöver en kommentar för att förklara vad ett stycke av den gör.
  Gör stycket till en funktion och låt namnet förklara.
- Den gör flera saker: räknar *och* skriver ut, eller räknar två olika
  saker.

Veckans projekt har ett exempel på motsatsen: `legacy_report.py`.

**Öva:** övning 3.11, 3.12 och 3.13.

### Steg 8: Moduler och import

En **modul** är en Python-fil. Med `import` använder du kod från andra
filer.

Pythons **standardbibliotek** har hundratals moduler. Några exempel:

```python
import math
print(math.pi)           # 3.141592653589793
print(math.sqrt(16))     # 4.0

import random
print(random.choice(["sol", "regn", "snö"]))
```

Från dina egna filer importerar du på samma sätt. Med `from ... import
...` hämtar du enskilda namn, så att du slipper skriva modulnamnet varje
gång:

```python
from function_library.stats import mean, median
print(mean([1, 2, 3]))
```

`function_library` är en mapp med Python-filer (ett **paket**), och
`stats` är filen `stats.py` i den. Importer skrivs överst i filen.

**Öva:** övning 3.2.

### Steg 9: Skriv egna tester

Hittills har du kört tester som någon annan skrivit. Nu skriver du egna.
En testfil heter `test_något.py`, och varje test är en funktion vars namn
börjar med `test_`:

```python
import pytest
from function_library.stats import mean


def test_mean_of_four_numbers():
    assert mean([1, 2, 3, 4]) == pytest.approx(2.5)


def test_mean_of_one_number():
    assert mean([5]) == 5


def test_mean_of_empty_list_raises():
    with pytest.raises(ValueError):
        mean([])
```

- `assert` påstår att något är sant.
- `pytest.approx` jämför decimaltal med en liten tolerans (vecka 1).
- `with pytest.raises(ValueError):` påstår att koden i blocket ska kasta
  ett `ValueError`. Testet misslyckas om det **inte** gör det.

Vad är ett bra test? Ett som skulle misslyckas om funktionen hade ett
fel. Pröva:

- ett vanligt fall
- gränser och specialfall: tom lista, ett enda värde, noll, negativa tal
- varje parameter, både med standardvärdet och ändrat
- att ogiltiga värden avvisas

Ett test per sak, med ett namn som säger vad som prövas. När ett test
misslyckas vet du då direkt vad som är fel.

**Öva:** övning 3.14. Där kontrollerar kontrollen dina tester: de måste
avslöja tre felaktiga versioner av en funktion.

## Veckans projekt: ett funktionsbibliotek

```
Week-03-function-library/
├── starta.py                        - räkna statistik på egna tal: python starta.py
├── src/
│   └── function_library/
│       ├── stats.py                 - mean, median, mode, stddev
│       ├── text_utils.py            - word_count, is_palindrome
│       └── legacy_report.py         - DÅLIGT EXEMPEL: allt i en funktion
├── tests/
│   ├── test_stats.py
│   ├── test_text_utils.py
│   └── test_facit_prova_sjalv.py
├── ovningar/  kontroll/  facit/
└── FACIT.md
```

Börja med **`legacy_report.py`**. Funktionen `handle_data(d, t)` räknar
fyra olika statistiska mått, analyserar en text och skriver ut alltihop.
Den fungerar, men:

- Namnen (`d`, `t`, `s`, `c`, `bc`, `k`) säger ingenting.
- Inget av det den räknar kan återanvändas: vill du bara ha medianen
  måste du kopiera kod.
- Den går inte att testa en del i taget, och eftersom den skriver ut i
  stället för att returnera är den svår att testa alls.

Jämför med **`stats.py`** och **`text_utils.py`**, som räknar exakt samma
saker. Varje mått är en egen funktion med ett tydligt namn, en docstring,
typannoteringar och en kontroll av tom lista. Några saker att lägga märke
till:

- `median` sorterar med `sorted(numbers)`, som ger en **ny** sorterad lista
  utan att ändra den som skickades in.
- `mode` använder `numbers.count(value)` och går igenom värdena i
  sorterad ordning, så att det minsta talet vinner vid lika antal.
- `stddev` anropar `mean` i stället för att räkna medelvärdet en gång
  till.
- `is_palindrome` har två parametrar med standardvärden, så att det
  vanliga anropet blir enkelt (`is_palindrome("Ni talar bra latin")`) men
  den som vill kan kräva exakt likhet.

Testerna i `tests/` prövar varje funktion för sig, med vanliga fall,
specialfall och tom lista.

## Köra programmet

```
python starta.py
```

Skriv några tal med mellanslag mellan, till exempel `1 2 2 3 10`, och
sedan en mening.

## Testa

```
python -m pytest                   # testerna för veckans projekt
python -m pytest kontroll          # kontrollerna av dina övningar
python -m pytest kontroll --facit  # visar att facit klarar alla kontroller
```

## Prova själv

1. **Huvuduppgiften:** skriv om `handle_data` som en ny funktion
   `build_report(numbers, text)` som anropar funktionerna i `stats.py` och
   `text_utils.py` i stället för att räkna själv, och som **returnerar**
   rapporten som text i stället för att skriva ut den. Skriv ett test som
   visar att den ger samma rapport som `handle_data` skriver ut.
2. Lägg till `variance(numbers)` (medelvärdet av de kvadrerade
   avvikelserna) i `stats.py`, och skriv om `stddev` så att den bara
   returnerar roten ur variansen.
3. Lägg till `most_common_word(text)` i `text_utils.py`. Den ska inte bry
   sig om stora och små bokstäver, och vid lika antal ska ordet som kommer
   först i bokstavsordning vinna. Vad ska hända med en tom text?
4. `mode` väljer det minsta värdet vid lika antal. Skriv `modes(numbers)`
   som i stället returnerar **alla** värden som delar förstaplatsen, som
   en sorterad lista.
5. Skriv `summary(numbers, decimals=2)` som returnerar en rad i stil med
   `"medel 2.5, median 2.5, typvärde 1, standardavvikelse 1.12"`, där
   `decimals` styr avrundningen.

## Facit

- Lösningar till övning 3.1–3.16 finns i `facit/`, med samma filnamn som
  i `ovningar/`.
- Lösningar till "Prova själv" finns i `facit/prova_sjalv.py`, med
  förklaringar i [`FACIT.md`](FACIT.md).
