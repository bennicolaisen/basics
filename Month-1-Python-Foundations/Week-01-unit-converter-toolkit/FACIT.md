# Facit vecka 1

Lösningarna finns i [`facit/`](facit/), med samma filnamn som i
`ovningar/`. Här förklaras hur man tänker och var fällorna ligger. Läs en
övning i taget, helst först när din egen lösning fungerar.

## 1.1 Citat

```python
print("Hon sa: \"Det går inte att skriva så här.\"\nHan svarade: 'Prova C:\\kurs\\nytt' i stället.")
```

Tre saker ska in i en enda sträng:

- **Radbrytningen** mellan raderna skrivs `\n`.
- **Dubbla citattecken** i en sträng som avgränsas av dubbla citattecken
  skrivs `\"`. De enkla behöver ingen escape här.
- **Bakstrecken** är fällan. I `C:\kurs\nytt` står `\n`, som Python läser
  som en radbrytning. Ett bakstreck som ska synas skrivs `\\`.

Alternativet är en *rå sträng*, `r"..."`, där bakstreck inte tolkas. Men
då fungerar inte heller `\n` som radbrytning, så den passar inte när båda
behövs i samma sträng.

## 1.2 Tre fel

Python visar felen i den här ordningen:

1. **`SyntaxError: '(' was never closed`** på raden med `"Totalt: "`.
   Koden går inte att tolka, så ingenting körs.
2. **`TypeError: can only concatenate str (not "int") to str`** på samma
   rad. `+` mellan text och tal fungerar inte. Gör om talet till text med
   `str(summa)`, eller skriv raden som en f-sträng.
3. **`NameError: name 'sumna' is not defined`** på sista raden. Ett
   stavfel.

Syntaxfelet kommer först fast det står på samma rad som typfelet,
eftersom Python läser in hela filen innan något körs. Typfel och namnfel
upptäcks först när raden körs, och därför ett i taget, uppifrån.

Att skriva in `147` och `132.30` i utskriften ger rätt svar för pris 49
och antal 3, men kontrollen kör programmet med andra värden. Utskriften
måste räknas fram.

## 1.3 Byt plats

```python
tillfallig = a
a = b
b = tillfallig
```

`a = b` skriver över `a`. Utan en tredje variabel är `a`:s gamla värde
borta innan det hunnit sparas i `b`. Python har också ett kortare sätt,
`a, b = b, a`, som räknar ut båda värdena till höger innan något sparas.

Kontrollen provar med text, `True` och `None` för att en lösning som
räknar (`a = a + b`, `b = a - b`, `a = a - b`) bara fungerar för tal. Att
byta plats ska fungera för vilka värden som helst.

## 1.4 Sekunder

```python
dygn = sekunder // 86400
timmar = sekunder % 86400 // 3600
minuter = sekunder % 3600 // 60
rest = sekunder % 60
```

Varje enhet räknas på samma sätt: **ta bort det som ryms i större enheter
med `%`, och se hur många hela gånger enheten går i resten med `//`.** Ett
dygn är 24 · 3600 = 86 400 sekunder.

Den vanliga missen är timmarna: `sekunder // 3600` ger *totala* antalet
timmar, 27 för 100 000 sekunder, inte 3. Först `% 86400` tar bort de hela
dygnen. Minuterna klarar sig med `% 3600`, eftersom ett dygn är ett jämnt
antal timmar.

## 1.5 Siffror

```python
tusental = tal // 1000
hundratal = tal // 100 % 10
tiotal = tal // 10 % 10
ental = tal % 10
```

`% 10` ger sista siffran. `// 10` tar bort sista siffran. Tillsammans
plockar de ut vilken siffra som helst: `tal // 100 % 10` tar bort de två
sista och tar sedan den sista av det som är kvar.

Baklänges bygger man ett nytt tal, `ental * 1000 + tiotal * 100 + ...`,
och skriver ut det med `:04d` så att 21 visas som `0021`. Nollorna i
början finns aldrig i talet, bara i hur det visas.

Varför regeln? Med text blir det `input()[::-1]`, en rad. Övningen
handlar om `//` och `%`, som behövs när data är tal: datum, tider,
kontonummer, kontrollsiffror.

## 1.6 Svenskt belopp

```python
text = f"{belopp:,.2f}"                          # "1,234,567.89"
text = text.replace(",", " ").replace(".", ",")  # "1 234 567,89"
```

Formatspecifikationen `,.2f` ger tusentalsavgränsare och två decimaler i
engelsk stil. Sedan byts tecknen.

**Ordningen avgör.** Byter du punkten mot komma först får du
`"1,234,567,89"`, och nästa byte gör om *alla* kommatecken till
mellanslag: `"1 234 567 89"`. Byt kommatecknen först, medan punkten
fortfarande är den enda punkten.

Formateringen avrundar innan den grupperar, så 999.999 blir `1 000,00`.
Det är ett skäl att låta formatspecifikationen göra båda delarna i
stället för att bygga grupperna själv.

## 1.7 Ruta

```python
kant = "+" + "-" * (bredd - 2) + "+\n"
mitt = "|" + " " * (bredd - 2) + "|\n"
print(kant + mitt * (hojd - 2) + kant, end="")
```

Rutan byggs som en enda sträng. Varje rad slutar med `\n`, så att
`mitt * (hojd - 2)` ger rätt antal rader under varandra. `end=""` hindrar
`print` från att lägga till en extra radbrytning sist.

Höjden 2 ger `mitt * 0`, en tom sträng, och rutan blir bara två kanter.
Det fungerar utan specialfall. Bredden *minus två* beror på att hörnen
tar två av tecknen.

## 1.8 Namn

```python
namn = input("Namn: ").strip()
mellanslag = namn.find(" ")
fornamn = namn[:mellanslag]
efternamn = namn[mellanslag + 1:]
fornamn = fornamn[0].upper() + fornamn[1:].lower()
```

`strip()` först, annars hittar `find` ett mellanslag *före* namnet.
Mellanslagets index delar sedan namnet i två: allt före, och allt efter.

`.title()` och `.capitalize()` finns också, men `title()` gör
`"jean-luc"` till `"Jean-Luc"`, medan uppgiften säger stor första bokstav
och resten små. Att bygga det själv med index och slicing gör exakt det
som står.

Å, Ä och Ö fungerar utan extra arbete: `"å".upper()` är `"Å"`.

## 1.9 Förutsäg

| Uttryck | Svar | Varför |
|---|---|---|
| `7 / 7` | `1.0` | `/` ger alltid ett decimaltal. |
| `7 // 2.0` | `3.0` | Heltalsdivision, men med ett decimaltal blir svaret ett decimaltal. |
| `-7 // 2` | `-4` | `//` avrundar **nedåt**, mot minus oändligheten, inte mot noll. -3,5 blir -4. |
| `-7 % 2` | `1` | Resten hör ihop med `//`: `-7 == 2 * (-4) + 1`. |
| `round(2.5)` | `2` | Python avrundar halvor till närmaste **jämna** tal. |
| `round(3.5)` | `4` | Samma regel: 4 är jämnt. |
| `int(-3.99)` | `-3` | `int` kapar decimalerna, mot noll. Inte samma sak som `//`. |
| `"3" * 3` | `"333"` | Text gånger heltal upprepar texten. |
| `int("3.5")` | `"ValueError"` | `int` läser bara heltal från text. `int(float("3.5"))` fungerar. |
| `0.1 + 0.2 == 0.3` | `False` | Summan blir `0.30000000000000004`. |
| `True + True + True` | `3` | `bool` räknas som heltal: `True` är 1, `False` är 0. |
| `2 ** 3 ** 2` | `512` | `**` räknas från höger: `2 ** 9`. |
| `"10" < "9"` | `True` | Text jämförs tecken för tecken, och `"1"` kommer före `"9"`. |
| `len("Malmö\n")` | `6` | `\n` är ett tecken, och `ö` är ett tecken. |
| `"Malmö"[-1]` | `"ö"` | Negativt index räknar bakifrån. |
| `"Malmö"[1:4]` | `"alm"` | Index 1, 2 och 3. Slutet räknas inte med. |

Fyra av dem kommer tillbaka i veckans andra övningar: avrundningen av
halvor i 1.10 och 1.13, `%` med negativa tal i 1.11, och decimaltalens fel
i 1.12.

## 1.10 Avrunda till närmaste steg

```python
def round_to_nearest(value, step):
    return (2 * value + step) // (2 * step) * step
```

Det naturliga försöket är `round(value / step) * step`. Det ger fel för
`round_to_nearest(25, 10)`: `round(2.5)` är 2 (se 1.9), så svaret blir 20
i stället för 30.

Lösningen undviker `round` och decimaltal helt. Att avrunda med halvor
uppåt är detsamma som att lägga till en halv och sedan avrunda nedåt:
`value / step + 1/2`, nedåt. Förläng med två för att slippa halvan:
`(2 * value + step) // (2 * step)`. Allt är heltal, så svaret är exakt och
ett heltal.

## 1.11 Klockslag

```python
def to_minutes(clock):
    return int(clock[:2]) * 60 + int(clock[3:])


def minutes_between(start, end):
    return (to_minutes(end) - to_minutes(start)) % (24 * 60)
```

Två idéer:

- **Gör om till ett tal först.** Klockslag är svåra att räkna med; minuter
  sedan midnatt är lätta. Hjälpfunktionen `to_minutes` används två gånger
  i stället för att samma uträkning skrivs två gånger.
- **`%` sköter dygnsskiftet.** Från 22:30 till 01:15 blir skillnaden
  75 − 1350 = −1275, och `-1275 % 1440` är 165. Modulo 1440 ger alltid ett
  svar från 0 till 1439, även för negativa tal (se `-7 % 2` i 1.9). Inget
  `if` behövs.

## 1.12 Dela notan

```python
def split_bill(total, people, tip_percent):
    total_ore = round(total * 100)
    with_tip = total_ore * (100 + tip_percent)
    return math.ceil(with_tip / (100 * 100 * people))
```

Det naturliga försöket är
`math.ceil(total * (1 + tip_percent / 100) / people)`. Det ger 56 för
`split_bill(50, 1, 10)`, men svaret är 55. `50 * 1.1` är
`55.00000000000001` i datorn, och `math.ceil` avrundar den lilla
överskjutande biten uppåt till en hel krona.

Lösningen räknar med **heltal** så långt det går. Notan görs om till hela
ören med `round(total * 100)`, vilket är säkert eftersom notan har högst
två decimaler. Därefter är allt heltal, och den enda divisionen sker
sist. Den är exakt nog: när svaret är ett helt antal kronor blir
divisionen exakt, och annars ligger den långt från närmaste heltal.

Lärdom: räkna pengar i ören (eller med modulen `decimal`). Det gör alla
riktiga betalsystem.

## 1.13 Avslöja buggarna

```python
def check(seconds_to_hms):
    assert seconds_to_hms(0) == "0:00:00"
    assert seconds_to_hms(59) == "0:00:59"
    assert seconds_to_hms(65) == "0:01:05"
    assert seconds_to_hms(2700) == "0:45:00"
    assert seconds_to_hms(3600) == "1:00:00"
    assert seconds_to_hms(3665) == "1:01:05"
    assert seconds_to_hms(90000) == "25:00:00"
```

Varje fall avslöjar en sorts fel:

| Fall | Avslöjar |
|---|---|
| `0` | timmar med inledande nolla (`"00:00:00"`) |
| `65` | minuter utan inledande nolla, och sekunder som räknas fel |
| `2700` | timmar som avrundas i stället för att kapas: `round(0.75)` är 1 |
| `3665` | minuter som inte räknas om efter hela timmar (`"1:61:05"`) |
| `90000` | timmar som slår om efter ett dygn (`"1:00:00"`) |

Fel brukar gömma sig vid noll, precis vid en gräns (59 och 60, 3599 och
3600), där en del går från en till två siffror, och vid värden som är
större än man först tänker sig. Lägg märke till att 1800 sekunder inte
räcker för avrundningsbuggen: `round(0.5)` är 0 (se 1.9), så den buggiga
versionen svarar rätt där.

Att mäta tester genom att låta dem jaga avsiktligt felaktiga versioner
kallas *mutationstestning*.

## Prova själv

Koden finns i [`facit/prova_sjalv.py`](facit/prova_sjalv.py) och testerna
i [`tests/test_facit_prova_sjalv.py`](tests/test_facit_prova_sjalv.py).

### 1. Kelvin

Kelvin och Celsius har lika stora steg och är förskjutna 273,15 grader, så
det räcker med plus och minus. Talet läggs i en konstant. Testa 0 °C, 0 K
och att fram och tillbaka ger samma tal, med `pytest.approx`.

### 2. Från text till sekunder

```python
def hms_to_seconds(text):
    hours = int(text[:-6])
    minutes = int(text[-5:-3])
    seconds = int(text[-2:])
    return hours * 3600 + minutes * 60 + seconds
```

Timmarna har varierande längd, men minuter och sekunder har alltid två
siffror. Räkna därför bakifrån med negativa index. `text.find(":")`
fungerar också.

Testet fram och tillbaka, `hms_to_seconds(seconds_to_hms(n)) == n` för
många `n`, provar båda funktionerna på en gång och hittar fel som två
separata tester med handräknade svar kan missa.

### 3. Löptakt

```python
def pace(km, minutes):
    seconds_per_km = round(minutes * 60 / km)
    return f"{seconds_per_km // 60}:{seconds_per_km % 60:02d} min/km"
```

Fällan är att avrunda för sent. Delar man först upp i minuter och
sekunder och avrundar sekunderna sist blir 359,88 sekunder 5 minuter och
`round(59.88)`, alltså 60, sekunder: `"5:60"`. **Avrunda till hela
sekunder först, dela upp sedan.** Då kan resten aldrig bli 60.

### 4. Hastigheter

```python
def mph_to_kmh(mph):
    return miles_to_km(mph)
```

En hastighet är en sträcka per timme, så omvandlingen är densamma som för
sträckor. Att anropa de befintliga funktionerna gör att 1.609344 bara
står i `KM_PER_MILE`. Ett test kontrollerar det.

### 5. Decimaltal

```python
def test_floats_are_not_exact():
    assert 0.1 + 0.2 != 0.3

def test_approx_compares_with_a_tolerance():
    assert 0.1 + 0.2 == pytest.approx(0.3)
```

Datorn lagrar decimaltal binärt, och 0,1 går inte att skriva exakt binärt,
på samma sätt som 1/3 inte går att skriva exakt med decimaler. `==` kräver
exakt likhet; `pytest.approx` godtar en mycket liten skillnad. Jämför
aldrig decimaltal med `==` i tester.
