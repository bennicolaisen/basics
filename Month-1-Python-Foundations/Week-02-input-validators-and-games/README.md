# Vecka 2 — Beslut och upprepning: if, loopar, listor och fel

## Syfte

Förra veckans program gjorde samma sak varje gång, rad för rad uppifrån.
Riktiga program fattar beslut ("om lösenordet är för kort, säg till") och
upprepar saker ("fråga igen tills svaret är ett tal"). Den här veckan lär
du dig de två verktygen för det: villkor (`if`) och loopar (`while`,
`for`). Du lär dig också listor, så att ett program kan hantera många
värden, och hur man fångar fel i stället för att låta programmet krascha.
Veckans projekt är funktioner som kontrollerar användarnamn och lösenord,
och ett gissningsspel som använder dem.

## Mål

När veckan är klar kan du:

- jämföra värden och kombinera villkor med `and`, `or` och `not`
- välja mellan olika vägar i koden med `if`, `elif` och `else`
- upprepa kod med `while` och `for`, och avbryta en loop med `break`
- räkna med `range` och gå igenom en text tecken för tecken
- skapa listor, hämta värden med index och lägga till med `append`
- fånga fel med `try`/`except` och kasta egna fel med `raise`
- använda modulen `random`

## Genomgång

Gör övningarna efter varje steg. De finns i `ovningar/`, och du
kontrollerar dem som förra veckan:

```
python -m pytest kontroll -k 03
```

### Steg 1: Sant och falskt

En **jämförelse** ger alltid `True` (sant) eller `False` (falskt), alltså
ett `bool`-värde:

| Jämförelse | Betyder | `5 ? 3` |
|---|---|---|
| `==` | lika med | `False` |
| `!=` | inte lika med | `True` |
| `<` | mindre än | `False` |
| `>` | större än | `True` |
| `<=` | mindre än eller lika med | `False` |
| `>=` | större än eller lika med | `True` |

Kom ihåg: `=` sparar ett värde i en variabel, `==` jämför två värden.

Villkor kombineras med tre ord:

- `a and b` är sant om **båda** är sanna.
- `a or b` är sant om **minst en** är sann.
- `not a` vänder på det: `not True` är `False`.

```python
age = 20
print(age >= 18 and age < 65)    # True
print(age < 12 or age >= 65)     # False
print(not age >= 18)             # False
```

Text kan också jämföras: `"Oslo" == "Oslo"` är `True`, men `"oslo" ==
"Oslo"` är `False` eftersom stora och små bokstäver skiljer sig.

En funktion kan returnera en jämförelse direkt:

```python
def is_adult(age):
    return age >= 18
```

**Öva:** övning 2.1.

### Steg 2: if, elif och else

`if` kör kod bara om villkoret är sant:

```python
temperature = -3
if temperature < 0:
    print("Det är minusgrader.")
    print("Klä dig varmt.")
print("Det här skrivs alltid ut.")
```

Raderna som hör till `if` är **indragna** med fyra mellanslag, precis som
i en funktion. Den första raden utan indrag är tillbaka i den vanliga
ordningen.

Med `else` anger du vad som ska hända annars, och med `elif` ("else if")
kan du pröva fler villkor i tur och ordning:

```python
if temperature < 0:
    print("Minusgrader")
elif temperature < 15:
    print("Svalt")
else:
    print("Varmt")
```

Python prövar villkoren uppifrån och kör **bara den första gren som är
sann**. Resten hoppas över. Därför spelar ordningen roll: i exemplet ovan
behöver `elif temperature < 15` inte säga "och inte under 0", eftersom
det redan är avgjort.

**Öva:** övning 2.2 till 2.5.

### Steg 3: while-loopen

En `while`-loop upprepar sin kod så länge villkoret är sant:

```python
count = 3
while count > 0:
    print(count)
    count = count - 1
print("Klart!")
```

Varje varv kontrolleras villkoret först. När `count` blivit 0 är det
falskt, och programmet fortsätter efter loopen. Om du glömmer att ändra
`count` blir villkoret aldrig falskt och loopen går för evigt. Avbryt ett
program som hängt sig med **Ctrl+C** i terminalen.

`while True:` är en loop som aldrig slutar av sig själv. Den avbryts med
`break`, som hoppar ut ur loopen direkt:

```python
while True:
    answer = input("Skriv 'sluta' för att sluta: ")
    if answer == "sluta":
        break
print("Hej då!")
```

`continue` hoppar i stället direkt till nästa varv.

**Öva:** övning 2.6.

### Steg 4: for-loopen och range

En `for`-loop går igenom något, ett värde i taget:

```python
for character in "Umeå":
    print(character)       # U, m, e, å på var sin rad
```

`range` ger en följd av heltal:

| Uttryck | Ger talen |
|---|---|
| `range(5)` | 0, 1, 2, 3, 4 |
| `range(1, 6)` | 1, 2, 3, 4, 5 |
| `range(0, 10, 2)` | 0, 2, 4, 6, 8 |

Observera att `range` slutar **strax före** det sista talet. `range(1,
6)` ger 1 till 5. Vill du ha talen 1 till n skriver du `range(1, n + 1)`.

Ett vanligt mönster är att samla ihop något i en variabel under loopen:

```python
total = 0
for number in range(1, 5):
    total = total + number
print(total)    # 1 + 2 + 3 + 4 = 10
```

`total = total + number` skrivs ofta kortare som `total += number`.

**När `while` och när `for`?** Använd `for` när du vet vad du ska gå
igenom (talen 1–10, varje tecken i en text). Använd `while` när du inte
vet hur många varv det blir (fråga tills svaret är rätt).

**Öva:** övning 2.7 till 2.9.

### Steg 5: Listor

En **lista** håller många värden i en bestämd ordning:

```python
temperatures = [12.5, 14.0, 9.8]
names = ["Alva", "Bo", "Cyril"]
empty = []
```

Varje värde har ett **index**, ett nummer för sin plats. Index börjar på
**0**:

```python
print(names[0])      # Alva  (första)
print(names[2])      # Cyril (tredje)
print(names[-1])     # Cyril (-1 betyder sista)
print(len(names))    # 3
```

Försöker du hämta `names[3]` blir det ett `IndexError`, eftersom det inte
finns något fjärde värde.

Listor kan ändras:

```python
names.append("Dina")   # lägg till sist
names[0] = "Ada"        # byt ut det första
```

En `for`-loop går igenom en lista precis som en text:

```python
for name in names:
    print(f"Hej, {name}!")
```

Användbara inbyggda funktioner för listor med tal: `sum(lista)`,
`min(lista)`, `max(lista)` och `len(lista)`. Med `in` frågar du om ett
värde finns: `"Bo" in names` är `True`.

**Öva:** övning 2.11 till 2.13.

### Steg 6: Text är också en följd

En text fungerar i mycket som en lista med tecken: den har index,
`len()` ger antalet tecken, och `for` går igenom tecknen. Med **slicing**
plockar du ut en bit:

```python
city = "Göteborg"
print(city[0])       # G
print(city[0:4])     # Göte   (index 0 till 3; slutet räknas inte med)
print(city[4:])      # borg   (från index 4 till slutet)
print(city[::-1])    # grobetöG (baklänges)
```

Text har också **metoder**, funktioner som anropas med en punkt efter
texten:

| Metod | Gör | `"  Hej Du  "` blir |
|---|---|---|
| `.lower()` | små bokstäver | `"  hej du  "` |
| `.upper()` | stora bokstäver | `"  HEJ DU  "` |
| `.strip()` | tar bort mellanslag i början och slutet | `"Hej Du"` |
| `.replace("Du", "dig")` | byter ut text | `"  Hej dig  "` |
| `.count("j")` | hur många gånger något förekommer | `1` |

Och frågor som svarar `True` eller `False` för varje tecken eller hela
texten: `.isdigit()` (bara siffror), `.isalpha()` (bara bokstäver),
`.isalnum()` (bokstäver eller siffror), `.isupper()`, `.islower()`.

Text kan inte ändras på plats: metoderna ger en **ny** text tillbaka.
`city.upper()` ändrar inte `city`; skriv `city = city.upper()` om du vill
spara resultatet.

**Öva:** övning 2.10 och 2.18.

### Steg 7: Fel som går att hantera

När något går fel **kastar** Python ett undantag (*exception*), till
exempel `ValueError` när `int("sju")` inte går. Med `try` och `except`
fångar du felet och bestämmer själv vad som ska hända:

```python
text = input("Skriv ett tal: ")
try:
    number = int(text)
    print(f"Dubbelt så mycket är {number * 2}")
except ValueError:
    print("Det där var inget heltal.")
```

Om något i `try`-blocket kastar ett `ValueError` hoppar Python direkt till
`except`-blocket. Om inget fel uppstår hoppas `except` över.

Tillsammans med en loop blir det mönstret för "fråga tills svaret är
rätt":

```python
while True:
    try:
        age = int(input("Hur gammal är du? "))
        break
    except ValueError:
        print("Skriv ålder med siffror.")
```

Dina egna funktioner kan också kasta fel, med `raise`. Det är rätt när
funktionen får något den inte kan ge ett vettigt svar på:

```python
def average(numbers):
    if len(numbers) == 0:
        raise ValueError("listan är tom")
    return sum(numbers) / len(numbers)
```

Det är bättre än att returnera ett påhittat svar som 0, som kan se rätt
ut och leda till fel längre fram.

**Öva:** övning 2.13 till 2.15.

### Steg 8: Slumptal

Python har många färdiga **moduler**, samlingar av funktioner som du
hämtar in med `import`. Modulen `random` ger slumptal:

```python
import random

dice = random.randint(1, 6)    # ett heltal från 1 till 6 (båda inräknade)
print(dice)
```

Veckans projekt använder `random` för att välja talet i gissningsspelet.

**Öva:** övning 2.16 och 2.17, som blandar allt från veckan.

## Veckans projekt: kontroller och ett gissningsspel

```
Week-02-input-validators-and-games/
├── starta.py                        - startar spelet: python starta.py
├── src/
│   └── validators_and_games/
│       ├── validators.py            - funktioner som kontrollerar text (testas)
│       └── game.py                  - gissningsspelet
├── tests/
│   ├── test_validators.py           - tester för validators.py
│   ├── test_game.py                 - tester för spelet
│   └── test_facit_prova_sjalv.py    - tester för facit till "Prova själv"
├── ovningar/  kontroll/  facit/     - övningar, kontroller och lösningar
└── FACIT.md                         - förklarade lösningar till "Prova själv"
```

**`validators.py`** har tre funktioner:

- `is_valid_username(text)` kontrollerar längden, att första tecknet är en
  bokstav (`text[0].isalpha()`), och sedan varje tecken med en `for`-loop.
  Så fort ett tecken är fel returneras `False`. Kommer loopen hela vägen
  igenom är alla tecken godkända, och `True` returneras efter loopen.
- `is_strong_password(text)` använder fyra variabler som börjar som
  `False` och sätts till `True` när loopen hittar en stor bokstav, en
  liten, en siffra eller ett annat tecken. Sist kombineras de med `and`.
- `parse_int_in_range(text, low, high)` gör om text till ett tal och
  kastar ett `ValueError` med ett tydligt meddelande om det inte går eller
  om talet ligger utanför intervallet.

**`game.py`** återanvänder `parse_int_in_range`. `ask_for_guess` frågar i
en `while True`-loop tills gissningen är giltig. `play_game` har en
`for`-loop med ett varv per försök, och lämnar funktionen med `return`
direkt vid rätt svar. Det rätta talet skickas in som en parameter
(`secret`), i stället för att slumpas inne i `play_game`. Det gör att
testerna kan bestämma svaret och kontrollera spelet; `main()` slumpar
talet med `random.randint` när man spelar på riktigt.

Testerna för spelet ersätter `input` med en funktion som "skriver in"
färdiga svar. Verktyget för det heter `monkeypatch` i pytest.

Lägg också märke till hur testerna i `test_validators.py` väljer sina
exempel: precis vid varje gräns och strax utanför (2, 3, 20 och 21 tecken
för användarnamn). Det är där felen brukar sitta.

## Köra programmet

```
python starta.py
```

Prova att skriva en bokstav, ett för stort tal och sedan riktiga
gissningar.

## Testa

```
python -m pytest                   # testerna för veckans projekt
python -m pytest kontroll          # kontrollerna av dina övningar
python -m pytest kontroll --facit  # visar att facit klarar alla kontroller
```

## Prova själv

1. Skriv `is_valid_email(text)` med en förenklad regel: inga mellanslag,
   exakt ett `@`, något före `@`, och efter `@` minst en punkt som varken
   står först eller sist. Testa varje regel vid gränsen, som
   `test_validators.py` gör.
2. Ändra spelet så att en ogiltig gissning (inte ett tal, eller utanför
   intervallet) kostar ett försök i stället för att vara gratis. Tala om
   för spelaren vad som var fel och hur många försök som är kvar.
3. Lägg till en svårighetsmeny (lätt: 1–10 och 5 försök, medel: 1–100 och
   7 försök, svår: 1–1000 och 10 försök) som frågar innan spelet startar,
   utan att ändra `play_game`.
4. Skriv `count_valid_usernames(candidates)`, som tar en lista med
   användarnamn och returnerar hur många av dem som är giltiga. Använd
   `is_valid_username`.
5. Lägg en "Spela igen? (j/n)"-loop runt spelet som räknar vinster och
   förluster och skriver ut ställningen efter varje omgång.

## Facit

- Lösningar till övning 2.1–2.18 finns i `facit/`, med samma filnamn som
  i `ovningar/`.
- Lösningar till "Prova själv" finns i `facit/prova_sjalv.py`, med
  förklaringar i [`FACIT.md`](FACIT.md).
