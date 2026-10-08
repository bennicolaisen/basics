# Vecka 1 — Python: grunderna

## Syfte

Veckan bygger grunden som resten av kursen står på: att köra program,
läsa felmeddelanden, variabler och typer, räkna, arbeta med text, läsa in
data, skriva funktioner och testa dem. Inga förkunskaper krävs, men
genomgången är kort och går rakt på sak.

Övningarna säger **vad** programmet ska göra, aldrig **hur**. Räkna med
att experimentera, läsa felmeddelanden och slå upp saker i Pythons
dokumentation, <https://docs.python.org/3/>. Det är en del av uppgiften,
inte ett tecken på att du gör fel.

## Mål

När veckan är klar kan du:

- köra Python-program och använda Python-skalet för att prova saker
- läsa ett felmeddelande och hitta felet utan hjälp
- använda variabler, de grundläggande typerna och omvandla mellan dem
- räkna med `+ - * / // % **` och förutsäga resultatet, även för
  negativa tal och decimaltal
- plocka ut, skära ut och formatera text
- skriva funktioner som tar emot värden och returnerar ett svar
- skriva tester som hittar fel

## Så arbetar du

Varje steg nedan slutar med en eller flera övningar. Varje övning är en
fil i `ovningar/` med en specifikation: vad som ska läsas in, vad som ska
skrivas ut eller returneras, och ibland en regel, till exempel att print
bara får anropas en gång.

Kontrollera en övning med:

```
python -m pytest kontroll -k 04
```

Kontrollerna provar **fler fall än exemplen** i uppgiften. Ett program
som bara klarar exemplet blir underkänt, och meddelandet talar om vilket
fall som gick fel.

Facit finns i `facit/` och förklaras i [`FACIT.md`](FACIT.md). Läs det
när din lösning fungerar, för att jämföra, eller när du verkligen har
kört fast.

## Genomgång

### Steg 0: Förbered datorn

1. Installera Python 3.10 eller nyare från
   <https://www.python.org/downloads/>. På Windows: kryssa i
   **"Add python.exe to PATH"**.
2. Installera [VS Code](https://code.visualstudio.com/) och tillägget
   "Python".
3. Öppna den här mappen i VS Code (*File > Open Folder…*) och en
   terminal (*Terminal > New Terminal*).
4. Kör `python --version` och sedan `python -m pip install pytest`.

På Mac och Linux heter kommandot ofta `python3`, och på Windows ibland
`py`.

### Steg 1: Program och print

Ett program är en textfil med instruktioner som körs uppifrån och ned.
Kör en fil med `python filnamn.py`.

```python
# En kommentar: allt efter # ignoreras av Python.
print("Hej!")
print("Temperatur:", -3, "grader")   # flera värden, med mellanslag emellan
```

Text (en **sträng**) skrivs inom `"..."` eller `'...'`. Inne i en sträng
inleder ett bakstreck `\` en **escape-sekvens**, ett sätt att skriva
tecken som annars är svåra att skriva: `\n` är en radbrytning och `\"` ett
citattecken som inte avslutar strängen.

Skriver du bara `python` i terminalen startar **Python-skalet**, där varje
rad körs direkt. Använd det för att prova saker. Avsluta med `exit()`.

**Öva:** 1.1.

### Steg 2: Felmeddelanden

```
Traceback (most recent call last):
  File "program.py", line 3, in <module>
    print(pris + " kr")
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

Läs nerifrån och upp: sista raden säger vilken sorts fel det är och vad
som hände, raden ovanför visar koden, och `line 3` var den står.

| Fel | Betyder |
|---|---|
| `SyntaxError` | Koden är felskriven och går inte att tolka. |
| `NameError` | Ett namn som inte finns. |
| `TypeError` | En operation som inte fungerar för de här typerna. |
| `ValueError` | Rätt typ, men ett värde som inte går att använda. |
| `IndentationError` | Fel indrag. |

Ett `SyntaxError` upptäcks innan programmet börjar köras. Alla andra fel
upptäcks först när raden körs.

**Öva:** 1.2.

### Steg 3: Variabler och typer

```python
stad = "Kiruna"
temperatur = -3
temperatur = temperatur + 1    # räkna ut höger sida, spara under namnet till vänster
```

`=` betyder "spara värdet till höger under namnet till vänster". Namn
skrivs med små bokstäver och understreck (`antal_personer`) och får inte
börja med en siffra.

| Typ | Exempel |
|---|---|
| `int`, heltal | `42`, `-3` |
| `float`, decimaltal | `3.14`, `20.0` |
| `str`, text | `"Kiruna"`, `"42"` |
| `bool`, sant eller falskt | `True`, `False` |
| `NoneType`, inget värde | `None` |

`type(x)` talar om vilken typ `x` har. `int()`, `float()`, `str()` och
`bool()` gör om ett värde till en annan typ, när det går.

**Öva:** 1.3.

### Steg 4: Läsa in och räkna

`input("Fråga: ")` visar frågan och returnerar det användaren skriver,
**alltid som text**. Vill du räkna med svaret måste du göra om det.

| Operator | Betyder |
|---|---|
| `+ - *` | plus, minus, gånger |
| `/` | division, ger alltid ett decimaltal |
| `//` | heltalsdivision: hur många hela gånger |
| `%` | rest (modulo) |
| `**` | upphöjt till |

Prioriteten är som i matematiken, och parenteser bestämmer ordningen. Två
saker att veta om decimaltal: de lagras binärt och är därför inte alltid
exakta, och `round(x, 2)` avrundar till två decimaler.

Inbyggda funktioner som ofta behövs: `abs`, `min`, `max`, `round`. Fler
matematiska funktioner finns i modulen `math`, som du hämtar med
`import math` överst i filen. Se dess dokumentation:
<https://docs.python.org/3/library/math.html>.

**Öva:** 1.4 och 1.5.

### Steg 5: Text

```python
stad = "Göteborg"
stad[0]      # "G", första tecknet (index 0)
stad[-1]     # "g", sista tecknet
stad[2:5]    # "teb", tecken 2, 3 och 4 (slutet räknas inte med)
stad[:3]     # "Göt"
len(stad)    # 8
"ab" + "cd"  # "abcd"
"ab" * 3     # "ababab"
```

**Metoder** är funktioner som hör till ett värde och anropas med punkt.
De ändrar aldrig strängen, utan returnerar en ny:

| Metod | Gör |
|---|---|
| `s.upper()`, `s.lower()` | stora eller små bokstäver |
| `s.strip()` | tar bort mellanslag i början och slutet |
| `s.replace(a, b)` | byter ut varje `a` mot `b` |
| `s.find(a)` | index där `a` först förekommer, eller `-1` |
| `s.count(a)` | hur många gånger `a` förekommer |

En **f-sträng** sätter in värden i text: `f"{stad}: {temperatur} grader"`.
Efter ett kolon styr en **formatspecifikation** hur värdet visas, till
exempel `{pris:.2f}` (två decimaler), `{minut:02d}` (minst två siffror,
nollor framför) och `{namn:>10}` (högerställt i tio tecken). Det finns
många fler möjligheter; se "Format Specification Mini-Language" i
dokumentationen:
<https://docs.python.org/3/library/string.html#formatspec>.

**Öva:** 1.6, 1.7, 1.8 och 1.9.

### Steg 6: Funktioner

```python
def area(width, height):
    return width * height

print(area(3, 4))    # 12
```

- `def` definierar funktionen. Inom parentes står **parametrarna**.
- Koden i funktionen är **indragen** fyra mellanslag.
- `return` lämnar tillbaka ett värde och avslutar funktionen. En funktion
  utan `return` returnerar `None`.
- `area(3, 4)` **anropar** funktionen med **argumenten** 3 och 4.

`return` och `print` är olika saker: `print` visar något på skärmen,
`return` ger ett värde till den som anropade. En funktion som räknar ut
något ska returnera svaret, så att det kan användas vidare och testas.
Funktioner kan anropa andra funktioner, och det är ofta så man delar upp
ett problem.

Kursen använder engelska namn på funktioner och parametrar, som nästan
all kod i världen gör. [`ORDLISTA.md`](../../ORDLISTA.md) förklarar
begreppen och låter dig öva på dem.

**Öva:** 1.10, 1.11 och 1.12.

### Steg 7: Tester

```python
def test_area():
    assert area(3, 4) == 12
    assert area(0, 5) == 0
```

`assert` kontrollerar att något är sant; är det falskt misslyckas testet.
`pytest` hittar alla funktioner som börjar med `test_` och kör dem. Kör
veckans tester med `python -m pytest`. Decimaltal jämförs med
`pytest.approx(0.3)` i stället för `==`.

Ett test är bara så bra som fallen det provar. Ett test som bara provar
ett vanligt fall missar de flesta fel.

**Öva:** 1.13.

## Veckans projekt: Enhetsomvandlaren

```
Week-01-unit-converter-toolkit/
├── starta.py                     - startar programmet: python starta.py
├── src/converter_toolkit/
│   ├── converters.py             - funktionerna som räknar
│   └── cli.py                    - programmet som frågar och skriver ut
├── tests/                        - tester för projektet och för facit
├── ovningar/                     - dina övningar
├── kontroll/                     - kontrollerna av övningarna
├── facit/                        - lösningar
└── FACIT.md                      - förklaringar till lösningarna
```

`converters.py` innehåller bara funktioner som tar emot tal och
returnerar svar, utan `input` och `print`. `cli.py` pratar med användaren
och låter funktionerna räkna. Uppdelningen gör att funktionerna kan testas
automatiskt. Läs båda filerna och testerna i `tests/test_converters.py`,
och förstå varje rad.

## Köra programmet

```
python starta.py
```

## Testa

```
python -m pytest                   # testerna för veckans projekt
python -m pytest kontroll          # kontrollerna av dina övningar
python -m pytest kontroll --facit  # facit mot samma kontroller
```

## Prova själv

Bygg ut projektet. Lägg funktionerna i `converters.py`, ändringarna av
programmet i `cli.py`, och tester för allt i `tests/test_converters.py`.

1. `celsius_to_kelvin(celsius)` och `kelvin_to_celsius(kelvin)`. 0 °C är
   273,15 K.
2. `hms_to_seconds(text)`, som gör om en text som `"1:01:05"` till antal
   sekunder. Timmarna kan ha hur många siffror som helst. Skriv ett test
   som visar att `hms_to_seconds(seconds_to_hms(n))` blir `n` för en rad
   olika värden på `n`.
3. `pace(km, minutes)`, löptakt i minuter per kilometer, avrundat till
   hela sekunder: 10 km på 55 minuter ger `"5:30 min/km"`. Svaret får
   aldrig innehålla `:60`.
4. `mph_to_kmh(mph)` och `kmh_to_mph(kmh)`, och en sista fråga i
   programmet: en hastighet i km/h som skrivs ut i mph med en decimal.
   Talet 1.609344 får bara stå på ett ställe i koden.
5. Ett test som visar att `0.1 + 0.2` inte är exakt `0.3` i Python, och
   ett test som jämför dem på ett sätt som fungerar. Förklara varför i en
   kommentar.

## Facit

Lösningar till övning 1.1–1.13 finns i `facit/`, och till "Prova själv" i
`facit/prova_sjalv.py`. Allt förklaras i [`FACIT.md`](FACIT.md).
