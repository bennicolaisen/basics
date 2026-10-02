# Kom igång

Kursen förutsätter att du **aldrig har programmerat**. Du behöver inte
installera allt på en gång; varje del installeras när kursen behöver den.

## Det du behöver från start

1. **Python 3.10 eller nyare** från <https://www.python.org/downloads/>.
   På Windows: kryssa i **"Add python.exe to PATH"** innan du klickar
   Install.
2. **En editor.** Vi rekommenderar
   [Visual Studio Code](https://code.visualstudio.com/) (gratis) med
   tillägget "Python".
3. **Kursen.** Klicka på den gröna knappen **Code** på kursens sida på
   GitHub, välj **Download ZIP** och packa upp filen. (Git lär du dig i
   vecka 16. Kan du det redan:
   `git clone https://github.com/bennicolaisen/basics.git`.)
4. **pytest**, verktyget som kontrollerar dina övningar. Öppna en terminal
   och skriv:

   ```bash
   python -m pip install pytest
   ```

   (På Mac heter kommandot ofta `python3` i stället för `python`.)

Vecka 1 går igenom allt det här steg för steg, med exakt vad du ska
klicka på och skriva. Börja där om något ovan känns oklart.

## Så arbetar du med en vecka

Öppna veckans mapp i VS Code (*File > Open Folder…*) och läs dess
`README.md`. Den är lektionen.

**Vecka 1–4** (på svenska) är byggda för att du ska skriva mycket kod
själv, med drygt 70 övningar som kontrolleras automatiskt:

1. Läs ett steg i genomgången.
2. Gör stegets övningar i mappen `ovningar/`. Varje fil säger vad du ska
   göra.
3. Kontrollera dina svar:

   ```bash
   python -m pytest kontroll -k 05      # bara övning 05
   python -m pytest kontroll            # alla veckans övningar
   ```

   Grönt betyder rätt. Rött talar om vad som var fel.
4. Jämför med facit i `facit/` och läs förklaringarna i `FACIT.md`.
5. Gör sedan veckans projekt och avsnittet "Prova själv".

**Vecka 5–26** (på engelska, med facit på svenska) är färdiga, fungerande
projekt som du läser, kör och bygger vidare på:

1. Läs `README.md`, särskilt *Concepts Refresher*, som är själva
   undervisningen.
2. Kör veckans tester och se dem gå igenom (kommandot står i README).
3. Läs koden med testerna bredvid.
4. Gör övningarna under **Try It Yourself**.
5. Jämför med veckans `FACIT.md`, där varje övning är löst, testad och
   förklarad.

## Om facit

Varje övning i kursen har ett facit, och facit är testat: samma `pytest`
eller `mvn test` som kör veckans tester kör också facits tester. Du kan
alltså lita på att lösningarna fungerar.

Facit är till för att **jämföra**, inte för att läsa i stället för att
försöka. Fastnar du: läs avsnittet i README igen, försök en gång till, och
titta i facit när du har ett eget försök att jämföra med. Det är i
skillnaden mellan ditt försök och facit som du lär dig mest.

## Ordlistan

Programmering har många nya ord. [`ORDLISTA.md`](ORDLISTA.md) har alla
kursens begrepp med det engelska ordet, en svensk översättning och en
förklaring, ordnade efter vecka. Öva och bli förhörd:

- **I webbläsaren:** öppna `ordlista/index.html` (glosskort och förhör).
- **I terminalen**, i kursens huvudmapp:

  ```bash
  python ordlista/ova.py --vecka 1-4
  ```

En bra vana: gör ett kort förhör på veckans ord när du är klar med
veckan, och ett på alla tidigare veckor då och då.

## Senare i kursen

- **Vecka 10–17 (Java):** det enklaste är att installera
  [IntelliJ IDEA Community](https://www.jetbrains.com/idea/download/)
  (gratis). Maven följer med, och IntelliJ kan ladda ner Java åt dig:
  *File > Project Structure > SDK > Download JDK*, välj version 17.
  [`INTELLIJ_SETUP.md`](INTELLIJ_SETUP.md) visar hur hela kursen öppnas
  som ett projekt med färdiga körkonfigurationer. Vill du köra `mvn` i
  terminalen behöver du också installera
  [Maven](https://maven.apache.org/install.html) separat.
- **Vecka 16 (Git):** installera Git från <https://git-scm.com/downloads>
  om du inte redan har det.
- **Vecka 19–26 (SQL och API:er):** inget nytt att installera. SQLite och
  webbservern finns redan i Python.

Följ tabellen i [`README.md`](README.md), en vecka i taget. Ta den tid du
behöver: det är bättre att en vecka tar två än att du går vidare med
luckor.
