# Basics — programmering från noll till databaser och API:er

## Vem kursen är för

Kursen börjar från början och förutsätter **ingen erfarenhet alls av
programmering**. Första veckan installerar du Python och skriver ditt
första program; sista veckan bygger du ett eget webb-API med en databas
bakom. Inget hoppas över som "för enkelt".

Den passar lika bra för den som har programmerat förut men känner att
grunderna har blivit osäkra: läs då README-filerna snabbare, och använd
övningarna och facit för att hitta luckorna.

Kursen är sex månader, ett projekt i veckan:

| Månad | Vecka | Del |
|---|---|---|
| 1–4 | 1–18 | Programmeringens grunder: Python, datastrukturer, objektorientering, Java, testning, felsökning, Git och ett slutprojekt |
| 5 | 19–24 | Databaser och SQL, i tre nivåer: nybörjare, mellannivå, avancerad |
| 6 | 25–26 | Webb-API:er: först att anropa ett, sedan att bygga ett på din egen databas |

**Ny här?** Börja med [`GETTING_STARTED.md`](GETTING_STARTED.md): vad du
installerar, hur du arbetar med en vecka och hur facit och ordlistan
används.

## Språk

- **Vecka 1–4 är på svenska**, skrivna för den som aldrig har
  programmerat. Varje engelskt begrepp förklaras när det dyker upp.
- **Vecka 5–26 är på engelska**, med **facit på svenska**. Det är
  medvetet: programmeringens ord är engelska, i koden, i dokumentation och
  i sökresultat. Efter vecka 4 har du orden som behövs för att läsa
  vidare.
- **[Ordlistan](ORDLISTA.md)** har alla 278 begrepp i kursen: det
  engelska ordet, en svensk översättning och en förklaring, ordnade efter
  vecka. Du kan öva på dem och bli förhörd, i webbläsaren
  (`ordlista/index.html`) eller i terminalen (`python ordlista/ova.py`).

## Hur kursen är byggd

**Vecka 1–4** är lektioner i små steg. Efter varje steg kommer övningar
i mappen `ovningar/` som du löser själv och kontrollerar automatiskt med
`python -m pytest kontroll`. Varje vecka avslutas med ett litet projekt
som använder allt du lärt dig, och med extra övningar ("Prova själv").
Totalt drygt 60 kontrollerade övningar, alla med facit. Kontrollerna
provar fler fall än exemplen i uppgiften, så det räcker inte att klara
exemplet.

**Vecka 5–26** är **kompletta, fungerande projekt**, inte tomma uppgifter
med bitar som saknas. Du laddar ner, kör, läser koden, kör testerna och
ser dem gå igenom. Varje veckas `README.md` har samma delar:

- **Purpose** — varför ämnet är viktigt.
- **Objectives** — vad koden konkret visar.
- **Concepts Refresher** — själva undervisningen, förklarad från grunden.
- **Design & Architecture** — hur koden är uppdelad och varför.
- **How to Build & Run** — exakta kommandon.
- **Testing** — vad testerna täcker och hur de körs.
- **Try It Yourself** — 3–5 övningar som bygger vidare på veckans kod.

**Varje övning har facit.** I varje vecka finns en `FACIT.md` på
svenska som löser varje övning och förklarar hur man tänker, inklusive
vanliga fel och varför ett annat sätt hade varit sämre. Lösningarna finns
också som körbar kod (i `facit/`, eller i ett `facit`-paket i
Java-veckorna) med egna tester, som körs tillsammans med veckans tester.
Facit är alltså kontrollerat, inte bara skrivet.

## Det du behöver

- **Python 3.10+** (vecka 1–9 och 19–26) och `pytest`. Inga andra
  paket: databaserna och webbservrarna i månad 5–6 använder det som
  redan följer med Python (`sqlite3`, `http.server`, `urllib`).
- **En editor**, till exempel Visual Studio Code (gratis).
- **Java 17** och **Maven** (vecka 10–17). Enklast via IntelliJ IDEA
  Community, se [`INTELLIJ_SETUP.md`](INTELLIJ_SETUP.md).

## Tempo

Tjugosex veckor, ett projekt i veckan. Det är en plan, inte ett krav: gå
långsammare på veckor som visar en verklig lucka. Behöver du korta ned
är veckorna som knyter ihop en månad (4, 8, 12, 17, 24 och 26) de som är
minst lämpliga att hoppa över.

Vecka 18 är halvvägs: där slutar grunderna och databaserna och API:erna
börjar. SQL-veckorna är tre nivåer om två veckor (19–20, 21–22, 23–24),
så om tiden tar slut kan du stanna efter vilken nivå som helst med en
användbar kunskap, och ändå göra API-veckorna i månad 6, som bara kräver
nivå 1–2.

## Kursplan

### Månad 1 — Grunderna i Python (på svenska)
*Från ingenting till att skriva egna program: variabler, villkor, loopar,
funktioner och samlingar av data.*

| Vecka | Projekt | Ämne |
|---|---|---|
| 1 | [`01-unit-converter-toolkit`](Month-1-Python-Foundations/Week-01-unit-converter-toolkit/) | Grunderna: `print`, felmeddelanden, variabler och typer, räkning, text och slicing, funktioner, tester |
| 2 | [`02-input-validators-and-games`](Month-1-Python-Foundations/Week-02-input-validators-and-games/) | Villkor och loopar: `if`/`elif`/`else`, `while`, `for`, `break` |
| 3 | [`03-function-library`](Month-1-Python-Foundations/Week-03-function-library/) | Funktioner på riktigt: parametrar, returvärden, räckvidd, att dela upp ett program |
| 4 | [`04-text-analyzer`](Month-1-Python-Foundations/Week-04-text-analyzer/) | Samlingar: `list`, `dict`, `set`, `tuple`, comprehensions |

### Månad 2 — Rekursion och datastrukturer (Python)
*Två saker som ofta förklarar "jag förstod det en gång men inte nu":
rekursion, och vad en datastruktur egentligen är.*

| Vecka | Projekt | Ämne |
|---|---|---|
| 5 | [`05-recursion-basics`](Month-2-Recursion-and-Data-Structures/Week-05-recursion-basics/) | Rekursion I: basfall, rekursionsfall, anropsstacken |
| 6 | [`06-backtracking-puzzles`](Month-2-Recursion-and-Data-Structures/Week-06-backtracking-puzzles/) | Rekursion II: backtracking, sök och ångra |
| 7 | [`07-diy-data-structures`](Month-2-Recursion-and-Data-Structures/Week-07-diy-data-structures/) | Bygg en länkad lista, en stack och en kö från grunden |
| 8 | [`08-search-and-sort`](Month-2-Recursion-and-Data-Structures/Week-08-search-and-sort/) | Sökning, sortering och en känsla för Big-O |

### Månad 3 — Objektorientering och steget till Java
*Från "ett program är en följd av steg" till "ett program är objekt som
samarbetar", och från Pythons dynamiska typer till Javas statiska,
kompilerade värld.*

| Vecka | Projekt | Ämne |
|---|---|---|
| 9 | [`09-oop-bank-simulation`](Month-3-OOP-and-Java-Bridge/Week-09-oop-bank-simulation/) | OOP i Python: klasser, inkapsling, komposition |
| 10 | [`10-java-bridge`](Month-3-OOP-and-Java-Bridge/Week-10-java-bridge/) | Bron till Java: statiska typer, kompilering, Maven, `main` |
| 11 | [`11-java-oop-shapes`](Month-3-OOP-and-Java-Bridge/Week-11-java-oop-shapes/) | OOP i Java: interface, abstrakta klasser, arv, polymorfism |
| 12 | [`12-java-collections-catalog`](Month-3-OOP-and-Java-Bridge/Week-12-java-collections-catalog/) | Collections Framework, generics, `Comparable`/`Comparator` |

### Månad 4 — Testning, felsökning, Git och slutprojekt
*Vanorna runt koden: att testa den, felsöka den när den är fel och
samarbeta kring den, plus ett slutprojekt som knyter ihop månad 1–4.*

| Vecka | Projekt | Ämne |
|---|---|---|
| 13 | [`13-java-exceptions-parser`](Month-4-Testing-Debugging-and-Capstone/Week-13-java-exceptions-parser/) | Undantag, defensiv programmering, tålig inläsning |
| 14 | [`14-java-junit-testing`](Month-4-Testing-Debugging-and-Capstone/Week-14-java-junit-testing/) | JUnit 5 på djupet, testdriven utveckling (TDD) |
| 15 | [`15-debugging-clinic`](Month-4-Testing-Debugging-and-Capstone/Week-15-debugging-clinic/) | Systematisk felsökning: stackspår, brytpunkter, halvering |
| 16 | [`16-git-workflow-lab`](Month-4-Testing-Debugging-and-Capstone/Week-16-git-workflow-lab/) | Git: grenar, sammanslagningar, konflikter, pull requests |
| 17–18 | [`17-capstone-library-system`](Month-4-Testing-Debugging-and-Capstone/Week-17-capstone-library-system/) | Slutprojekt: ett komplett bibliotekssystem |

### Månad 5 — Databaser och SQL (Python + SQLite)
*Från "datan ligger i en lista" till "datan ligger i en databas": ställa
frågor till den, kombinera den, ändra den säkert, analysera den och låta
databasen själv upprätthålla reglerna. Allt på samma data om nordiskt
väder, och i nivå 3 en butik som säljer väderutrustning. För snabb
övning med direkt återkoppling, öppna
[`sql-playground/index.html`](Month-5-Databases-and-SQL/sql-playground/index.html)
i en webbläsare.*

| Vecka | Nivå | Projekt | Ämne |
|---|---|---|---|
| 19 | 1 · Nybörjare | [`19-sql-select-basics`](Month-5-Databases-and-SQL/Week-19-sql-select-basics/) | `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, `NULL` |
| 20 | 1 · Nybörjare | [`20-sql-aggregates-and-grouping`](Month-5-Databases-and-SQL/Week-20-sql-aggregates-and-grouping/) | Sammanställningar, `GROUP BY`, `HAVING` |
| 21 | 2 · Mellannivå | [`21-sql-joins-and-keys`](Month-5-Databases-and-SQL/Week-21-sql-joins-and-keys/) | Nycklar, normalisering, `JOIN`, `LEFT JOIN`, subqueries |
| 22 | 2 · Mellannivå | [`22-sqlite-weather-log`](Month-5-Databases-and-SQL/Week-22-sqlite-weather-log/) | Skriva data från Python: regler i schemat, transaktioner, parametrar |
| 23 | 3 · Avancerad | [`23-sql-analytics-and-window-functions`](Month-5-Databases-and-SQL/Week-23-sql-analytics-and-window-functions/) | Analys: CTE:er, fönsterfunktioner, `EXISTS`, fan-out-fällan |
| 24 | 3 · Avancerad | [`24-sql-business-logic`](Month-5-Databases-and-SQL/Week-24-sql-business-logic/) | Affärslogik i databasen: triggrar, vyer, upserts |

### Månad 6 — Webb-API:er (Python)
*Hur program pratar med varandra över nätet: först som klient som
anropar någon annans API, sedan som server, med vecka 22:s väderlogg
bakom.*

| Vecka | Projekt | Ämne |
|---|---|---|
| 25 | [`25-how-apis-work`](Month-6-APIs/Week-25-how-apis-work/) | HTTP, JSON, statuskoder, att anropa ett API från Python |
| 26 | [`26-build-a-rest-api`](Month-6-APIs/Week-26-build-a-rest-api/) | Bygga ett REST-API: routing, validering, statuskoder |

## Vart det leder

Halvvägs, efter vecka 18, är en bra kontroll att läsa om *Concepts
Refresher* i månad 1–3 och genomgångarna i vecka 1–4. Känns de som
påminnelser snarare än nytt stoff har grunderna fastnat. Gör också ett
förhör på hela ordlistan fram till vecka 18.

Efter vecka 26 har du delarna som de flesta riktiga program består av:
en databas, SQL för att ställa frågor till den och skydda den, och ett
API framför. Ett bra nästa projekt är att sätta ihop dem själv, till
exempel en väderapp som hämtar prognoser från ett öppet API, sparar dem
i SQLite och erbjuder ett eget API med sammanfattningar.
