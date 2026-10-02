"""Kontroller för veckans övningar.

Kör alla:            python -m pytest kontroll
Kör en enda övning:  python -m pytest kontroll -k 05

Ett test som misslyckas skriver ut vad som var fel. Läs meddelandet
efter "AssertionError", rätta din kod och kör igen.

(PYTEST_DONT_REWRITE: raden gör att pytest bara visar meddelandena
nedan, i stället för en lång teknisk analys.)
"""

import pytest


def lines(text: str) -> list[str]:
    return text.strip("\n").split("\n")


def check(function, args, expected):
    """Anropa function(*args) och jämför med expected, med ett begripligt meddelande."""
    call = f"{function.__name__}({', '.join(repr(a) for a in args)})"
    got = function(*args)
    assert got == expected, f"{call} ska returnera {expected!r}, men returnerade {got!r}"


def test_01_myndig(ovning):
    m = ovning("01_myndig")
    check(m.is_adult, [18], True)
    check(m.is_adult, [17], False)
    check(m.is_adult, [65], True)


@pytest.mark.parametrize("number, expected", [(5, "positivt"), (-2, "negativt"), (0, "noll"), (0.5, "positivt")])
def test_02_tecken(ovning, number, expected):
    check(ovning("02_tecken").sign_word, [number], expected)


@pytest.mark.parametrize(
    "points, expected",
    [(100, "A"), (90, "A"), (89, "B"), (80, "B"), (79, "C"), (70, "C"), (65, "D"), (50, "E"), (49, "F"), (0, "F")],
)
def test_03_betyg(ovning, points, expected):
    check(ovning("03_betyg").grade, [points], expected)


@pytest.mark.parametrize("year, expected", [(2024, True), (2023, False), (1900, False), (2000, True), (2100, False)])
def test_04_skottar(ovning, year, expected):
    check(ovning("04_skottar").is_leap_year, [year], expected)


@pytest.mark.parametrize("age, expected", [(8, 20), (11, 20), (12, 30), (17, 30), (18, 40), (64, 40), (65, 25), (90, 25)])
def test_05_biljettpris(ovning, age, expected):
    check(ovning("05_biljettpris").ticket_price, [age], expected)


def test_06_nedrakning(kor):
    ut = kor("06_nedrakning").utskrift
    assert lines(ut) == ["5", "4", "3", "2", "1", "Lyft!"], f"Fick {ut!r}"


@pytest.mark.parametrize("n, expected", [(4, 10), (100, 5050), (1, 1), (0, 0)])
def test_07_summa_till(ovning, n, expected):
    check(ovning("07_summa_till").sum_to, [n], expected)


def test_08_gangertabell(kor):
    ut = kor("08_gangertabell", inmatning=["7"]).utskrift
    rows = [row for row in lines(ut) if " x " in row]
    assert rows[:1] == ["7 x 1 = 7"], f"Första raden i tabellen ska vara '7 x 1 = 7'. Fick {ut!r}"
    assert rows[-1:] == ["7 x 10 = 70"], "Sista raden ska vara '7 x 10 = 70'"
    assert len(rows) == 10, f"Tabellen ska ha 10 rader, hade {len(rows)}"


@pytest.mark.parametrize("text, expected", [("Kiruna", 3), ("Öland", 2), ("", 0), ("BRR", 0), ("Ystad", 2)])
def test_09_vokaler(ovning, text, expected):
    check(ovning("09_vokaler").count_vowels, [text], expected)


@pytest.mark.parametrize("text, expected", [("Malmö", "ömlaM"), ("", ""), ("a", "a"), ("abc", "cba")])
def test_10_baklanges(ovning, text, expected):
    check(ovning("10_baklanges").reverse_text, [text], expected)


@pytest.mark.parametrize("numbers, expected", [([3, 9, 2], 9), ([-5, -2, -8], -2), ([4], 4), ([1, 7, 7], 7)])
def test_11_storsta(ovning, numbers, expected):
    check(ovning("11_storsta").largest, [numbers], expected)


@pytest.mark.parametrize("numbers, expected", [([1, 2, 3, 4, 6], [2, 4, 6]), ([1, 3], []), ([], []), ([0, -2], [0, -2])])
def test_12_jamna_tal(ovning, numbers, expected):
    check(ovning("12_jamna_tal").only_even, [numbers], expected)


def test_13_medelvarde(ovning):
    m = ovning("13_medelvarde")
    check(m.average, [[2, 4, 9]], 5.0)
    check(m.average, [[7]], 7.0)
    with pytest.raises(ValueError):
        m.average([])


@pytest.mark.parametrize("text, expected", [("42", 42), (" 7 ", 7), ("-3", -3), ("sju", None), ("", None), ("4.5", None)])
def test_14_sakert_heltal(ovning, text, expected):
    check(ovning("14_sakert_heltal").to_int_or_none, [text], expected)


def test_15_fraga_igen(kor):
    ut = kor("15_fraga_igen", inmatning=["tjugo", "25 år", "25"]).utskrift
    assert ut.count("Skriv ålder med siffror.") == 2, "Programmet ska klaga en gång för varje svar som inte är ett heltal"
    assert lines(ut)[-1] == "Du är 25 år.", f"Sista raden ska vara 'Du är 25 år.'. Fick {ut!r}"


def test_16_fizzbuzz(ovning):
    m = ovning("16_fizzbuzz")
    check(m.fizzbuzz, [5], ["1", "2", "Fizz", "4", "Buzz"])
    got = m.fizzbuzz(15)
    assert got[14] == "FizzBuzz", f"Talet 15 ska bli 'FizzBuzz', blev {got[14]!r}"
    check(m.fizzbuzz, [0], [])


@pytest.mark.parametrize("guess, secret, expected", [(3, 7, "För lågt"), (9, 7, "För högt"), (7, 7, "Rätt!")])
def test_17_gissning(ovning, guess, secret, expected):
    check(ovning("17_gissning").guess_feedback, [guess, secret], expected)


def test_18_siffror(ovning):
    m = ovning("18_siffror")
    check(m.count_digits, ["Box 123, 456 Umeå"], 6)
    check(m.count_digits, ["inga"], 0)
    for text, expected in [("90736", True), ("907 36", True), ("9073", False), ("907-36", False), ("9073a", False), ("90 736", False)]:
        check(m.is_postcode, [text], expected)
