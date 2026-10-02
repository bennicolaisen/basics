# Facit vecka 4 — Prova själv

Koden finns i [`facit/prova_sjalv.py`](facit/prova_sjalv.py) och testerna
i [`tests/test_facit_prova_sjalv.py`](tests/test_facit_prova_sjalv.py).
Facit till övningarna 4.1–4.18 finns i mappen [`facit/`](facit/).

## 1. Skiljetecken bara i kanterna

```python
def tokenize_keep_inner(text: str) -> list[str]:
    words = [word.strip(string.punctuation) for word in text.lower().split()]
    return [word for word in words if word != ""]
```

Ordningen är omvänd mot `tokenize`: först delas texten i ord, sedan
städas varje ord. `.strip()` med ett argument tar bort de angivna tecknen
i **början och slutet**, men inte inuti, så `"don't"` klarar sig medan
`"(nu)!"` blir `"nu"`. Ett "ord" som bara bestod av skiljetecken (som
`"-"`) blir tom text, och den andra comprehensionen filtrerar bort det.

Vilken variant är bäst beror på vad texten ska användas till. För svenska
gör det sällan skillnad; för engelska, där apostrofer är vanliga, är den
nya varianten oftast bättre.

## 2. Ordpar

```python
def bigrams(tokens: list[str]) -> list[tuple[str, str]]:
    return [(tokens[i], tokens[i + 1]) for i in range(len(tokens) - 1)]


def most_common_bigram(tokens: list[str]) -> tuple[str, str]:
    pairs = bigrams(tokens)
    if len(pairs) == 0:
        raise ValueError("det behövs minst två ord för att bilda ett par")
    frequencies = analyzer.word_frequencies(pairs)
    return analyzer.top_n_words(frequencies, 1)[0][0]
```

`range(len(tokens) - 1)` slutar ett steg tidigare än vanligt, eftersom
det sista ordet inte har något ord efter sig.

Det fina är att `word_frequencies` och `top_n_words` fungerar för par
utan att ändras. `word_frequencies` räknar vad som helst som kan vara
nyckel i en dictionary, och tupler kan det. Sorteringsnyckeln `(-count,
pair)` jämför tupler med tupler, vilket också fungerar. Det är vinsten
med funktioner som inte gör fler antaganden än de behöver.

`[0][0]` betyder "första tupeln i listan, och första värdet i den", alltså
paret utan antalet.

## 3. Stoppord

```python
def top_n_words_without(frequencies, n, stopwords):
    kept = {word: count for word, count in frequencies.items() if word not in stopwords}
    return analyzer.top_n_words(kept, n)
```

En dictionary comprehension med villkor bygger en ny dictionary utan
stopporden; sedan gör den befintliga funktionen resten. Stopporden kommer
som en **mängd** eftersom `word not in stopwords` är snabbt för mängder,
även med hundratals ord.

## 4. Genomsnittlig ordlängd

```python
def average_word_length(tokens: list[str]) -> float:
    if len(tokens) == 0:
        raise ValueError("det finns inga ord att räkna på")
    return sum([len(token) for token in tokens]) / len(tokens)
```

Facit räknar på **alla** ord, med upprepningar. Det svarar på frågan "hur
långa är orden man läser i texten?", där ett ord som förekommer tio
gånger också läses tio gånger. Räknat på unika ord svarar det i stället på
"hur långa är orden i ordförrådet?". Testet visar skillnaden:

```python
# "a" tre gånger och "bbb" en gång: (1 + 1 + 1 + 3) / 4 = 1.5.
# Räknat på unika ord hade svaret blivit (1 + 3) / 2 = 2.0.
assert average_word_length(["a", "a", "a", "bbb"]) == pytest.approx(1.5)
```

Det viktiga är inte vilket val man gör, utan att valet står i
dokumentationen och låses fast av ett test.

## 5. Kontrollera n

```python
def _check_n(n: int) -> None:
    if n <= 0:
        raise ValueError(f"n måste vara minst 1, fick {n}")


def top_n_words(frequencies, n):
    _check_n(n)
    return analyzer.top_n_words(frequencies, n)
```

Kontrollen ligger i en egen liten funktion, eftersom två funktioner
behöver den. Understrecket först i namnet är en vana i Python som betyder
"intern hjälpfunktion, inte tänkt att användas utifrån".

Utan kontrollen ger `top_n_words(freqs, 0)` en tom lista, och
`top_n_words(freqs, -1)` ger alla utom det sista, eftersom `[:-1]` är
slicing från slutet. Ingen av dem är ett rimligt svar på frågan "de -1
vanligaste orden", så ett tydligt fel är bättre.
