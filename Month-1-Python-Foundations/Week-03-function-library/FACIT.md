# Facit vecka 3 — Prova själv

Koden finns i [`facit/prova_sjalv.py`](facit/prova_sjalv.py) och testerna
i [`tests/test_facit_prova_sjalv.py`](tests/test_facit_prova_sjalv.py).
Facit till övningarna 3.1–3.16 finns i mappen [`facit/`](facit/).

## 1. build_report

```python
def build_report(numbers: list[float], text: str) -> str:
    lines = [
        "=== Rapport ===",
        f"Medelvärde: {mean(numbers)}",
        f"Median: {median(numbers)}",
        f"Typvärde: {mode(numbers)}",
        f"Standardavvikelse: {stddev(numbers)}",
        f"Antal ord: {word_count(text)}",
        f"Palindrom: {is_palindrome(text)}",
    ]
    return "\n".join(lines)
```

Ungefär 50 rader blev 10, och varje rad säger vad den gör. All räkning
sker i funktioner som redan är testade; `build_report` sätter bara ihop
svaren. `"\n".join(lines)` sätter ihop raderna med en radbrytning (`\n`)
mellan varje.

Den viktigaste ändringen är att funktionen **returnerar** texten i stället
för att skriva ut den. Då kan testet jämföra den direkt:

```python
def test_report_matches_the_legacy_output(capsys):
    handle_data([1, 2, 2, 3, 10], "Ni talar bra latin")
    legacy = capsys.readouterr().out.rstrip("\n")
    assert build_report([1, 2, 2, 3, 10], "Ni talar bra latin") == legacy
```

`capsys` är ett verktyg i pytest som fångar det som skrivs ut, så att
testet kan läsa det. Testet visar att omskrivningen ger exakt samma
resultat som originalet. Sådana tester är det säkraste sättet att skriva
om gammal kod: först ett test som låser fast vad koden gör, sedan
omskrivningen.

## 2. variance

```python
def variance(numbers: list[float]) -> float:
    average = mean(numbers)
    total = 0
    for value in numbers:
        total = total + (value - average) ** 2
    return total / len(numbers)


def stddev(numbers: list[float]) -> float:
    return variance(numbers) ** 0.5
```

Variansen var redan en mellanräkning inne i `stddev`. Som egen funktion
får den ett namn, kan testas för sig och kan användas av den som behöver
variansen. `** 0.5` är kvadratroten (det går också att använda
`math.sqrt`). `variance` behöver ingen egen kontroll av tom lista:
`mean` kastar redan `ValueError` för den.

## 3. most_common_word

```python
def most_common_word(text: str) -> str:
    words = text.lower().split()
    if len(words) == 0:
        raise ValueError("texten innehåller inga ord")
    best = words[0]
    best_count = 0
    for word in sorted(words):
        count = words.count(word)
        if count > best_count:
            best = word
            best_count = count
    return best
```

Samma mönster som `mode` och övning 3.15, med ord i stället för tal.
`text.lower()` först gör att "Sol" och "sol" räknas som samma ord, och
`sorted(words)` gör att det ord som kommer först i bokstavsordning vinner
vid lika antal. En tom text har inget vanligaste ord, så funktionen kastar
`ValueError`, precis som `mean` för en tom lista.

## 4. modes

```python
def modes(numbers: list[float]) -> list[float]:
    if len(numbers) == 0:
        raise ValueError("modes() behöver minst ett tal")
    highest = 0
    for value in numbers:
        if numbers.count(value) > highest:
            highest = numbers.count(value)
    result = []
    for value in sorted(numbers):
        if numbers.count(value) == highest and value not in result:
            result.append(value)
    return result
```

Två varv: det första tar reda på hur många gånger det vanligaste värdet
förekommer, det andra samlar alla värden som förekommer så många gånger.
`value not in result` hindrar att samma värde läggs till flera gånger
(värdet 1 förekommer ju två gånger i `[1, 1, 2, 2]`). Lägg märke till att
returtypen ändras från ett tal till en lista. Det är skälet till att
`mode` inte ändrades: alla som anropar `mode` räknar med att få ett tal.

I vecka 4 lär du dig dictionaries, som gör det här både kortare och
snabbare.

## 5. summary

```python
def summary(numbers: list[float], decimals: int = 2) -> str:
    return (
        f"medel {round(mean(numbers), decimals)}, "
        f"median {round(median(numbers), decimals)}, "
        f"typvärde {mode(numbers)}, "
        f"standardavvikelse {round(stddev(numbers), decimals)}"
    )
```

`decimals` har standardvärdet 2, så det vanliga anropet blir
`summary(numbers)`. Parenteserna runt de fyra f-strängarna gör att Python
läser dem som en enda lång text över flera rader.

En detalj som testet visar: `round(2.5, 0)` blir `2.0`, inte `3.0`.
Python avrundar ett tal som ligger exakt mitt emellan till närmaste
**jämna** tal ("bankers avrundning"). Det gör att avrundningsfelen inte
alltid drar åt samma håll när man avrundar många tal.
