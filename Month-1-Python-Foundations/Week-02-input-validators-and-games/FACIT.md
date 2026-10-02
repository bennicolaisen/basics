# Facit vecka 2 — Prova själv

Koden finns i [`facit/prova_sjalv.py`](facit/prova_sjalv.py) och testerna
i [`tests/test_facit_prova_sjalv.py`](tests/test_facit_prova_sjalv.py).
Facit till övningarna 2.1–2.18 finns i mappen [`facit/`](facit/).

## 1. is_valid_email

```python
def is_valid_email(text):
    if " " in text or text.count("@") != 1:
        return False
    at = text.index("@")
    local = text[:at]
    domain = text[at + 1:]
    if local == "":
        return False
    if "." not in domain:
        return False
    if domain.startswith(".") or domain.endswith("."):
        return False
    return True
```

Samma mönster som `is_valid_username`: pröva en regel i taget och
returnera `False` så fort en regel bryts. Om alla prövningar passerats är
adressen godkänd.

- `text.index("@")` ger platsen för `@`. Slicing delar texten i delen
  före (`text[:at]`) och efter (`text[at + 1:]`); `+ 1` hoppar över
  själva `@`.
- `.startswith(".")` och `.endswith(".")` är textmetoder som svarar
  `True` eller `False`.

Bra tester tar en regel i taget och bryter bara den: `"alva@@example.se"`
(två @), `"@example.se"` (inget före), `"alva@examplese"` (ingen punkt),
`"alva@.se"` och `"alva@example."` (punkt på fel ställe), och en adress
med mellanslag. Riktiga e-postadresser följer en mycket krångligare
standard; i verkliga program kontrollerar man oftast bara grovt, och
skickar sedan ett e-brev för att se att adressen fungerar.

## 2. En ogiltig gissning kostar ett försök

Ändringen är att gissningen inte längre läses med `ask_for_guess` (som
frågar tills svaret är giltigt), utan direkt i `for`-loopen, en gång per
varv:

```python
for attempt in range(1, max_attempts + 1):
    remaining = max_attempts - attempt
    text = input(f"Gissa ett tal mellan {low} och {high}: ")
    try:
        guess = parse_int_in_range(text, low, high)
    except ValueError as error:
        print(f"Ogiltig gissning ({error}). Det kostade ett försök. {remaining} försök kvar.")
        continue
    ...
```

`continue` hoppar till nästa varv, och eftersom varje varv är ett försök
har försöket gått åt. `except ValueError as error` sparar felet i
variabeln `error`, så att meddelandet från `parse_int_in_range` ("'hej'
är inte ett heltal" eller "500 ligger utanför 1–10") kan visas för
spelaren. Det talar om vilken sorts fel det var.

## 3. Svårighetsmeny

```python
while True:
    level = input("Välj svårighet (lätt/medel/svår): ").strip().lower()
    if level == "lätt":
        high = 10
        attempts = 5
        break
    elif level == "medel":
        ...
    print("Skriv lätt, medel eller svår.")

secret = random.randint(1, high)
return play_game(secret, 1, high, attempts)
```

`play_game` ändras inte alls: den tar redan intervall och antal försök som
parametrar. Menyn bestämmer bara vilka värden som skickas in. Det är
vinsten med parametrar i stället för fasta värden inne i funktionen.

`.strip().lower()` gör att `" Lätt "` också godtas. Metoderna anropas i
tur och ordning: först tas mellanslagen bort, sedan görs bokstäverna små.

## 4. count_valid_usernames

```python
def count_valid_usernames(candidates):
    count = 0
    for candidate in candidates:
        if is_valid_username(candidate):
            count = count + 1
    return count
```

Samla-ihop-mönstret från steg 4: en räknare som börjar på 0 och ökar i
loopen. Funktionen återanvänder `is_valid_username` i stället för att
upprepa reglerna. I vecka 4 lär du dig skriva samma sak på en rad med en
*comprehension*.

## 5. Spela igen

```python
wins = 0
losses = 0
while True:
    if play_game(random.randint(LOW, HIGH), LOW, HIGH, MAX_ATTEMPTS):
        wins = wins + 1
    else:
        losses = losses + 1
    print(f"Vinster: {wins}, förluster: {losses}")
    again = input("Spela igen? (j/n) ").strip().lower()
    if again != "j":
        break
return wins, losses
```

`play_game` returnerar `True` eller `False`, så anropet kan stå direkt i
`if`. Räknarna skapas **före** loopen; skapades de inuti skulle de börja
om från 0 varje omgång. `return wins, losses` lämnar tillbaka två värden
på en gång (en *tupel*, som du lär dig mer om i vecka 4); testet använder
det för att kontrollera ställningen.

Testerna för 3 och 5 ersätter `random.randint` med en funktion som alltid
ger samma tal, så att spelets svar är känt i förväg.
