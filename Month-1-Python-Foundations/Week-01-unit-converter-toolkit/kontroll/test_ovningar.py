"""Kontroller för veckans övningar.

Kör alla:            python -m pytest kontroll
Kör en enda övning:  python -m pytest kontroll -k 05

Kontrollerna provar fler fall än exemplen i uppgifterna. Ett program som
bara klarar exemplet blir underkänt.

(PYTEST_DONT_REWRITE: raden gör att pytest bara visar meddelandena
nedan, i stället för en lång teknisk analys.)
"""

import ast

import pytest


def lines(text: str) -> list[str]:
    return text.strip("\n").split("\n")


def called_names(source: str) -> list[str]:
    """Namnen på alla funktioner som anropas direkt i koden, till exempel ["input", "print"]."""
    names = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Call):
            names.append(node.func.id if isinstance(node.func, ast.Name) else "." + getattr(node.func, "attr", "?"))
    return names


def uses(source: str, *node_types) -> bool:
    return any(isinstance(node, node_types) for node in ast.walk(ast.parse(source)))


# 1.1 ---------------------------------------------------------------------


def test_01_citat(kor, kallkod):
    expected = "Hon sa: \"Det går inte att skriva så här.\"\nHan svarade: 'Prova C:\\kurs\\nytt' i stället.\n"
    ut = kor("01_citat").utskrift
    assert ut == expected, f"Utskriften stämmer inte. Ditt program skrev:\n{ut}"
    count = called_names(kallkod("01_citat")).count("print")
    assert count == 1, f"print ska anropas exakt en gång, men anropas {count} gånger."


# 1.2 ---------------------------------------------------------------------


def test_02_tre_fel(kor, kallkod):
    ut = kor("02_tre_fel").utskrift
    assert ut == "Totalt: 147 kr\nMed 10 % rabatt: 132.30 kr\n", f"Utskriften stämmer inte. Ditt program skrev:\n{ut}"
    ut = kor("02_tre_fel", ersatt={"pris = 49": "pris = 20", "antal = 3": "antal = 7"}).utskrift
    assert ut == "Totalt: 140 kr\nMed 10 % rabatt: 126.00 kr\n", (
        f"Med pris = 20 och antal = 7 skrev programmet:\n{ut}\nUtskriften ska räknas fram från pris och antal."
    )
    comments = "\n".join(line for line in kallkod("02_tre_fel").splitlines() if line.lstrip().startswith("#"))
    positions = [comments.find(name) for name in ("SyntaxError", "TypeError", "NameError")]
    assert -1 not in positions, "Överst i filen ska namnen på de tre feltyperna stå som kommentarer."
    assert positions == sorted(positions), "Feltyperna står inte i den ordning Python visade dem."


# 1.3 ---------------------------------------------------------------------


@pytest.mark.parametrize("a, b", [("7", "42"), ("'hej'", "3.5"), ("-1", "'två ord'"), ("True", "None")])
def test_03_byt_plats(kor, a, b):
    resultat = kor("03_byt_plats", ersatt={"a = 7": f"a = {a}", "b = 42": f"b = {b}"})
    old_a, old_b = ast.literal_eval(a), ast.literal_eval(b)
    assert (resultat.variabler.get("a"), resultat.variabler.get("b")) == (old_b, old_a), (
        f"Med a = {a} och b = {b} har värdena inte bytt plats."
    )
    expected = f"a = {old_b}, b = {old_a}\n"
    assert resultat.utskrift == expected, (
        f"Med a = {a} och b = {b} ska utskriften vara {expected!r}, men var {resultat.utskrift!r}."
    )


# 1.4 ---------------------------------------------------------------------


@pytest.mark.parametrize(
    "given, expected",
    [
        ("100000", "1 dygn, 3 h, 46 min, 40 s"),
        ("0", "0 dygn, 0 h, 0 min, 0 s"),
        ("59", "0 dygn, 0 h, 0 min, 59 s"),
        ("3600", "0 dygn, 1 h, 0 min, 0 s"),
        ("86399", "0 dygn, 23 h, 59 min, 59 s"),
        ("90061", "1 dygn, 1 h, 1 min, 1 s"),
        ("1000000", "11 dygn, 13 h, 46 min, 40 s"),
    ],
)
def test_04_sekunder(kor, given, expected):
    ut = kor("04_sekunder", inmatning=[given]).utskrift
    assert lines(ut)[-1] == expected, f"Med {given} ska sista raden vara {expected!r}, men var {lines(ut)[-1]!r}."


# 1.5 ---------------------------------------------------------------------


@pytest.mark.parametrize(
    "given, total, backwards",
    [("1200", 3, "0021"), ("1234", 10, "4321"), ("7", 7, "7000"), ("0", 0, "0000"),
     ("1050", 6, "0501"), ("9999", 36, "9999"), ("8070", 15, "0708")],
)
def test_05_siffror(kor, given, total, backwards):
    expected = [f"Siffersumma: {total}", f"Baklänges: {backwards}"]
    got = lines(kor("05_siffror", inmatning=[given]).utskrift)[-2:]
    assert got == expected, f"Med {given} ska de sista raderna vara {expected}, men var {got}."


def test_05_siffror_regler(kallkod):
    source = kallkod("05_siffror")
    others = sorted(set(called_names(source)) - {"input", "int", "print"})
    assert not others, f"Koden får bara anropa input, int och print, men anropar också: {', '.join(others)}."
    assert not uses(source, ast.Subscript, ast.List, ast.ListComp), "Koden får inte innehålla hakparenteser."


# 1.6 ---------------------------------------------------------------------


@pytest.mark.parametrize(
    "given, expected",
    [("1234567.891", "1 234 567,89 kr"), ("-1500.5", "-1 500,50 kr"), ("5", "5,00 kr"),
     ("999.999", "1 000,00 kr"), ("12.3", "12,30 kr"), ("123456", "123 456,00 kr"), ("0", "0,00 kr")],
)
def test_06_svenskt_belopp(kor, given, expected):
    last = lines(kor("06_svenskt_belopp", inmatning=[given]).utskrift)[-1]
    assert last == expected, f"Med {given} ska sista raden vara {expected!r}, men var {last!r}."


# 1.7 ---------------------------------------------------------------------


def box(width: int, height: int) -> str:
    edge = "+" + "-" * (width - 2) + "+"
    middle = "|" + " " * (width - 2) + "|"
    return "\n".join([edge] + [middle] * (height - 2) + [edge]) + "\n"


@pytest.mark.parametrize("width, height", [(5, 3), (2, 2), (6, 4), (3, 5), (10, 2)])
def test_07_ruta(kor, width, height):
    ut = kor("07_ruta", inmatning=[str(width), str(height)]).utskrift
    expected = f"Bredd: {width}\nHöjd: {height}\n" + box(width, height)
    assert ut == expected, f"Med bredden {width} och höjden {height} ska utskriften vara:\n{expected}\nDitt program skrev:\n{ut}"


def test_07_ruta_regler(kallkod):
    assert not uses(kallkod("07_ruta"), ast.For, ast.While, ast.comprehension), "Koden får inte innehålla loopar."


# 1.8 ---------------------------------------------------------------------


@pytest.mark.parametrize(
    "given, initials, catalog",
    [("  ada LOVELACE ", "A.L.", "Lovelace, Ada"), ("grace hopper", "G.H.", "Hopper, Grace"),
     ("LINUS torvalds", "L.T.", "Torvalds, Linus"), ("åsa öberg", "Å.Ö.", "Öberg, Åsa"),
     ("x y", "X.Y.", "Y, X"), ("jean-luc PICARD ", "J.P.", "Picard, Jean-luc")],
)
def test_08_namn(kor, given, initials, catalog):
    expected = [f"Initialer: {initials}", f"Katalognamn: {catalog}"]
    got = lines(kor("08_namn", inmatning=[given]).utskrift)[-2:]
    assert got == expected, f"Med {given!r} ska de sista raderna vara {expected}, men var {got}."


# 1.9 ---------------------------------------------------------------------

EXPRESSIONS = [
    "7 / 7", "7 // 2.0", "-7 // 2", "-7 % 2", "round(2.5)", "round(3.5)", "int(-3.99)", '"3" * 3',
    'int("3.5")', "0.1 + 0.2 == 0.3", "True + True + True", "2 ** 3 ** 2", '"10" < "9"',
    'len("Malmö\\n")', '"Malmö"[-1]', '"Malmö"[1:4]',
]


def actual_value(expression: str):
    try:
        return eval(expression)
    except Exception as error:
        return type(error).__name__


def test_09_forutsag(kallkod):
    answers = {}
    for node in ast.parse(kallkod("09_forutsag")).body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            answers[node.targets[0].id] = node.value
    unanswered, not_values, wrong = [], [], []
    for number, expression in enumerate(EXPRESSIONS, start=1):
        node = answers.get(f"svar_{number}")
        if node is None or (isinstance(node, ast.Constant) and node.value is Ellipsis):
            unanswered.append(str(number))
            continue
        try:
            given = ast.literal_eval(node)
        except ValueError:
            not_values.append(str(number))
            continue
        expected = actual_value(expression)
        if type(given) is not type(expected) or given != expected:
            wrong.append(str(number))
    assert not unanswered, f"Obesvarade: {', '.join(unanswered)}."
    assert not not_values, f"Skriv värden, inte uttryck: {', '.join(not_values)}."
    assert not wrong, f"{len(wrong)} av {len(EXPRESSIONS)} svar är fel: {', '.join(wrong)}."


# 1.10 --------------------------------------------------------------------


@pytest.mark.parametrize(
    "value, step, expected",
    [(17, 5, 15), (149, 100, 100), (18, 5, 20), (25, 10, 30), (35, 10, 40), (45, 10, 50), (150, 100, 200),
     (250, 100, 300), (0, 5, 0), (7, 1, 7), (13, 5, 15), (1, 3, 0), (2, 3, 3)],
)
def test_10_avrunda(ovning, value, step, expected):
    got = ovning("10_avrunda").round_to_nearest(value, step)
    assert got == expected, f"round_to_nearest({value}, {step}) ska ge {expected}, men gav {got!r}."
    assert isinstance(got, int), f"round_to_nearest({value}, {step}) ska returnera ett heltal, men gav {got!r}."


# 1.11 --------------------------------------------------------------------


@pytest.mark.parametrize(
    "start, end, expected",
    [("08:15", "09:00", 45), ("22:30", "01:15", 165), ("12:00", "12:00", 0), ("00:00", "23:59", 1439),
     ("23:59", "00:00", 1), ("09:05", "08:59", 1434), ("10:50", "11:10", 20)],
)
def test_11_klockslag(ovning, start, end, expected):
    got = ovning("11_klockslag").minutes_between(start, end)
    assert got == expected, f"minutes_between({start!r}, {end!r}) ska ge {expected}, men gav {got!r}."


# 1.12 --------------------------------------------------------------------


@pytest.mark.parametrize(
    "total, people, tip, expected",
    [(1000, 3, 10, 367), (900, 3, 0, 300), (100, 3, 0, 34), (50, 1, 10, 55), (25, 4, 12, 7),
     (19.99, 1, 25, 25), (12.5, 2, 12, 7), (333.33, 3, 0, 112)],
)
def test_12_dela_notan(ovning, total, people, tip, expected):
    got = ovning("12_dela_notan").split_bill(total, people, tip)
    assert got == expected, f"split_bill({total}, {people}, {tip}) ska ge {expected}, men gav {got!r}."
    assert isinstance(got, int), f"split_bill({total}, {people}, {tip}) ska returnera ett heltal, men gav {got!r}."


# 1.13 --------------------------------------------------------------------


def _right(total):
    return f"{total // 3600}:{total % 3600 // 60:02d}:{total % 60:02d}"


def _version_1(total):
    return f"{total // 3600}:{total // 60:02d}:{total % 60:02d}"


def _version_2(total):
    return f"{total // 3600}:{total % 3600 // 60}:{total % 60:02d}"


def _version_3(total):
    return f"{total // 3600}:{total % 3600 // 60:02d}:{total % 3600:02d}"


def _version_4(total):
    return f"{total // 3600 % 24}:{total % 3600 // 60:02d}:{total % 60:02d}"


def _version_5(total):
    return f"{round(total / 3600)}:{total % 3600 // 60:02d}:{total % 60:02d}"


def _version_6(total):
    return f"{total // 3600:02d}:{total % 3600 // 60:02d}:{total % 60:02d}"


BUGGY = [_version_1, _version_2, _version_3, _version_4, _version_5, _version_6]


def test_13_avsloja_buggar(ovning):
    check = ovning("13_avsloja_buggar").check
    try:
        check(_right)
    except AssertionError:
        pytest.fail("Din check underkänner den rätta versionen. Något av dina förväntade svar är fel.")
    missed = []
    for number, version in enumerate(BUGGY, start=1):
        try:
            check(version)
        except AssertionError:
            continue
        missed.append(str(number))
    assert not missed, f"Din check avslöjade inte {len(missed)} av {len(BUGGY)} buggiga versioner (nummer {', '.join(missed)})."
