# Vecka 4 — Samlingar: listor, tupler, dictionaries och mängder

## Syfte

De flesta program hanterar många värden på en gång: alla ord i en text,
alla temperaturer under en vecka, alla kunder i ett register. Python har
fyra inbyggda **samlingar** för det, och var och en är bra på något
särskilt. Den här veckan lär du dig alla fyra, när du ska välja vilken,
och de kortare skrivsätt (comprehensions) som gör kod med samlingar läsbar.
Du lär dig också läsa och skriva filer, och tar en första titt på klasser,
som du behöver i vecka 7 och lär dig ordentligt i vecka 9. Veckans projekt
läser en textfil och tar fram statistik om orden. Det här är sista veckan
med grunderna i Python; från vecka 5 bygger kursen vidare på dem.

## Mål

När veckan är klar kan du:

- använda listors metoder och skilja på `sorted()` och `.sort()`
- skapa tupler och packa upp dem i flera variabler
- slå upp, lägga till och räkna med dictionaries
- ta bort dubbletter och jämföra samlingar med mängder
- välja rätt samling för en uppgift
- skriva list comprehensions, med och utan villkor
- sortera med en egen nyckel, och styra hur lika värden sorteras
- läsa och skriva textfiler, och läsa argument från terminalen
- skapa en enkel klass med `__init__`, attribut och metoder

## Genomgång

Övningarna finns i `ovningar/` och kontrolleras med
`python -m pytest kontroll -k 05` (byt 05 mot övningens nummer).

### Steg 1: Listor på djupet

Du kan redan skapa listor, hämta med index och lägga till med `append`.
Några fler verktyg:

```python
cities = ["Umeå", "Luleå", "Kiruna"]
cities.insert(0, "Visby")    # lägg in på plats 0
cities.remove("Luleå")       # ta bort ett värde
last = cities.pop()          # ta bort och returnera det sista: "Kiruna"
print(cities[0:2])           # slicing fungerar som för text: ['Visby', 'Umeå']
```

**`sorted()` eller `.sort()`?** Båda sorterar, men på olika sätt:

```python
numbers = [3, 1, 2]
ordered = sorted(numbers)    # ny sorterad lista; numbers är oförändrad
numbers.sort()               # sorterar numbers själv; returnerar None
```

En funktion som får en lista ska oftast inte ändra den, eftersom den som
anropade kanske fortfarande behöver den som den var. Använd därför
`sorted()` i funktioner.

Det hänger ihop med en viktig egenskap: en lista kan ändras (den är
*muterbar*), och två namn kan peka på **samma** lista:

```python
a = [1, 2]
b = a           # b är ett nytt namn på samma lista, ingen kopia
b.append(3)
print(a)        # [1, 2, 3]
```

Vill du ha en kopia skriver du `b = list(a)` eller `b = a.copy()`.

**Öva:** övning 4.1.

### Steg 2: Tupler

En **tupel** är som en lista som inte kan ändras. Den skrivs med vanliga
parenteser:

```python
point = (59.33, 18.07)
print(point[0])     # 59.33
```

Tupler används för ett litet, fast antal värden som hör ihop, som
koordinater eller ett par (ord, antal). Det stora tricket är
**uppackning**: värdena i en tupel kan läggas i flera variabler på en
gång.

```python
latitude, longitude = point
```

Det gör att en funktion kan returnera flera svar:

```python
def min_and_max(numbers):
    return (min(numbers), max(numbers))

lowest, highest = min_and_max([3, -1, 8])
```

Parenteserna kan ofta utelämnas: `return min(numbers), max(numbers)` och
`a, b = b, a` (som byter plats på två variabler) är också tupler.

**Öva:** övning 4.2 till 4.4.

### Steg 3: Dictionaries

En **dictionary** (`dict`, ordbok) kopplar **nycklar** till **värden**. I
stället för att hämta med ett nummer, som i en lista, hämtar du med
nyckeln:

```python
population = {"Stockholm": 984748, "Umeå": 132235}
print(population["Umeå"])         # 132235
population["Kiruna"] = 22423      # lägg till (eller ändra) ett värde
print("Visby" in population)      # False: in frågar om nycklarna
print(len(population))            # 3
```

Att hämta en nyckel som inte finns ger `KeyError`. Med `.get` får du ett
standardvärde i stället:

```python
print(population.get("Visby", 0))    # 0
```

Så här går du igenom en dictionary:

```python
for city, people in population.items():
    print(f"{city}: {people}")
```

**Räknemönstret** är det vanligaste du kommer att göra med dictionaries:

```python
counts = {}
for word in ["sol", "regn", "sol"]:
    counts[word] = counts.get(word, 0) + 1
# {'sol': 2, 'regn': 1}
```

Nycklar måste vara värden som inte kan ändras: text, tal och tupler går
bra, listor gör det inte.

**Öva:** övning 4.5 till 4.8, 4.14 och 4.15.

### Steg 4: Mängder

En **mängd** (`set`) innehåller bara unika värden, utan bestämd ordning:

```python
weather = {"sol", "regn", "sol"}
print(weather)                  # {'sol', 'regn'} (ordningen kan variera)
unique = set(["a", "b", "a"])   # gör om en lista till en mängd
weather.add("snö")
print("snö" in weather)         # True, och snabbt även för stora mängder
```

Mängder kan jämföras med varandra:

| Uttryck | Ger |
|---|---|
| `a & b` | värden som finns i båda |
| `a \| b` | värden som finns i någon av dem |
| `a - b` | värden som finns i `a` men inte i `b` |

En tom mängd skrivs `set()`, eftersom `{}` är en tom dictionary.

**Vilken samling ska jag välja?**

| Samling | Välj den när |
|---|---|
| `list` | ordningen spelar roll och samma värde kan förekomma flera gånger |
| `tuple` | några värden hör ihop och ska inte ändras, som (ord, antal) |
| `dict` | du vill slå upp ett värde med en nyckel, som namn → nummer |
| `set` | du bara bryr dig om vilka olika värden som finns |

**Öva:** övning 4.9 och 4.10.

### Steg 5: Comprehensions

En **list comprehension** bygger en ny lista ur en annan på en rad. De
här två gör samma sak:

```python
squares = []
for x in range(1, 5):
    squares.append(x ** 2)

squares = [x ** 2 for x in range(1, 5)]    # [1, 4, 9, 16]
```

Läs den som "x i kvadrat, för varje x i range(1, 5)". Med `if` sist
filtrerar du:

```python
long_words = [word for word in words if len(word) > 3]
```

Det finns comprehensions för dictionaries och mängder också:

```python
lengths = {word: len(word) for word in words}
first_letters = {word[0] for word in words}
```

Använd en comprehension när loopen bara räknar ut ett värde per element
och samlar ihop dem. Gör loopen något mer (skriver ut, räknar flera
saker), skriv en vanlig loop.

**Öva:** övning 4.11 och 4.12.

### Steg 6: Sortera med en nyckel

`sorted` jämför värdena direkt: tal efter storlek, text i
bokstavsordning. Med `key` bestämmer du vad som ska jämföras. `key` ska
vara en funktion som får ett värde och returnerar det som ska jämföras:

```python
words = ["snöstorm", "is", "regn"]
print(sorted(words, key=len))    # ['is', 'regn', 'snöstorm']
```

Lägg märke till att det står `len`, inte `len()`: du skickar själva
funktionen, och `sorted` anropar den för varje ord.

`reverse=True` vänder ordningen. Och genom att låta nyckelfunktionen
returnera en tupel kan du sortera på flera saker: tupler jämförs ett
värde i taget, så `(len(word), word)` sorterar på längd först och, vid
lika längd, i bokstavsordning:

```python
def length_then_word(word):
    return (len(word), word)

sorted(["sol", "is", "snö"], key=length_then_word)    # ['is', 'snö', 'sol']
```

För korta nyckelfunktioner används ofta **`lambda`**, en funktion utan
namn som skrivs direkt där den behövs:

```python
sorted(words, key=lambda word: (len(word), word))
```

**Öva:** övning 4.13 och 4.14.

### Steg 7: Filer och argument

Så här läser du en hel textfil:

```python
with open("text.txt", encoding="utf-8") as file:
    content = file.read()
```

- `open` öppnar filen. `encoding="utf-8"` säger hur tecken som å, ä och ö
  är lagrade; skriv alltid ut det.
- `with` ser till att filen stängs när blocket är klart, även om något
  går fel.
- `file.read()` ger hela innehållet som en text. Med `for line in file:`
  får du i stället en rad i taget (med radbrytningen `\n` sist).

För att skriva öppnar du med `"w"` (*write*). En befintlig fil skrivs
över; `"a"` (*append*) lägger till sist i stället:

```python
with open("ut.txt", "w", encoding="utf-8") as file:
    file.write("Första raden\n")
```

En **sökväg** (*path*) säger var filen finns. En relativ sökväg som
`"text.txt"` letas efter i mappen där terminalen står.

Program kan få **argument** från terminalen: `python starta.py
min_text.txt`. De hamnar i listan `sys.argv` (efter `import sys`), där
`sys.argv[0]` är programmets namn och `sys.argv[1]` det första
argumentet.

**Öva:** övning 4.16 och 4.17.

### Steg 8: Klasser, en första titt

Ibland hör några värden och några funktioner så tydligt ihop att man vill
göra en egen datatyp av dem. Det gör man med en **klass**:

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


r = Rectangle(3, 4)    # skapa ett objekt
print(r.width)         # 3
print(r.area())        # 12
```

- En klass är en ritning; `Rectangle(3, 4)` skapar ett **objekt** (en
  *instans*) efter ritningen.
- `__init__` (två understreck på var sida) körs automatiskt när objektet
  skapas. Där sparas värdena.
- `self` är objektet självt. `self.width = width` sparar värdet som ett
  **attribut** på objektet.
- Funktioner i en klass kallas **metoder**. De får alltid `self` först,
  och kommer åt objektets attribut genom det. När du anropar `r.area()`
  skickar Python in `r` som `self` automatiskt.

Du har använt metoder hela tiden: `"hej".upper()` och `lista.append(3)`
anropar metoder på ett text- och ett listobjekt. Klasser kommer tillbaka i
vecka 7, där du bygger egna datastrukturer, och i vecka 9, som handlar
helt om dem.

**Öva:** övning 4.18.

## Veckans projekt: textanalys

```
Week-04-text-analyzer/
├── starta.py                        - python starta.py [fil]
├── src/
│   └── text_analyzer/
│       ├── analyzer.py              - funktioner som analyserar ord (testas)
│       ├── cli.py                   - läser filen och skriver ut rapporten
│       └── data/
│           └── sample.txt           - exempeltext
├── tests/
│   ├── test_analyzer.py
│   └── test_facit_prova_sjalv.py
├── ovningar/  kontroll/  facit/
└── FACIT.md
```

Samma uppdelning som i de andra veckorna: `analyzer.py` räknar och
returnerar, `cli.py` läser filen och skriver ut. Varje funktion i
`analyzer.py` använder den samling som passar uppgiften:

- **`tokenize`** returnerar en **lista** med orden, i ordning och med
  upprepningar, eftersom det är så de står i texten. Skiljetecknen tas
  bort med en loop som hoppar över alla tecken i `string.punctuation` (en
  färdig text med alla skiljetecken).
- **`word_frequencies`** returnerar en **dictionary** ord → antal, med
  räknemönstret från steg 3.
- **`top_n_words`** returnerar en lista med **tupler** (ord, antal).
  `frequencies.items()` ger just sådana tupler, och de sorteras med
  nyckeln `by_count_then_word`, som returnerar `(-count, word)`.
  Minustecknet gör att högst antal kommer först, utan att
  bokstavsordningen vid lika antal också vänds.
- **`unique_words`** returnerar en **mängd**, eftersom det bara handlar om
  vilka olika ord som finns.
- **`longest_words`** tar bort dubbletter med `unique_words` **innan** den
  sorterar. Annars skulle ett långt ord som förekommer fem gånger ta fem
  av platserna.

`cli.py` läser filen med `with open(...)` och väljer fil efter
`sys.argv`, precis som i steg 7. `Path(__file__).parent / "data" /
"sample.txt"` bygger sökvägen till exempeltexten utifrån var `cli.py`
själv ligger, så att den hittas oavsett var terminalen står.

## Köra programmet

```
python starta.py                 # analysera exempeltexten
python starta.py din_text.txt    # analysera en egen textfil
```

## Testa

```
python -m pytest                   # testerna för veckans projekt
python -m pytest kontroll          # kontrollerna av dina övningar
python -m pytest kontroll --facit  # visar att facit klarar alla kontroller
```

`test_analyzer.py` prövar skiljetecken mitt i och i slutet av ord, stora
och små bokstäver, tom text, och framför allt reglerna för lika antal och
lika längd, där det är lättast att göra fel.

## Prova själv

1. `tokenize` tar bort skiljetecken även inne i ord, så "don't" blir
   "dont". Skriv `tokenize_keep_inner(text)` som bara tar bort skiljetecken
   i **början och slutet** av varje ord, så att "don't" behålls men
   "(nu)" blir "nu". Ord som bara bestod av skiljetecken ska försvinna.
2. Skriv `bigrams(tokens)`, som returnerar alla par av ord som står efter
   varandra (`["a", "b", "c"]` ger `[("a", "b"), ("b", "c")]`), och
   `most_common_bigram(tokens)`, som återanvänder `word_frequencies` och
   `top_n_words` i stället för att räkna på nytt.
3. Skriv `top_n_words_without(frequencies, n, stopwords)`, som hoppar över
   vanliga småord som "och", "det" och "att" (de får du som en mängd).
4. Skriv `average_word_length(tokens)`, som kastar `ValueError` för en tom
   lista. Ska den räkna på alla ord, med upprepningar, eller bara på de
   unika? Bestäm dig, och skriv ett test som visar skillnaden.
5. Gör så att `top_n_words` och `longest_words` kastar `ValueError` om `n`
   är 0 eller negativt, och testa båda fallen.

## Facit

- Lösningar till övning 4.1–4.18 finns i `facit/`, med samma filnamn som
  i `ovningar/`.
- Lösningar till "Prova själv" finns i `facit/prova_sjalv.py`, med
  förklaringar i [`FACIT.md`](FACIT.md).
