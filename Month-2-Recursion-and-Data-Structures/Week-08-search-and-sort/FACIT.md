# Facit vecka 8 — Try It Yourself

Koden finns i [`facit/prova_sjalv.py`](facit/prova_sjalv.py) och testerna
i [`tests/test_facit.py`](tests/test_facit.py). Kör tidsmätningarna med:

```
PYTHONPATH=src python3 -m facit.prova_sjalv
```

Testerna kontrollerar aldrig tider, eftersom de beror på datorn; bara att
mätningarna går att köra och att alla funktioner ger rätt svar.

## 1. Mät alla fyra sorteringsalgoritmer

`benchmark_sorts` sorterar **samma** slumpade lista (5 000 heltal) med var
och en av de fyra algoritmerna och mäter tiden med `time.perf_counter()`.
En fast `seed` gör att listan blir densamma varje gång, så att mätningar
kan jämföras. Resultatet kontrolleras också mot `sorted()`: en snabb
algoritm som sorterar fel är värdelös.

Ungefär så här brukar det se ut (tiderna varierar mellan datorer):

| Algoritm | Ungefärlig tid | Komplexitet |
|---|---|---|
| `bubble_sort` | ett par sekunder | O(n²) |
| `insertion_sort` | omkring en sekund | O(n²) |
| `merge_sort` | några hundradels sekunder | O(n log n) |
| `quick_sort` | några hundradels sekunder | O(n log n) i snitt |

Ja, skillnaden syns tydligt. Med n = 5 000 är n² = 25 miljoner men
n · log₂ n ≈ 61 000, alltså drygt 400 gånger färre steg. Prova att
fördubbla n: de två O(n²)-algoritmerna tar då ungefär fyra gånger så lång
tid, de två andra bara drygt dubbelt så lång.

`insertion_sort` är snabbare än `bubble_sort` trots samma komplexitet,
eftersom den gör färre byten. Big-O beskriver hur tiden **växer**, inte
hur lång den är.

## 2. Selection sort

```python
def selection_sort(lst):
    result = list(lst)
    for i in range(len(result)):
        smallest = i
        for j in range(i + 1, len(result)):
            if result[j] < result[smallest]:
                smallest = j
        result[i], result[smallest] = result[smallest], result[i]
    return result
```

**Komplexitet:** O(n²) i alla fall. Den inre loopen går alltid igenom hela
den osorterade delen för att vara säker på att den hittat minimum, så
även en redan sorterad lista kräver n(n − 1)/2 jämförelser. (Jämför med
`insertion_sort`, som blir O(n) på sorterad indata.) Antalet **byten** är
däremot högst n, vilket är algoritmens fördel när byten är dyra.

| Algoritm | Värsta fall | Bästa fall | Stabil? |
|---|---|---|---|
| `selection_sort` | O(n²) | O(n²) | nej |

**Stabil?** Nej. Bytet kan flytta ett element långt fram, förbi ett annat
med samma värde. Testet visar det med tre element där två har samma
nyckel: `[(2, a), (2, b), (1, c)]`. Första varvet byter plats på `(2, a)`
och `(1, c)`, och resultatet blir `[(1, c), (2, b), (2, a)]`: `a` och `b`
har bytt ordning.

## 3. Quicksort med första elementet som pivot

```python
pivot = lst[0]
less = [x for x in lst[1:] if x < pivot]
equal = [x for x in lst if x == pivot]
greater = [x for x in lst[1:] if x > pivot]
```

På en redan sorterad lista är det första elementet alltid det minsta.
Varje uppdelning ger då en tom `less` och en `greater` som bara är ett
element kortare: n nivåer av rekursion, och n + (n − 1) + … + 1 ≈ n²/2
jämförelser. Det är quicksorts värsta fall, O(n²). Med mittelementet som
pivot (som i `quick_sort`) delas en sorterad lista i två lika stora
halvor, och det blir O(n log n).

I Python syns värsta fallet på ett extra tydligt sätt: med en nivå av
rekursion per element slår funktionen i Pythons gräns på ungefär 1 000
nivåer och kraschar med `RecursionError` redan för några tusen element.
Testet visar att 5 000 sorterade element ger `RecursionError` för
första-element-pivoten men går utmärkt med mittelementet. Därför mäter
`benchmark_sorted_input` på 900 element, där skillnaden i tid ändå syns
tydligt.

Lärdomen: pivotvalet spelar stor roll, och "första elementet" är det
sämsta valet för indata som redan är sorterad, något som är vanligt i
verkligheten. Riktiga implementationer väljer mittelementet, medianen av
tre, eller ett slumpat element.

## 4. find_all i O(log n + k)

Idén: i en sorterad lista ligger alla förekomster av ett värde **intill
varandra**. Det räcker därför att hitta var gruppen börjar och var den
slutar, med två binärsökningar:

```python
def find_all(sorted_lst, target):
    start = _first_index_not_less_than(sorted_lst, target)   # första >= target
    end = _first_index_greater_than(sorted_lst, target)      # första > target
    return list(range(start, end))
```

De två hjälpfunktionerna är binärsökning med en skillnad mot veckans
version: de slutar inte när de hittar target, utan fortsätter tills
intervallet krympt till en enda plats. Den enda skillnaden mellan dem är
`<` mot `<=` i jämförelsen. Varje sökning tar O(log n), och att bygga
listan med de k träffarna tar O(k): totalt O(log n + k).

Att i stället hitta en träff med `binary_search_iterative` och sedan gå
åt vänster och höger tills värdet ändras ger också rätt svar, men blir
O(n) om nästan hela listan är samma värde.

(Pythons standardbibliotek har samma funktioner färdiga: `bisect_left`
och `bisect_right` i modulen `bisect`.)

## 5. Sätt in i en sorterad lista

```python
def insert_sorted(sorted_lst, value):
    position = _first_index_greater_than(sorted_lst, value)
    sorted_lst.insert(position, value)
```

Att hitta platsen tar O(log n) med binärsökning. Men `list.insert` måste
flytta varje element efter platsen ett steg åt höger för att göra plats,
och det tar O(n) i värsta fall (insättning först). **Den bästa möjliga
komplexiteten med en vanlig lista är alltså O(n)**, och flaskhalsen är
flytten, inte sökningen. Det är ändå bättre än att lägga till sist och
sortera om, O(n log n).

Vill man ha snabbare insättning behövs en annan datastruktur: i en
länkad lista (vecka 7) är själva insättningen O(1), men där går det inte
att binärsöka, så att hitta platsen blir O(n). Balanserade sökträd ger
O(log n) för båda, men det ligger utanför den här kursen.
