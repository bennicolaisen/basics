# Facit vecka 5 — Try It Yourself

Koden finns i [`facit/prova_sjalv.py`](facit/prova_sjalv.py) och testerna
i [`tests/test_facit.py`](tests/test_facit.py). Kör dem med
`python -m pytest` i veckans mapp.

## 1. Spåra fibonacci(6) för hand

Varje anrop med `n >= 2` delar sig i två: `fibonacci(n - 1)` och
`fibonacci(n - 2)`. Trädet blir (svaret efter pilen):

```
fibonacci(6)                                   -> 5 + 3 = 8
├── fibonacci(5)                               -> 3 + 2 = 5
│   ├── fibonacci(4)                           -> 2 + 1 = 3
│   │   ├── fibonacci(3)                       -> 1 + 1 = 2
│   │   │   ├── fibonacci(2)                   -> 1 + 0 = 1
│   │   │   │   ├── fibonacci(1)  -> 1   (basfall)
│   │   │   │   └── fibonacci(0)  -> 0   (basfall)
│   │   │   └── fibonacci(1)      -> 1   (basfall)
│   │   └── fibonacci(2)          -> 1   (samma delträd som ovan)
│   └── fibonacci(3)              -> 2   (samma delträd som ovan)
└── fibonacci(4)                  -> 3   (samma delträd som ovan)
```

Svaret är **8**, och det görs **25 anrop** totalt. Lägg märke till hur
samma delproblem räknas om och om igen: `fibonacci(4)` två gånger,
`fibonacci(3)` tre gånger och `fibonacci(2)` fem gånger. Det är orsaken
till att funktionen blir så långsam (uppgift 2) och det som memoisering
löser (uppgift 3).

`fibonacci_trace` i facit skriver ut samma träd med indrag, så att du kan
jämföra med ditt eget.

## 2. Räkna anropen

```python
call_count = 0

def fibonacci_counted(n: int) -> int:
    global call_count
    call_count += 1
    if n < 2:
        return n
    return fibonacci_counted(n - 1) + fibonacci_counted(n - 2)
```

`global call_count` behövs eftersom funktionen ändrar en variabel utanför
sig själv; utan den skulle `call_count += 1` skapa en ny lokal variabel och
ge ett fel.

`fibonacci(20)` gör **21 891** anrop. Det är mindre än `2 ** 20 =
1 048 576`, men växer i samma takt: antalet anrop är `2 · fibonacci(n + 1)
- 1`, och Fibonaccitalen växer ungefär som 1,618ⁿ (det gyllene snittet).
Varje gång `n` ökar med ett blir arbetet drygt 60 % större. `fibonacci(40)`
kräver över 300 miljoner anrop och tar märkbart lång tid, och
`fibonacci(90)` skulle kräva omkring 10¹⁹ anrop, vilket i Python tar
tiotusentals år. Det kallas **exponentiell** tidskomplexitet.

## 3. Memoisering

```python
def fibonacci_memo(n: int, cache: dict[int, int] | None = None) -> int:
    if cache is None:
        cache = {}
    if n in cache:
        return cache[n]
    if n < 2:
        result = n
    else:
        result = fibonacci_memo(n - 1, cache) + fibonacci_memo(n - 2, cache)
    cache[n] = result
    return result
```

Varje svar sparas i `cache` första gången det räknas ut. Nästa gång samma
`n` efterfrågas returneras det sparade svaret direkt. Med räknaren från
uppgift 2 blir det **39 anrop** för `fibonacci(20)` i stället för 21 891,
och i allmänhet `2n - 1`: tidskomplexiteten går från exponentiell till
**linjär**. `fibonacci_memo(90)` svarar omedelbart.

En fälla: skriv inte `cache: dict = {}` som standardvärde. Ett
standardvärde skapas **en gång**, när funktionen definieras, så alla anrop
skulle dela samma dictionary. Här vore det inte ens fel (svaren är ju
desamma), men i andra funktioner ger det mycket förvirrande buggar.
Mönstret `None` + `if cache is None: cache = {}` ger en ny dictionary vid
varje anrop utifrån. (I verkliga program används ofta
`functools.cache`, som gör samma sak.)

## 4. Factorial med ackumulator

```python
def factorial_acc(n: int, acc: int = 1) -> int:
    if n == 0:
        return acc
    return factorial_acc(n - 1, acc * n)
```

Spåra `factorial_acc(4)`:

```
factorial_acc(4, 1)
factorial_acc(3, 4)       # 1 * 4
factorial_acc(2, 12)      # 4 * 3
factorial_acc(1, 24)      # 12 * 2
factorial_acc(0, 24)      # 24 * 1
-> 24
```

Skillnaden mot den vanliga `factorial`: där sker multiplikationen
**efter** att det rekursiva anropet returnerat (`n * factorial(n - 1)`),
så varje anrop måste vänta och spåret har en "ihopfällande" halva där
svaren multipliceras på vägen tillbaka. Med en ackumulator sker
multiplikationen **före** anropet. När basfallet nås är svaret redan
klart, och varje anrop returnerar bara vidare samma värde: det finns
ingen ihopfällande halva.

Ett anrop där det rekursiva anropet är det allra sista som händer kallas
**svansrekursion** (*tail recursion*). Vissa språk kan då återanvända
samma plats på anropsstacken. Python gör inte det, så här är fördelen
bara att tänka på problemet på ett annat sätt.

## 5. count_up utan loop

```python
def count_up(n: int) -> None:
    if n <= 0:
        return
    count_up(n - 1)
    print(n)
```

Nyckeln är ordningen. Det rekursiva anropet kommer **före** `print`, så
`count_up(5)` anropar först `count_up(4)`, som anropar `count_up(3)`, och
så vidare ner till basfallet. Utskrifterna sker sedan på vägen tillbaka:
1 först, 5 sist. Flyttar du `print(n)` före anropet räknar funktionen i
stället ner, från 5 till 1.
