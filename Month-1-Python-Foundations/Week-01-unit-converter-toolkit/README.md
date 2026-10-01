# Vecka 1 — Python från noll: ditt första program

## Syfte

Den här veckan förutsätter att du aldrig har programmerat. Du installerar
det du behöver, skriver och kör dina första program, och lär dig de
byggstenar som allt annat i kursen vilar på: att skriva ut text, spara
värden i variabler, räkna, fråga användaren om något, och samla kod i
funktioner. Du lär dig också läsa felmeddelanden, för de kommer du att se
ofta, och det är helt normalt. I slutet av veckan läser du ett riktigt
litet program, en enhetsomvandlare, och förstår varje rad i det.

## Mål

När veckan är klar kan du:

- installera Python, öppna en terminal och köra ett Python-program
- skriva ut text med `print` och läsa ett felmeddelande
- skapa variabler och räkna med `+ - * / // % **`
- skilja på heltal (`int`), decimaltal (`float`) och text (`str`)
- bygga text med f-strängar och styra antalet decimaler
- fråga användaren om något med `input` och göra om svaret till ett tal
- skriva egna funktioner med `def` och `return`
- köra automatiska tester med pytest och läsa vad de säger

## Genomgång

Läs ett steg i taget. Efter varje steg finns övningar i mappen
`ovningar/`. Gör dem innan du går vidare: det är genom att skriva kod
själv som du lär dig, inte genom att läsa.

### Steg 0: Förbered datorn

Det här steget gör du bara en gång.

**1. Installera Python.** Gå till <https://www.python.org/downloads/> och
ladda ner den senaste versionen (3.10 eller nyare).

- *Windows:* kryssa i rutan **"Add python.exe to PATH"** längst ner i
  installationsfönstret innan du klickar Install. Glömmer du den hittar
  terminalen inte Python.
- *Mac:* kör installationsfilen som vanligt.

**2. Installera en editor**, ett program för att skriva kod. Vi
rekommenderar [Visual Studio Code](https://code.visualstudio.com/)
(gratis). Installera tillägget "Python" i den (klicka på ikonen med fyra
rutor till vänster och sök på Python).

**3. Ladda ner kursen.** På kursens sida på GitHub: klicka den gröna
knappen **Code** och sedan **Download ZIP**. Packa upp zip-filen någonstans
där du hittar den, till exempel i Dokument. (Kan du redan Git kan du klona
repot i stället; Git lär du dig i vecka 16.)

**4. Öppna veckans mapp i VS Code.** *File > Open Folder…* och välj mappen
`Month-1-Python-Foundations/Week-01-unit-converter-toolkit`.

**5. Öppna en terminal.** I VS Code: *Terminal > New Terminal*. En
terminal är ett fönster där du skriver kommandon till datorn i stället för
att klicka. Den öppnas redan "i" veckans mapp. Skriv:

```
python --version
```

och tryck Enter. Du ska se något i stil med `Python 3.12.4`.

> **Mac och Linux:** där heter kommandot ofta `python3`. Får du "command
> not found", skriv `python3` överallt där kursen skriver `python`.
> **Windows:** fungerar inte `python`, prova `py`.

**6. Installera pytest**, verktyget som kontrollerar dina övningar:

```
python -m pip install pytest
```

### Steg 1: Ditt första program

Ett program är en textfil med instruktioner som datorn utför uppifrån och
ner, en rad i taget. Python-filer slutar på `.py`. Här är ett helt program:

```python
print("Hej!")
print("Det här är mitt första program.")
```

`print(...)` betyder "skriv ut det här". Texten står inom citattecken så
att Python förstår att det är text och inte kod.

Öppna `ovningar/01_hej_varlden.py`. Överst står uppgiften som
**kommentarer**: rader som börjar med `#`. Python hoppar över allt efter
`#`, så där kan du skriva anteckningar till dig själv och andra. Skriv din
kod under kommentarerna, spara filen (Ctrl+S, på Mac Cmd+S) och kör den i
terminalen:

```
python ovningar/01_hej_varlden.py
```

**Kontrollera din lösning.** Varje övning har en automatisk kontroll:

```
python -m pytest kontroll -k 01
```

`-k 01` betyder "bara övning 01". Står det `passed` i grönt är du klar.
Står det `failed` i rött, läs raden som börjar med `AssertionError`: där
står vad som var fel. Rätta och kör igen. Utan `-k` kontrolleras alla
övningar på en gång.

> **Python-skalet.** Skriver du bara `python` i terminalen startar ett
> interaktivt läge med prompten `>>>`. Där körs varje rad direkt, vilket
> är praktiskt för att prova saker: skriv `2 + 2` och tryck Enter. Avsluta
> med `exit()`.

**Öva:** övning 1.1 och 1.2.

### Steg 2: När något går fel

Alla som programmerar skriver fel hela tiden. Det viktiga är att kunna
läsa vad Python säger. Prova att köra ett program med ett stavfel:

```python
prnt("Hej")
```

Python svarar ungefär:

```
Traceback (most recent call last):
  File "test.py", line 1, in <module>
    prnt("Hej")
NameError: name 'prnt' is not defined
```

Läs felmeddelanden **nerifrån och upp**:

- **Sista raden** säger vilken sorts fel det är (`NameError`) och vad som
  hände: Python känner inte till något som heter `prnt`.
- **Raden ovanför** visar koden som orsakade felet.
- **`line 1`** säger på vilken rad i filen felet sitter.

Några fel du kommer att se ofta:

| Fel | Betyder ungefär |
|---|---|
| `SyntaxError` | Koden är felskriven: ett citattecken eller en parentes saknas, eller liknande. |
| `NameError` | Du använder ett namn som inte finns. Ofta ett stavfel. |
| `TypeError` | Du blandar typer som inte går ihop, som text plus tal. |
| `ValueError` | Värdet har rätt typ men går inte att använda, som `int("hej")`. |
| `IndentationError` | Fel indrag (mellanslag i början av en rad). Se steg 8. |

**Öva:** övning 1.3.

### Steg 3: Variabler

En **variabel** är ett namn som pekar på ett värde, ungefär som en etikett
på en låda. Du skapar den med `=`:

```python
stad = "Kiruna"
temperatur = -3
print(stad)          # skriver ut: Kiruna
print(temperatur)    # skriver ut: -3
```

`=` betyder här **"spara värdet till höger under namnet till vänster"**,
inte "är lika med" som i matematik. Därför kan en variabel få ett nytt
värde:

```python
poang = 10
poang = poang + 5    # räkna ut 10 + 5 och spara resultatet i poang igen
print(poang)         # 15
```

Regler och vanor för namn:

- Namn får innehålla bokstäver, siffror och understreck, men inte börja med
  en siffra. `antal_1` går bra, `1_antal` gör det inte.
- Stora och små bokstäver räknas som olika: `Pris` och `pris` är två olika
  variabler.
- I Python skriver man namn med små bokstäver och understreck mellan
  orden: `antal_personer`. Det kallas *snake_case*.
- Undvik å, ä och ö i namn. Det fungerar, men nästan all kod i världen
  använder bara a–z, så det är en bra vana från början.

`print` kan skriva ut flera saker på en rad. Separera dem med kommatecken,
så sätter Python ett mellanslag mellan dem:

```python
print("I", stad, "är det", temperatur, "grader.")
# I Kiruna är det -3 grader.
```

**Öva:** övning 1.4.

### Steg 4: Datatyper

Varje värde har en **typ**. De fyra vanligaste:

| Typ | Namn | Exempel |
|---|---|---|
| `int` | heltal (integer) | `42`, `-3`, `0` |
| `float` | decimaltal (floating point) | `3.14`, `-0.5`, `20.0` |
| `str` | text (string, sträng) | `"Kiruna"`, `'hej'`, `"42"` |
| `bool` | sant eller falskt (boolean) | `True`, `False` |

Observera att Python använder **punkt** som decimaltecken: `3.14`, inte
`3,14`. Och att `"42"` med citattecken är text, inte ett tal.

Du kan fråga Python vilken typ ett värde har:

```python
print(type(42))      # <class 'int'>
print(type("42"))    # <class 'str'>
```

Typen avgör vad som händer. `+` betyder addition för tal men "sätt ihop"
för text:

```python
print(10 + 5)        # 15
print("10" + "5")    # 105
```

Du gör om mellan typer med typens namn: `int("10")` ger talet `10`,
`float("2.5")` ger `2.5` och `str(42)` ger texten `"42"`.

**Öva:** övning 1.7.

### Steg 5: Räkna

| Tecken | Betyder | Exempel | Svar |
|---|---|---|---|
| `+` | plus | `7 + 2` | `9` |
| `-` | minus | `7 - 2` | `5` |
| `*` | gånger | `7 * 2` | `14` |
| `/` | delat med | `7 / 2` | `3.5` |
| `//` | heltalsdivision: hur många hela gånger | `7 // 2` | `3` |
| `%` | rest (modulo): vad som blir över | `7 % 2` | `1` |
| `**` | upphöjt till | `7 ** 2` | `49` |

Python räknar i samma ordning som i matematiken: `**` först, sedan
`* / // %`, sist `+ -`. Använd parenteser när du vill bestämma ordningen,
eller när det gör koden tydligare: `(32 - 4) * 2`.

`//` och `%` är mer användbara än de ser ut. 200 minuter är `200 // 60 =
3` hela timmar och `200 % 60 = 20` minuter till.

`/` ger alltid ett decimaltal, även när det går jämnt ut: `10 / 2` är
`5.0`. Och decimaltal i datorer är inte alltid exakta: `0.1 + 0.2` blir
`0.30000000000000004`. Det beror på att datorn lagrar tal binärt, och
precis som 1/3 inte går att skriva exakt med decimaler går 0.1 inte att
skriva exakt binärt. Avrunda när du visar svaret, med `round(tal, 2)`
eller formatering (steg 6).

**Öva:** övning 1.5 och 1.6.

### Steg 6: Text

Text (strängar) skrivs inom `"..."` eller `'...'`. Några saker man kan göra
med dem:

```python
namn = "Alva"
print("Hej " + namn)     # sätt ihop: Hej Alva
print("ha" * 3)          # upprepa: hahaha
print(len(namn))         # antal tecken: 4
```

Det smidigaste sättet att bygga text av variabler är en **f-sträng**:
skriv ett `f` före citattecknet, och sätt variabler eller uträkningar inom
`{ }`:

```python
alder = 31
print(f"{namn} är {alder} år och fyller {alder + 1} nästa år.")
# Alva är 31 år och fyller 32 nästa år.
```

Efter ett kolon inne i `{ }` kan du styra hur talet visas:

```python
pris = 149.7000000001
print(f"{pris:.2f} kr")   # 149.70 kr   (.2f = två decimaler)
minut = 5
print(f"{minut:02d}")     # 05          (02d = minst två siffror, nollor framför)
```

**Öva:** övning 1.8 och 1.9.

### Steg 7: Fråga användaren

`input()` visar en fråga, väntar tills användaren skrivit något och tryckt
Enter, och ger tillbaka det som skrevs:

```python
namn = input("Vad heter du? ")
print(f"Hej, {namn}!")
```

Det `input()` ger tillbaka är **alltid text**, även om man skriver en
siffra. Vill du räkna med svaret måste du göra om det:

```python
tal = int(input("Skriv ett heltal: "))         # heltal
temperatur = float(input("Temperatur: "))      # decimaltal
```

Skriver användaren något som inte är ett tal, till exempel `tjugo`, blir
det ett `ValueError` och programmet stannar. I vecka 2 lär du dig fånga
sådana fel och be användaren försöka igen.

**Öva:** övning 1.10, 1.11 och 1.12.

### Steg 8: Funktioner

En **funktion** är en namngiven bit kod som du kan använda många gånger.
Du har redan använt Pythons inbyggda funktioner: `print`, `input`, `len`,
`int`, `round`. Nu skriver du egna:

```python
def double(number):
    return number * 2

print(double(4))     # 8
print(double(10))    # 20
```

Delarna:

- `def` betyder "här definieras en funktion". Sedan kommer namnet,
  `double`, och inom parentes **parametrarna**: namnen på det funktionen får
  in. Raden slutar med kolon.
- Raderna som hör till funktionen är **indragna** med fyra mellanslag.
  Indraget är inte bara snyggt: det är så Python vet var funktionen slutar.
  VS Code gör indraget åt dig när du trycker Enter efter kolonet.
- `return` lämnar tillbaka svaret till den som **anropade** funktionen,
  och avslutar funktionen.
- `double(4)` **anropar** funktionen: Python kör koden i den med `number =
  4`, och hela uttrycket `double(4)` får värdet som returneras.

**`return` eller `print`?** Det här är den vanligaste förväxlingen i
början. `print` visar något på skärmen, men lämnar inget svar tillbaka.
`return` lämnar tillbaka ett svar, som programmet kan spara, räkna vidare
med eller skriva ut:

```python
def greeting(name):
    return f"Hej, {name}!"

text = greeting("Bo")    # text är nu "Hej, Bo!"
print(text)              # och först nu skrivs något ut
```

En funktion som räknar ut något ska nästan alltid **returnera** svaret och
låta någon annan bestämma om det ska skrivas ut. Då kan den användas i
fler sammanhang, och den går att testa automatiskt (steg 9).

En funktion kan ha flera parametrar och egna variabler inuti:

```python
def minutes_to_text(total_minutes):
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours} h {minutes} min"
```

Funktionsnamn skrivs med små bokstäver och understreck, precis som
variabler. Övningarna och veckans projekt använder engelska namn, eftersom
nästan all kod i världen gör det. Ordlistan,
[`ORDLISTA.md`](../../ORDLISTA.md) i kursens huvudmapp, förklarar orden
och låter dig öva på dem.

I vecka 3 lär du dig mycket mer om funktioner.

**Öva:** övning 1.13 till 1.18.

### Steg 9: Tester

Ett **test** är en liten bit kod som kontrollerar att annan kod gör rätt.
Så här ser ett test för `double` ut:

```python
def test_double():
    assert double(4) == 8
```

`==` betyder "är lika med" (till skillnad från `=`, som sparar ett värde).
`assert` betyder "jag påstår att det här är sant". Är det sant händer
ingenting; är det falskt misslyckas testet och pytest talar om var.

Programmet **pytest** letar upp alla funktioner som börjar med `test_` och
kör dem. Det är så kontrollerna av dina övningar fungerar: de anropar dina
funktioner med tal där svaret är känt och jämför.

Varje vecka har också tester för veckans projekt, i mappen `tests/`. Kör
dem med:

```
python -m pytest
```

En sak till: eftersom decimaltal inte alltid är exakta (steg 5) jämförs
de i testerna med `pytest.approx`, som godtar en mycket liten skillnad:

```python
assert celsius_to_fahrenheit(100) == pytest.approx(212.0)
```

## Veckans projekt: Enhetsomvandlaren

Nu kan du läsa ett helt litet program. Enhetsomvandlaren räknar om
temperaturer, sträckor och tider.

```
Week-01-unit-converter-toolkit/
├── starta.py                     - startar programmet: python starta.py
├── src/
│   └── converter_toolkit/
│       ├── converters.py         - funktionerna som räknar (testas automatiskt)
│       └── cli.py                - programmet som frågar och skriver ut
├── tests/
│   ├── test_converters.py        - tester för converters.py
│   └── test_facit_prova_sjalv.py - tester för facit till "Prova själv"
├── ovningar/                     - veckans övningar: här skriver du din kod
├── kontroll/                     - kontrollerna av övningarna
├── facit/                        - lösningar till alla övningar
└── FACIT.md                      - förklarade lösningar till "Prova själv"
```

Programmet är delat i två filer, och den uppdelningen är det viktigaste
att lägga märke till:

- **`converters.py`** innehåller bara funktioner som tar emot ett tal och
  returnerar ett svar. Ingen av dem använder `input` eller `print`. Därför
  kan testerna anropa dem direkt och kontrollera svaren, utan att någon
  behöver sitta och skriva in tal.
- **`cli.py`** (CLI betyder *command-line interface*, ett program man
  använder i terminalen) pratar med användaren: frågar med `input`, låter
  funktionerna räkna och skriver ut med `print`.

Läs `converters.py` först. Lägg märke till:

- **Konstanten** `KM_PER_MILE = 1.609344` högst upp. Stora bokstäver
  betyder "det här värdet ändras aldrig". Talet står på ett enda ställe och
  har ett namn som förklarar det.
- **Dokumentationstexten** (*docstring*) inom `"""` först i varje funktion.
  Den förklarar vad funktionen gör, och visas om man skriver
  `help(celsius_to_fahrenheit)` i Python-skalet.
- **`seconds_to_hms`** använder `//`, `%` och formateringen `:02d` från
  steg 5 och 6 för att göra `3665` till `"1:01:05"`.

Läs sedan `cli.py`. Två saker är nya:

- `from converter_toolkit.converters import ...` **importerar** funktioner
  från en annan fil, så att de kan användas här.
- `if __name__ == "__main__":` längst ner betyder "kör `main()` bara om
  den här filen startas som ett program". Om filen i stället importeras av
  en annan fil, som testerna gör, körs ingenting automatiskt.

## Köra programmet

Stå i veckans mapp i terminalen och skriv:

```
python starta.py
```

Svara på frågorna. Prova också att skriva `tjugo` när programmet frågar
efter en temperatur, och läs felmeddelandet: det är ett `ValueError` från
`float()`, precis som i steg 7.

## Testa

```
python -m pytest                   # testerna för veckans projekt
python -m pytest kontroll          # kontrollerna av dina övningar
python -m pytest kontroll --facit  # visar att facit klarar alla kontroller
```

`tests/test_converters.py` provar varje omvandling med värden där svaret
är känt: fryspunkt och kokpunkt, -40 (samma i Celsius och Fahrenheit), en
mil fram och tillbaka, och tider från 0 sekunder till mer än ett dygn.
`kontroll/test_ovningar.py` innehåller kontrollerna för övning 1.1–1.18.

## Prova själv

De här uppgifterna är lite större och handlar om veckans projekt. Skriv
nya funktioner i `converters.py` och nya tester i `tests/test_converters.py`.

1. Lägg till `celsius_to_kelvin(celsius)` och `kelvin_to_celsius(kelvin)`.
   0 °C är 273.15 K, och skalorna har lika stora steg. Skriv tester, till
   exempel att 0 K är -273.15 °C.
2. Lägg till `hms_to_seconds(hours, minutes, seconds)`, som gör tvärtom
   mot `seconds_to_hms`. Skriv ett test som räknar fram och tillbaka.
3. Lägg till `mph_to_kmh(mph)` och `kmh_to_mph(kmh)` för hastigheter.
   Återanvänd `miles_to_km` och `km_to_miles` i stället för att skriva in
   1.609344 igen.
4. Utöka `main()` i `cli.py` så att programmet till sist frågar efter en
   hastighet i km/h och skriver ut den i mph med en decimal.
5. Skriv ett test som visar att `0.1 + 0.2` inte är exakt `0.3` i Python,
   och ett som visar att `pytest.approx` klarar jämförelsen. Förklara i en
   kommentar varför.

## Facit

- Lösningar till övning 1.1–1.18 finns i mappen `facit/`, med samma
  filnamn som i `ovningar/`. Där det behövs står en förklaring överst.
- Lösningar till "Prova själv" finns i `facit/prova_sjalv.py`, med
  förklaringar i [`FACIT.md`](FACIT.md).

Titta i facit **efter** att du försökt själv. Har du kört fast länge, titta
på en enda övning, stäng facit och skriv lösningen själv från början.
