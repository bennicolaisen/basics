# Facit vecka 6 — Try It Yourself

Koden finns i [`facit/prova_sjalv.py`](facit/prova_sjalv.py) och testerna
i [`tests/test_facit.py`](tests/test_facit.py). Kör dem med
`python -m pytest` i veckans mapp.

Alla fem lösningarna har samma form som veckans kod: **välj** något, **gå
vidare** rekursivt, och **ångra** valet om det inte ledde till en lösning.
Skillnaderna ligger i vad man väljer, när man slutar och vad som ångras.

## 1. Kortaste vägen i labyrinten

Ledtråden i uppgiften är frågan om djupet-först-sökning (DFS) hittar den
kortaste vägen. Svaret är **nej**. DFS följer en väg så långt det går och
nöjer sig med den första väg som når fram. Vilken det blir beror på i
vilken ordning grannarna prövas, inte på hur lång vägen är. Testet visar
ett fall: i ett öppet 2×3-rutnät från `(0, 0)` till `(0, 2)` provar
`solve_maze` "ner" före "höger" och hittar en väg på 4 steg, fast den
kortaste är 2.

Att räkna stegen i `solve_maze`s svar räcker alltså inte. Lösningen är
**bredden-först-sökning** (BFS): utforska alla rutor 1 steg bort, sedan
alla 2 steg bort, och så vidare. Första gången målet nås har man då
garanterat gått kortaste vägen.

```python
def shortest_path_length(grid, start, end):
    _validate(grid, start, end)
    distance = {start: 0}
    queue = deque([start])
    while queue:
        cell = queue.popleft()
        if cell == end:
            return distance[cell]
        for d_row, d_col in MOVES:
            neighbor = (cell[0] + d_row, cell[1] + d_col)
            if _is_open(grid, neighbor) and neighbor not in distance:
                distance[neighbor] = distance[cell] + 1
                queue.append(neighbor)
    return None
```

BFS använder en **kö** (först in, först ut) i stället för rekursion:
rutorna tas om hand i den ordning de upptäcktes, och därmed i ordning
efter avstånd. `deque` från modulen `collections` är Pythons snabba kö;
vecka 7 handlar om hur köer fungerar inuti. `distance` är både facit över
avstånden och listan över besökta rutor. `solve_maze` lämnas orörd.

## 2. N damer

Placera en dam per rad, och pröva varje kolumn i tur och ordning:

```python
def place(row):
    if row == n:
        return True               # alla rader har en dam: klart
    for col in range(n):
        if is_safe(col):
            queens.append(col)    # välj
            if place(row + 1):    # gå vidare
                return True
            queens.pop()          # ångra
    return False
```

Genom att placera exakt en dam per rad kan två damer aldrig hamna på samma
rad, så `is_safe` behöver bara pröva kolumner och diagonaler. Två damer
står på samma diagonal när avståndet i kolumner är lika stort som
avståndet i rader: `abs(other_col - col) == row - other_row`.

Svaret är en lista där index är raden och värdet kolumnen; för n = 4 blir
det `[1, 3, 0, 2]`. För n = 2 och n = 3 finns ingen lösning, och då
returneras `None`. För n = 0 är den tomma placeringen en giltig lösning.

## 3. Alla vägar genom labyrinten

Två saker ändras jämfört med `solve_maze`:

- Sökningen **slutar inte** vid målet. När en väg når fram sparas en kopia
  av den (`paths.append(list(path))`), och sökningen fortsätter.
- Markeringen av besökta rutor **ångras** också. I `solve_maze` står en
  ruta kvar i `visited` för alltid, eftersom en ruta som en gång lett till
  en återvändsgränd aldrig behöver prövas igen. Men när man vill hitta
  *alla* vägar får en ruta som hörde till en väg mycket väl ingå i en
  annan. Därför markerar lösningen bara rutorna på den *nuvarande* vägen
  (`on_path`) och tar bort markeringen på vägen tillbaka.

```python
path.append(cell)
on_path.add(cell)
if cell == end:
    paths.append(list(path))
else:
    for d_row, d_col in MOVES:
        explore((cell[0] + d_row, cell[1] + d_col))
path.pop()
on_path.remove(cell)
```

`list(path)` gör en kopia; utan den skulle alla sparade vägar vara samma
lista, som till slut är tom. Antalet vägar växer mycket snabbt: redan ett
öppet 3×3-rutnät har 12 vägar mellan två hörn.

## 4. Delmängden själv, inte bara ja eller nej

```python
chosen.append(nums[index])                       # pröva att ta med talet
if backtrack(index + 1, remaining - nums[index]):
    return True
chosen.pop()                                     # ångra
return backtrack(index + 1, remaining)           # pröva utan talet
```

Samma sökning som `has_subset_sum`, med en lista `chosen` som följer med
valen. Det enda nya är att valet att ta med ett tal måste **ångras** innan
man prövar att låta bli, annars ligger talet kvar i listan. När sökningen
lyckas innehåller `chosen` exakt de valda talen.

## 5. Permutationer av en viss längd

```python
def partial_permutations(lst, k):
    if k == 0:
        return [[]]
    result = []
    for i in range(len(lst)):
        rest = lst[:i] + lst[i + 1:]
        for tail in partial_permutations(rest, k - 1):
            result.append([lst[i]] + tail)
    return result
```

Det här är `all_permutations` med ett annat basfall: i stället för att
fortsätta tills listan är tom slutar rekursionen när `k` element har
valts. Ett ordnat urval av k element är "välj det första, och sedan ett
ordnat urval av k − 1 bland resten". Antalet blir n! / (n − k)!, till
exempel 12 för 2 av 4. Eftersom inga permutationer längre än k byggs
slösas inget arbete på att skapa fullständiga permutationer och sedan
korta dem.
