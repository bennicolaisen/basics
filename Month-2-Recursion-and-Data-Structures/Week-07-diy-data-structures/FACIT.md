# Facit vecka 7 — Try It Yourself

Koden finns i [`facit/prova_sjalv.py`](facit/prova_sjalv.py) och testerna
i [`tests/test_facit.py`](tests/test_facit.py). Kör dem med
`python -m pytest` i veckans mapp.

Lösningarna bygger vidare på veckans klasser med **arv**
(`class ReversibleLinkedList(LinkedList)`), så att referenskoden står kvar
orörd. I ett riktigt projekt skulle du lägga metoderna direkt i
`LinkedList`.

## 1. Tester för `__repr__`, och `__contains__`

Två bra tester för `__repr__`: den tomma listan (`"LinkedList([])"`) och
en lista med olika sorters värden, där texten visar att varje värde
skrivs med sin egen `repr` (`'a'` med citattecken, `None` utan).

```python
class LinkedListWithContains(LinkedList):
    def __contains__(self, value) -> bool:
        return self.find(value)
```

En överraskning som ett av testerna visar: `value in my_list` fungerade
redan **innan** `__contains__` fanns. När en klass saknar `__contains__`
använder Python `__iter__` i stället och går igenom värdena ett i taget.
Att skriva `__contains__` ändrar alltså inte vad `in` svarar, men det gör
beteendet uttryckligt och låter klassen välja ett snabbare sätt om det
finns ett. För en länkad lista finns inget snabbare; för en mängd eller
dictionary är det just `__contains__` som gör `in` till O(1).

## 2. Dubbellänkad lista

Varje nod får en pekare bakåt, `prev`, utöver `next`. Det kräver mer
omsorg vid varje ändring: när en nod läggs till eller tas bort måste
**både** `next` hos noden före och `prev` hos noden efter uppdateras.
Därför samlar lösningen borttagningen i en enda metod, `_unlink`, som alla
andra använder:

```python
def _unlink(self, node):
    if node.prev is None:
        self.head = node.next
    else:
        node.prev.next = node.next
    if node.next is None:
        self.tail = node.prev
    else:
        node.next.prev = node.prev
    self._size -= 1
```

**Vad blir O(1) som var O(n)?** Att ta bort en nod man redan har, och
framför allt **den sista noden**. I den enkellänkade listan måste
`delete` hålla reda på noden före (`prev` i loopen) eftersom noden själv
inte vet vem som pekar på den, och att ta bort den sista kräver att man
går igenom hela listan för att hitta den näst sista. Med `tail.prev` nås
den direkt. Att *leta upp* ett värde är fortfarande O(n).

Testerna kontrollerar listan i båda riktningarna (`backwards()`), eftersom
det vanligaste felet är att glömma en av de två pekarna. Listan ser då
rätt ut framifrån men fel bakifrån.

## 3. Deque

`Deque` lägger bara till fyra namn ovanpå den dubbellänkade listan:
`push_front`/`pop_front` arbetar vid `head`, `push_back`/`pop_back` vid
`tail`. Alla fyra är O(1).

Varför går det inte med en enkellänkad lista? För att ta bort den sista
noden måste den **näst sista** nodens `next` sättas till `None`, och den
näst sista går bara att hitta genom att gå igenom listan från början. Att
spara en pekare till den näst sista hjälper inte: efter en borttagning
behövs då den tredje sista, och så vidare. Det som behövs är en väg
bakåt från *varje* nod, alltså `prev`. (Pythons `collections.deque` löser
samma problem på ett liknande sätt.)

## 4. MinStack

Ledtråden var att varje nod kan bära lite extra information. Varje
element sparas som ett par: värdet och **det minsta värdet i stacken när
elementet lades dit**:

```python
def push(self, value):
    if self._stack.is_empty():
        smallest = value
    else:
        smallest = min(value, self._stack.peek()[1])
    self._stack.push((value, smallest))

def get_min(self):
    return self._stack.peek()[1]
```

Eftersom en stack bara ändras överst kan minimum under ett element aldrig
ändras så länge elementet ligger kvar. När det översta elementet poppas
står det rätta minimumet för resten av stacken redan sparat i elementet
under. Både `push`, `pop` och `get_min` blir O(1), mot priset av lite
extra minne per element. Lösningen återanvänder veckans `Stack` och lagrar
tupler i den.

## 5. Vänd listan på plats

```python
def reverse(self):
    previous = None
    node = self.head
    self.tail = self.head          # den gamla första blir den nya sista
    while node is not None:
        following = node.next      # spara vägen vidare
        node.next = previous       # vänd pekaren
        previous = node
        node = following
    self.head = previous           # den gamla sista blir den nya första
```

Tre variabler går fram genom listan. Den viktiga raden är `following =
node.next`: när `node.next` vänds tappar man annars vägen till resten av
listan. Inga nya noder skapas; testet kontrollerar att det är exakt samma
nodobjekt efteråt. `head` och `tail` byter plats, och testet visar att
`append` fortfarande fungerar efteråt, vilket det inte skulle göra om
`tail` glömts bort.
