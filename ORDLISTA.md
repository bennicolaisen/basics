# Ordlista

Alla ord och begrepp i kursen, med det engelska ordet (som står i koden
och i de flesta böcker och sökresultat), en svensk översättning och en
förklaring. Orden är ordnade efter den del av kursen där de först dyker
upp.

## Öva och bli förhörd

**I webbläsaren:** öppna [`ordlista/index.html`](ordlista/index.html).
Där kan du läsa orden, öva med glosskort och göra förhör. Sidan kommer
ihåg vilka ord du kan.

**I terminalen** (i kursens huvudmapp):

```
python ordlista/ova.py                      # 10 frågor från hela kursen
python ordlista/ova.py --vecka 1-4          # bara orden från vecka 1–4
python ordlista/ova.py --antal 20 --typ skriv
python ordlista/ova.py --lista --vecka 2    # visa veckans glosor
```

Förhöret blandar två sorters frågor: antingen får du förklaringen och
skriver det engelska ordet, eller så får du ordet och väljer rätt
förklaring av fyra. Efteråt ser du vilka ord du missade och kan öva på
dem direkt.


## Python-grunder (vecka 1–4)

| Engelska | Svenska | Förklaring | Vecka |
|---|---|---|---|
| **argument** | argument | Det värde som skickas in till en funktion när den anropas. | 1 |
| **assert** | påstå | Nyckelord som kontrollerar att något är sant; annars stoppas programmet eller testet misslyckas. Exempel: `assert double(4) == 8` | 1 |
| **assignment** | tilldelning | Att spara ett värde i en variabel med =. Exempel: `antal = 3` | 1 |
| **boolean** | sanningsvärde | Värdet True (sant) eller False (falskt); typen heter bool. | 1 |
| **bug** | bugg | Ett fel i ett program som gör att det inte beter sig som det ska. | 1 |
| **call** | anrop | Att köra en funktion, genom att skriva dess namn följt av parenteser. Exempel: `double(4)` | 1 |
| **comment** | kommentar | Text efter # som Python hoppar över; används för att förklara koden för människor. Exempel: `# Det här är en kommentar` | 1 |
| **constant** | konstant | Ett värde som inte ska ändras; skrivs med stora bokstäver i Python. Exempel: `KM_PER_MILE = 1.609344` | 1 |
| **data type** | datatyp | Vilken sorts värde något är, till exempel heltal, decimaltal eller text; typen avgör vad man kan göra med värdet. | 1 |
| **define** | definiera | Att skapa något, till exempel en funktion med def. Exempel: `def double(x):` | 1 |
| **docstring** | dokumentationssträng | En text inom """ först i en funktion som förklarar vad den gör. | 1 |
| **error message** | felmeddelande | Pythons beskrivning av vad som gick fel och var; läses nerifrån och upp. | 1 |
| **expression** | uttryck | Kod som räknas ut till ett värde, till exempel 2 + 3 eller len(namn). | 1 |
| **f-string** | f-sträng | En text med f framför citattecknet, där uttryck inom { } byts ut mot sina värden. Exempel: `f"Hej, {namn}!"` | 1 |
| **float** | flyttal (decimaltal) | Ett tal med decimaler; typen heter float. Python skriver decimaler med punkt. Exempel: `3.14` | 1 |
| **function** | funktion | En namngiven bit kod som kan anropas många gånger och ofta returnerar ett värde. | 1 |
| **indentation** | indrag | Mellanslagen i början av en rad; i Python visar de vilka rader som hör till en funktion, en if eller en loop. | 1 |
| **input** | inmatning | Det användaren skriver in; funktionen input() väntar på det och ger tillbaka det som text. | 1 |
| **integer** | heltal | Ett tal utan decimaler; typen heter int i Python. Exempel: `42` | 1 |
| **integer division** | heltalsdivision | Division som bara ger hela gånger, utan rest; skrivs // i Python. Exempel: `7 // 2  # 3` | 1 |
| **interpreter** | tolk | Programmet som läser och kör Python-kod rad för rad; det är det som startar när du skriver python. | 1 |
| **modulo** | modulo (rest) | Resten vid heltalsdivision; skrivs % i Python. Exempel: `7 % 2  # 1` | 1 |
| **operator** | operator | Ett tecken som utför en operation på värden, till exempel + eller ==. | 1 |
| **parameter** | parameter | Namnet i funktionsdefinitionen på ett värde som funktionen tar emot. | 1 |
| **print** | skriva ut | Inbyggd funktion som visar text på skärmen. Exempel: `print("Hej!")` | 1 |
| **program** | program | En följd av instruktioner som datorn utför, i Python skrivna i en textfil som slutar på .py. | 1 |
| **pytest** | pytest | Verktyget som letar upp och kör alla testfunktioner vars namn börjar med test_. | 1 |
| **return** | returnera | Att lämna tillbaka ett värde från en funktion och avsluta den. | 1 |
| **return value** | returvärde | Det värde som en funktion lämnar tillbaka med return. | 1 |
| **shell** | skal (interaktivt läge) | Pythons interaktiva läge med prompten >>>, där varje rad körs direkt. | 1 |
| **snake_case** | snake_case | Sättet att namnge variabler och funktioner i Python: små bokstäver med understreck mellan orden. Exempel: `antal_personer` | 1 |
| **source code** | källkod | Den text som programmeraren skriver och som datorn sedan kör. | 1 |
| **string** | sträng (text) | En text, skriven inom citattecken; typen heter str. Exempel: `"Kiruna"` | 1 |
| **syntax** | syntax | Reglerna för hur kod måste skrivas för att språket ska förstå den. | 1 |
| **syntax error** | syntaxfel | Fel som uppstår när koden bryter mot språkets regler, till exempel ett saknat citattecken. | 1 |
| **terminal** | terminal | Ett fönster där man styr datorn genom att skriva kommandon i stället för att klicka. | 1 |
| **test** | test | Kod som kontrollerar att annan kod gör rätt. | 1 |
| **traceback** | spårutskrift | Den del av ett felmeddelande som visar vilka rader och funktionsanrop som ledde fram till felet. | 1 |
| **type conversion** | typomvandling | Att göra om ett värde till en annan typ, till exempel text till tal med int(). Exempel: `int("42")` | 1 |
| **value** | värde | En bit data, till exempel talet 42 eller texten "Kiruna". | 1 |
| **variable** | variabel | Ett namn som pekar på ett värde, ungefär som en etikett på en låda. Exempel: `temperatur = -3` | 1 |
| **break** | avbryta | Nyckelord som hoppar ut ur en loop direkt. | 2 |
| **comparison** | jämförelse | Att jämföra två värden med till exempel ==, < eller >=; resultatet blir True eller False. | 2 |
| **condition** | villkor | Ett uttryck som är sant eller falskt och som avgör vad programmet gör. | 2 |
| **continue** | fortsätta | Nyckelord som hoppar direkt till nästa varv i en loop. | 2 |
| **edge case** | gränsfall | Ett fall precis vid en gräns eller i en ytterkant, som en tom lista; där sitter felen ofta. | 2 |
| **exception** | undantag | Ett fel som uppstår medan programmet körs och som kan fångas med try och except. | 2 |
| **for loop** | for-loop | En loop som går igenom något, ett värde i taget, till exempel varje tecken i en text. | 2 |
| **if statement** | if-sats | Kod som bara körs om ett villkor är sant; elif och else anger andra fall. | 2 |
| **index** | index | Ett värdes plats i en lista eller text; börjar på 0. | 2 |
| **IndexError** | indexfel | Undantag när man hämtar ett index som inte finns i en lista. | 2 |
| **infinite loop** | oändlig loop | En loop som aldrig tar slut; avbryts i terminalen med Ctrl+C. | 2 |
| **iteration** | iteration (varv) | Ett varv i en loop, eller att gå igenom något ett värde i taget. | 2 |
| **list** | lista | En samling värden i en bestämd ordning, som kan ändras. Exempel: `[3, 1, 2]` | 2 |
| **logical operator** | logisk operator | Orden and, or och not, som kombinerar eller vänder på villkor. | 2 |
| **loop** | loop (slinga) | Kod som upprepas flera gånger. | 2 |
| **method** | metod | En funktion som hör till ett objekt och anropas med punkt, till exempel text.upper(). | 2 |
| **off-by-one error** | ett-fel | Ett vanligt fel där man räknar ett för mycket eller ett för lite, till exempel med range. | 2 |
| **raise** | kasta (ett fel) | Att själv utlösa ett undantag, till exempel när en funktion fått ett ogiltigt värde. Exempel: `raise ValueError("listan är tom")` | 2 |
| **random** | slump | Modulen random ger slumptal, till exempel random.randint(1, 6). | 2 |
| **range** | intervall | Inbyggd funktion som ger en följd av heltal; slutet räknas inte med. Exempel: `range(1, 4)  # 1, 2, 3` | 2 |
| **slicing** | utsnitt | Att plocka ut en del av en lista eller text med [start:slut]. Exempel: `"Göteborg"[0:4]  # "Göte"` | 2 |
| **try/except** | fånga fel | Kod som provar något i try och hanterar ett visst fel i except i stället för att krascha. | 2 |
| **validation** | validering | Att kontrollera att indata är giltiga innan de används. | 2 |
| **ValueError** | värdefel | Undantag när ett värde har rätt typ men inte går att använda, som int("sju"). | 2 |
| **while loop** | while-loop | En loop som upprepas så länge ett villkor är sant. | 2 |
| **decomposition** | uppdelning | Att dela upp ett stort problem i mindre delar, ofta funktioner. | 3 |
| **default value** | standardvärde | Ett värde som en parameter får om anroparen inte skickar något. Exempel: `def greet(name, greeting="Hej"):` | 3 |
| **global variable** | global variabel | En variabel som skapas utanför alla funktioner och syns i hela filen. | 3 |
| **import** | importera | Att hämta in kod från en annan modul så att den kan användas. Exempel: `from math import pi` | 3 |
| **keyword argument** | namngivet argument | Ett argument som skickas med parameterns namn. Exempel: `round(x, ndigits=2)` | 3 |
| **local variable** | lokal variabel | En variabel som skapas i en funktion och bara finns medan funktionen körs. | 3 |
| **module** | modul | En Python-fil vars kod kan användas från andra filer med import. | 3 |
| **None** | inget värde | Pythons värde för "ingenting"; det en funktion utan return returnerar. | 3 |
| **package** | paket | En mapp med moduler som hör ihop. | 3 |
| **positional argument** | positionellt argument | Ett argument som kopplas till en parameter efter sin plats i anropet. | 3 |
| **refactoring** | omstrukturering | Att skriva om kod så att den blir bättre utan att ändra vad den gör. | 3 |
| **scope** | räckvidd | Den del av programmet där en variabel finns och kan användas. | 3 |
| **standard library** | standardbibliotek | De moduler som följer med Python, som math, random och sqlite3. | 3 |
| **type hint** | typannotering | En notering om vilken typ en parameter eller ett returvärde har; Python kontrollerar den inte när programmet körs. Exempel: `def mean(numbers: list[float]) -> float:` | 3 |
| **unit test** | enhetstest | Ett test som kontrollerar en liten del av programmet, ofta en enda funktion. | 3 |
| **attribute** | attribut | Ett värde som hör till ett objekt, som self.width. | 4 |
| **class** | klass | En ritning för en egen datatyp, som samlar data och de metoder som hör till den. | 4 |
| **collection** | samling | En datatyp som håller många värden: lista, tupel, dictionary eller mängd. | 4 |
| **command-line argument** | kommandoradsargument | Ett ord som skrivs efter programnamnet i terminalen; hamnar i sys.argv. | 4 |
| **comprehension** | comprehension | Ett kort sätt att bygga en lista, dictionary eller mängd ur en annan samling. Exempel: `[x * 2 for x in numbers]` | 4 |
| **constructor** | konstruktor | Metoden som körs när ett objekt skapas; heter __init__ i Python. | 4 |
| **dictionary** | ordbok | En samling som kopplar nycklar till värden; typen heter dict. Exempel: `{"Umeå": 132235}` | 4 |
| **encoding** | teckenkodning | Hur tecken som å, ä och ö lagras som bytes; UTF-8 är standard. | 4 |
| **file** | fil | Data som är sparad på disken, till exempel en textfil. | 4 |
| **immutable** | oföränderlig | Kan inte ändras efter att det skapats; text, tal och tupler är oföränderliga. | 4 |
| **instance** | instans | Ett objekt av en viss klass; Rectangle(3, 4) är en instans av Rectangle. | 4 |
| **key** | nyckel | Det man slår upp med i en dictionary. | 4 |
| **key-value pair** | nyckel-värde-par | En nyckel och dess värde i en dictionary. | 4 |
| **lambda** | lambda (anonym funktion) | En kort funktion utan namn som skrivs direkt där den behövs. Exempel: `lambda word: len(word)` | 4 |
| **mutable** | föränderlig | Kan ändras efter att det skapats; listor och dictionaries är föränderliga. | 4 |
| **object** | objekt | Ett värde skapat efter en klass, med egna attribut. | 4 |
| **path** | sökväg | Var en fil eller mapp finns, till exempel data/text.txt. | 4 |
| **self** | self (objektet självt) | Den första parametern i en metod, som pekar på objektet metoden anropades på. | 4 |
| **set** | mängd | En samling unika värden utan bestämd ordning. Exempel: `{"sol", "regn"}` | 4 |
| **sort key** | sorteringsnyckel | En funktion som bestämmer vad som jämförs när man sorterar. Exempel: `sorted(words, key=len)` | 4 |
| **tuple** | tupel | En samling värden i bestämd ordning som inte kan ändras. Exempel: `(59.33, 18.07)` | 4 |
| **unpacking** | uppackning | Att lägga värdena i en tupel eller lista i flera variabler på en gång. Exempel: `lat, lon = point` | 4 |

## Rekursion, datastrukturer och algoritmer (vecka 5–8)

| Engelska | Svenska | Förklaring | Vecka |
|---|---|---|---|
| **base case** | basfall | Fallet där en rekursiv funktion svarar direkt utan att anropa sig själv; utan det tar rekursionen aldrig slut. | 5 |
| **call stack** | anropsstack | Datorns lista över funktionsanrop som pågår; varje anrop läggs överst och tas bort när det returnerar. | 5 |
| **memoization** | memoisering | Att spara resultat av funktionsanrop så att samma uträkning inte görs flera gånger. | 5 |
| **recursion** | rekursion | När en funktion anropar sig själv för att lösa en mindre del av samma problem. | 5 |
| **recursive case** | rekursivt fall | Fallet där en rekursiv funktion anropar sig själv med ett mindre problem. | 5 |
| **stack overflow** | stackspill | När anropsstacken blir för djup, ofta på grund av rekursion utan basfall; i Python ett RecursionError. | 5 |
| **backtracking** | bakåtspårning | Att pröva ett val, gå vidare, och ångra valet om det leder fel. | 6 |
| **depth-first search** | djupet-först-sökning | Att söka genom att följa en väg så långt det går innan man backar och provar nästa. | 6 |
| **permutation** | permutation | En ordning av alla element; [1, 2, 3] har sex permutationer. | 6 |
| **data structure** | datastruktur | Ett sätt att organisera data i minnet så att vissa operationer blir snabba. | 7 |
| **FIFO** | först in, först ut | First in, first out: principen för en kö. | 7 |
| **generator** | generator | En funktion med yield, som ger sina värden ett i taget i stället för alla på en gång. | 7 |
| **iterator** | iterator | Ett objekt som ger ett värde i taget, så att det kan användas i en for-loop. | 7 |
| **LIFO** | sist in, först ut | Last in, first out: principen för en stack. | 7 |
| **linked list** | länkad lista | En lista av noder där varje nod pekar på nästa. | 7 |
| **node** | nod | En byggsten i en länkad struktur som håller ett värde och en referens till nästa nod. | 7 |
| **queue** | kö | En samling där det som lades in först tas ut först (FIFO). | 7 |
| **stack** | stack (trave) | En samling där det som lades in sist tas ut först (LIFO). | 7 |
| **algorithm** | algoritm | En steg-för-steg-beskrivning av hur ett problem löses. | 8 |
| **benchmark** | prestandamätning | Att mäta hur lång tid kod tar att köra. | 8 |
| **Big-O notation** | ordo-notation | Ett sätt att beskriva hur en algoritm skalar, som O(n) eller O(log n). | 8 |
| **binary search** | binärsökning | Att leta i en sorterad lista genom att halvera sökområdet i varje steg. | 8 |
| **linear search** | linjär sökning | Att leta genom att titta på varje element i tur och ordning. | 8 |
| **merge sort** | samsortering | Sorteringsalgoritm som delar listan, sorterar halvorna och fogar ihop dem; O(n log n). | 8 |
| **pivot** | pivotelement | Det element som quicksort delar upp listan kring. | 8 |
| **quicksort** | quicksort | Sorteringsalgoritm som delar listan kring ett pivotelement; i snitt O(n log n). | 8 |
| **stable sort** | stabil sortering | En sortering där lika värden behåller sin inbördes ordning. | 8 |
| **time complexity** | tidskomplexitet | Hur körtiden växer när mängden data växer, uttryckt med Big-O. | 8 |

## Objektorientering och Java (vecka 9–12)

| Engelska | Svenska | Förklaring | Vecka |
|---|---|---|---|
| **composition** | komposition | När ett objekt består av eller håller andra objekt (har-en-relation), i stället för att ärva. | 9 |
| **encapsulation** | inkapsling | Att dölja ett objekts inre data och bara låta andra ändra den via objektets metoder. | 9 |
| **inheritance** | arv | När en klass bygger vidare på en annan och får dess attribut och metoder. | 9 |
| **object-oriented programming** | objektorienterad programmering | Att bygga program av objekt som samarbetar, där varje objekt har egna data och metoder. | 9 |
| **override** | överskugga | Att en subklass skriver en egen version av en metod som finns i superklassen. | 9 |
| **subclass** | subklass | En klass som ärver från en annan klass. | 9 |
| **superclass** | superklass | Den klass som en annan klass ärver från. | 9 |
| **compile** | kompilera | Att översätta källkod med en kompilator. | 10 |
| **compiler** | kompilator | Program som översätter källkod till något datorn kan köra, och som hittar typfel innan programmet körs. | 10 |
| **dependency** | beroende | Ett externt bibliotek som ett projekt behöver, till exempel JUnit. | 10 |
| **dynamic typing** | dynamisk typning | Att typer kontrolleras först när programmet körs, som i Python. | 10 |
| **JVM** | Javas virtuella maskin | Programmet som kör kompilerad Java-kod (Java Virtual Machine). | 10 |
| **Maven** | Maven | Byggverktyg för Java som kompilerar, hämtar beroenden och kör tester. | 10 |
| **overloading** | överlagring | Flera metoder med samma namn men olika parametrar. | 10 |
| **primitive type** | primitiv typ | En grundtyp i Java som int, double och boolean, som inte är ett objekt. | 10 |
| **reference type** | referenstyp | En typ vars variabler pekar på ett objekt, som String i Java. | 10 |
| **static typing** | statisk typning | Att varje variabel har en typ som kontrolleras innan programmet körs, som i Java. | 10 |
| **abstract class** | abstrakt klass | En klass som inte kan användas direkt, men som subklasser bygger vidare på. | 11 |
| **interface** | gränssnitt | En lista över metoder som en klass lovar att ha, utan att säga hur de fungerar. | 11 |
| **polymorphism** | polymorfism | Att samma metodanrop gör olika saker beroende på vilket objekt det anropas på. | 11 |
| **access modifier** | åtkomstmodifierare | Ord som public och private som anger vem som får använda en klass, metod eller variabel. | 12 |
| **Collections Framework** | samlingsramverket | Javas inbyggda samlingar som List, Set och Map. | 12 |
| **Comparable** | jämförbar | Java-gränssnitt för en klass naturliga ordning, via metoden compareTo. | 12 |
| **Comparator** | jämförare | Java-objekt som anger en ordning att sortera i, utöver den naturliga. | 12 |
| **equals and hashCode** | likhet och hashkod | Java-metoderna som avgör när två objekt räknas som lika; de måste stämma överens. | 12 |
| **generics** | generiska typer | Att ange vilken typ en samling innehåller, som List<Book> i Java. | 12 |
| **map** | avbildning | Javas motsvarighet till Pythons dictionary: nycklar kopplade till värden. | 12 |

## Undantag, testning, felsökning och Git (vecka 13–18)

| Engelska | Svenska | Förklaring | Vecka |
|---|---|---|---|
| **checked exception** | kontrollerat undantag | Java-undantag som måste fångas eller deklareras, annars kompilerar inte koden. | 13 |
| **defensive programming** | defensiv programmering | Att skriva kod som tål felaktiga indata genom att kontrollera dem. | 13 |
| **fail fast** | misslyckas tidigt | Att avbryta så fort något är fel, nära orsaken, i stället för att fortsätta med felaktiga värden. | 13 |
| **parsing** | tolkning | Att läsa text och göra om den till strukturerade data. | 13 |
| **try-with-resources** | try med resurser | Java-konstruktion som stänger filer och liknande automatiskt; motsvarar with i Python. | 13 |
| **unchecked exception** | okontrollerat undantag | Java-undantag som inte måste deklareras, till exempel IllegalArgumentException. | 13 |
| **assertion** | påstående | En kontroll i ett test av att ett värde är det förväntade. | 14 |
| **JUnit** | JUnit | Det vanligaste testramverket för Java. | 14 |
| **parameterized test** | parametriserat test | Ett test som körs flera gånger med olika indata. | 14 |
| **test-driven development** | testdriven utveckling | Att skriva ett test som misslyckas först, sedan koden som får det att gå igenom. | 14 |
| **bisection** | bisektion | Att hitta ett fel genom att upprepade gånger halvera området där det kan finnas. | 15 |
| **breakpoint** | brytpunkt | En markerad rad där debuggern stannar programmet. | 15 |
| **debugger** | debugger | Verktyg som låter dig köra ett program steg för steg och titta på variablerna. | 15 |
| **debugging** | felsökning | Att hitta och rätta fel i ett program. | 15 |
| **stack trace** | stackspår | Listan över funktionsanrop som ledde fram till ett fel; Javas motsvarighet till traceback. | 15 |
| **branch** | gren | En egen utvecklingslinje i git, där man kan arbeta utan att påverka andra. | 16 |
| **clone** | klona | Att kopiera ett repo med hela dess historik till sin egen dator. | 16 |
| **commit** | incheckning | En sparad ögonblicksbild av projektet i git, med ett meddelande om vad som ändrats. | 16 |
| **git** | git | Det vanligaste systemet för versionshantering. | 16 |
| **merge** | sammanslagning | Att föra ihop ändringarna från två grenar. | 16 |
| **merge conflict** | sammanslagningskonflikt | När två grenar ändrat samma rader och git inte kan avgöra vilken ändring som gäller. | 16 |
| **pull** | hämta ner | Att hämta och slå ihop andras incheckningar från ett repo på en server. | 16 |
| **pull request** | ändringsförfrågan | En begäran om att få sina ändringar granskade och sammanslagna i ett gemensamt projekt. | 16 |
| **push** | skicka upp | Att skicka sina incheckningar till ett repo på en server. | 16 |
| **rebase** | flytta gren | Att flytta en grens ändringar så att de ligger ovanpå en annan gren. | 16 |
| **repository** | kodförråd (repo) | En mapp med ett projekt och hela dess historik i git. | 16 |
| **version control** | versionshantering | System som sparar alla ändringar i ett projekt så att man kan gå tillbaka och samarbeta. | 16 |
| **capstone** | slutprojekt | Ett större projekt som binder ihop det man lärt sig. | 17 |

## Databaser och SQL (vecka 19–24)

| Engelska | Svenska | Förklaring | Vecka |
|---|---|---|---|
| **column** | kolumn | En egenskap i en tabell, med ett namn och en typ. | 19 |
| **database** | databas | En organiserad samling data som ett program kan fråga och ändra. | 19 |
| **declarative** | deklarativ | Att beskriva vad man vill ha i stället för hur det ska tas fram, som i SQL. | 19 |
| **DISTINCT** | unika | SQL-ord som tar bort dubbletter ur resultatet. | 19 |
| **LIMIT** | begränsa | SQL-ord som anger hur många rader som högst ska returneras. | 19 |
| **NULL** | saknat värde | SQL:s markering för ett okänt eller saknat värde; jämförs med IS NULL. | 19 |
| **ORDER BY** | sortera efter | SQL-ord som sorterar resultatet. | 19 |
| **query** | fråga | En SQL-sats som hämtar data, till exempel en SELECT. | 19 |
| **relational database** | relationsdatabas | En databas som lagrar data i tabeller som kopplas ihop med nycklar. | 19 |
| **row** | rad | En post i en tabell, till exempel en stad eller en mätning. | 19 |
| **SELECT** | välj | SQL-ord som anger vilka kolumner som ska hämtas. | 19 |
| **SQL** | SQL | Språket man ställer frågor till och ändrar data i en relationsdatabas med (Structured Query Language). | 19 |
| **SQLite** | SQLite | En liten databas som lagras i en enda fil och följer med Python som modulen sqlite3. | 19 |
| **table** | tabell | Data ordnad i rader och kolumner. | 19 |
| **WHERE** | där | SQL-ord som filtrerar fram de rader som uppfyller ett villkor. | 19 |
| **aggregate function** | aggregatfunktion | En funktion som slår ihop många rader till ett värde, som COUNT, SUM eller AVG. | 20 |
| **conditional aggregation** | villkorlig aggregering | Att räkna bara vissa rader per grupp med SUM(CASE WHEN ... THEN 1 ELSE 0 END). | 20 |
| **GROUP BY** | gruppera efter | SQL-ord som delar rader i grupper så att aggregatfunktioner räknas per grupp. | 20 |
| **HAVING** | som har | SQL-ord som filtrerar grupper efter grupperingen, så att det kan använda aggregat. | 20 |
| **alias** | alias | Ett kort tillfälligt namn på en tabell eller kolumn i en fråga. | 21 |
| **foreign key** | främmande nyckel | En kolumn som pekar på primärnyckeln i en annan tabell. | 21 |
| **JOIN** | koppla ihop | SQL-ord som kombinerar rader från två tabeller där ett villkor stämmer. | 21 |
| **LEFT JOIN** | vänsterkoppling | En JOIN som behåller alla rader från den vänstra tabellen, även de utan matchning. | 21 |
| **normalization** | normalisering | Att dela upp data i tabeller så att varje fakta lagras på ett enda ställe. | 21 |
| **one-to-many** | en-till-många | En relation där en rad i en tabell hör ihop med många rader i en annan, som en stad och dess mätningar. | 21 |
| **primary key** | primärnyckel | En kolumn som unikt identifierar varje rad i en tabell. | 21 |
| **subquery** | delfråga | En fråga inuti en annan fråga. | 21 |
| **constraint** | begränsning (regel) | En regel i databasen som avvisar ogiltiga data, som NOT NULL, UNIQUE eller CHECK. | 22 |
| **DELETE** | radera | SQL-sats som tar bort rader. | 22 |
| **INSERT** | infoga | SQL-sats som lägger till rader. | 22 |
| **parameterized query** | parametriserad fråga | En SQL-fråga där värden skickas separat via platshållare som ?, vilket hindrar SQL-injektion. | 22 |
| **rollback** | återställa | Att ångra alla ändringar i en transaktion. | 22 |
| **schema** | schema | Beskrivningen av en databas tabeller, kolumner och regler. | 22 |
| **SQL injection** | SQL-injektion | Säkerhetshål där indata tolkas som SQL-kod; undviks med parametriserade frågor. | 22 |
| **transaction** | transaktion | En grupp ändringar som antingen genomförs alla eller inte alls. | 22 |
| **UPDATE** | uppdatera | SQL-sats som ändrar befintliga rader. | 22 |
| **CTE** | namngiven delfråga | Common table expression: en namngiven mellanfråga som skrivs med WITH. | 23 |
| **fan-out** | dubbelräkning vid join | När en join upprepar rader så att summor räknas flera gånger. | 23 |
| **PARTITION BY** | dela upp efter | Del av OVER (...) som delar raderna i grupper för en fönsterfunktion. | 23 |
| **running total** | löpande summa | En summa som för varje rad räknar med alla tidigare rader. | 23 |
| **window function** | fönsterfunktion | En funktion som räknar över flera rader men behåller varje rad, med OVER (...). | 23 |
| **audit trail** | ändringslogg | En logg över ändringar, som ingen kan glömma att skriva om den sköts av databasen. | 24 |
| **business logic** | affärslogik | De regler som gör att data betyder något för verksamheten, som att man inte kan sälja det som inte finns i lager. | 24 |
| **state machine** | tillståndsmaskin | En modell där något bara kan gå mellan vissa tillstånd, som open, paid och shipped. | 24 |
| **trigger** | trigger (utlösare) | SQL-kod som databasen kör automatiskt när rader ändras. | 24 |
| **upsert** | infoga eller uppdatera | Att lägga till en rad, eller uppdatera den om den redan finns. | 24 |
| **view** | vy | En sparad fråga som kan användas som en tabell. | 24 |

## API:er (vecka 25–26)

| Engelska | Svenska | Förklaring | Vecka |
|---|---|---|---|
| **API** | programmeringsgränssnitt | Application programming interface: de förfrågningar ett program lovar att förstå och de svar det lovar att ge. | 25 |
| **API key** | API-nyckel | En hemlig nyckel som identifierar den som anropar ett API; ska aldrig läggas i koden. | 25 |
| **body** | kropp | Själva innehållet i en förfrågan eller ett svar, ofta JSON. | 25 |
| **client** | klient | Programmet som skickar en förfrågan till en server. | 25 |
| **endpoint** | ändpunkt | En adress i ett API som man kan skicka förfrågningar till. | 25 |
| **GET** | hämta | HTTP-metod för att läsa en resurs utan att ändra något. | 25 |
| **header** | rubrik (huvud) | Metadata i en förfrågan eller ett svar, som Content-Type. | 25 |
| **HTTP** | HTTP | Protokollet som webbläsare och API:er använder för förfrågningar och svar. | 25 |
| **HTTP method** | HTTP-metod | Vad förfrågan vill göra: GET, POST, PUT, PATCH eller DELETE. | 25 |
| **HTTPS** | HTTPS | Krypterad HTTP. | 25 |
| **idempotent** | idempotent | Att göra något två gånger har samma effekt som att göra det en gång. | 25 |
| **JSON** | JSON | Textformat för strukturerade data som nästan alla API:er använder. | 25 |
| **percent-encoding** | procentkodning | Att skriva tecken som inte får finnas i en URL som %-koder, som Malm%C3%B6. | 25 |
| **POST** | skicka | HTTP-metod för att skapa något nytt. | 25 |
| **query string** | frågesträng | Delen av en URL efter ?, med nyckel=värde-par. | 25 |
| **rate limit** | anropsgräns | Hur många förfrågningar ett API tillåter per tidsenhet. | 25 |
| **request** | förfrågan | Det klienten skickar: metod, adress, rubriker och ibland en kropp. | 25 |
| **resource** | resurs | En sak som ett API ger åtkomst till, som en stad eller en mätning. | 25 |
| **response** | svar | Det servern skickar tillbaka: statuskod, rubriker och ofta en kropp. | 25 |
| **REST** | REST | En stil för API:er där adresserna namnger resurser och metoderna anger vad man gör med dem. | 25 |
| **server** | server | Programmet som tar emot förfrågningar och skickar svar. | 25 |
| **status code** | statuskod | Tresiffrigt tal i svaret som säger hur det gick, som 200, 404 eller 500. | 25 |
| **timeout** | tidsgräns | Hur länge man väntar på ett svar innan man ger upp. | 25 |
| **URL** | webbadress | En adress till en resurs, med schema, värd, sökväg och ibland en frågesträng. | 25 |
| **framework** | ramverk | Ett färdigt bibliotek som ger strukturen för ett program, som Flask eller FastAPI för webb-API:er. | 26 |
| **routing** | routning | Att avgöra vilken kod som ska hantera en förfrågan utifrån metod och adress. | 26 |
| **stateless** | tillståndslös | Att varje förfrågan innehåller allt servern behöver, så att servern inte minns något mellan förfrågningar. | 26 |
