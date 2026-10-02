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


def test_01_hej_varlden(kor):
    ut = kor("01_hej_varlden").utskrift
    assert ut == "Hej, världen!\n", f"Programmet ska skriva ut exakt 'Hej, världen!' men skrev {ut!r}"


def test_02_tre_rader(kor):
    ut = kor("02_tre_rader").utskrift
    assert lines(ut) == ["Python", "är", "kul"], f"Förväntade tre rader: Python, är, kul. Fick {ut!r}"


def test_03_fixa_felet(kor):
    ut = kor("03_fixa_felet").utskrift
    assert ut == "Jag kan läsa felmeddelanden\n", f"Fick {ut!r}"


def test_04_variabler(kor):
    resultat = kor("04_variabler")
    assert resultat.variabler.get("stad") == "Kiruna", "Variabeln stad ska ha värdet 'Kiruna'"
    assert resultat.variabler.get("temperatur") == -3, "Variabeln temperatur ska ha värdet -3 (ett tal, inte text)"
    assert resultat.utskrift == "I Kiruna är det -3 grader.\n", f"Fick {resultat.utskrift!r}"


def test_05_berakningar(kor):
    resultat = kor("05_berakningar")
    assert resultat.variabler.get("summa") == 387, "Variabeln summa ska vara pris * antal"
    assert resultat.utskrift == "Summa: 387\n", f"Fick {resultat.utskrift!r}"


def test_06_heltalsdivision(kor):
    resultat = kor("06_heltalsdivision")
    assert resultat.variabler.get("timmar") == 3, "timmar ska vara 3 (använd //)"
    assert resultat.variabler.get("minuter") == 20, "minuter ska vara 20 (använd %)"
    assert resultat.utskrift == "200 minuter är 3 timmar och 20 minuter\n", f"Fick {resultat.utskrift!r}"


def test_07_text_eller_tal(kor):
    ut = kor("07_text_eller_tal").utskrift
    assert ut == "15\n", f"Programmet ska skriva ut 15, men skrev {ut!r}"


def test_08_f_strang(kor):
    ut = kor("08_f_strang").utskrift
    assert ut == "Alva är 31 år och fyller 32 nästa år.\n", f"Fick {ut!r}"


def test_09_avrundning(kor):
    ut = kor("09_avrundning").utskrift
    assert ut == "Att betala: 149.70 kr\n", f"Fick {ut!r}"


def test_10_fraga_namn(kor):
    ut = kor("10_fraga_namn", inmatning=["Bo"]).utskrift
    assert lines(ut)[-1] == "Hej, Bo!", f"Med inmatningen Bo ska sista raden vara 'Hej, Bo!'. Fick {ut!r}"
    ut = kor("10_fraga_namn", inmatning=["Malin"]).utskrift
    assert lines(ut)[-1] == "Hej, Malin!", "Programmet ska använda namnet man skriver in, inte ett fast namn"


@pytest.mark.parametrize("given, expected", [("21", "42"), ("0", "0"), ("-7", "-14")])
def test_11_dubbla_talet(kor, given, expected):
    ut = kor("11_dubbla_talet", inmatning=[given]).utskrift
    assert lines(ut)[-1] == expected, f"Med inmatningen {given} ska sista raden vara {expected}. Fick {ut!r}"


@pytest.mark.parametrize(
    "given, expected",
    [("20", "20.0 °C är 68.0 °F"), ("-40", "-40.0 °C är -40.0 °F"), ("21.5", "21.5 °C är 70.7 °F")],
)
def test_12_celsius(kor, given, expected):
    ut = kor("12_celsius", inmatning=[given]).utskrift
    assert lines(ut)[-1] == expected, f"Med inmatningen {given} ska sista raden vara {expected!r}. Fick {ut!r}"


def test_13_funktion_dubbla(ovning):
    m = ovning("13_funktion_dubbla")
    assert m.double(4) == 8, f"double(4) ska returnera 8, men returnerade {m.double(4)!r}"
    assert m.double(2.5) == 5.0, "double(2.5) ska returnera 5.0"
    assert m.double(-3) == -6, "double(-3) ska returnera -6"


def test_14_funktion_halsa(ovning, capsys):
    m = ovning("14_funktion_halsa")
    svar = m.greeting("Bo")
    assert svar == "Hej, Bo!", f"greeting('Bo') ska returnera 'Hej, Bo!', men returnerade {svar!r}"
    assert m.greeting("Malin") == "Hej, Malin!", "greeting ska använda namnet den får"
    assert capsys.readouterr().out == "", "greeting ska returnera texten, inte skriva ut den med print"


def test_15_funktion_rektangel(ovning):
    m = ovning("15_funktion_rektangel")
    assert m.area(3, 4) == 12, f"area(3, 4) ska ge 12, gav {m.area(3, 4)!r}"
    assert m.area(5, 5) == 25, "area(5, 5) ska ge 25"
    assert m.perimeter(3, 4) == 14, f"perimeter(3, 4) ska ge 14, gav {m.perimeter(3, 4)!r}"
    assert m.perimeter(1, 10) == 22, "perimeter(1, 10) ska ge 22"


@pytest.mark.parametrize("minutes, expected", [(200, "3 h 20 min"), (45, "0 h 45 min"), (60, "1 h 0 min")])
def test_16_funktion_minuter(ovning, minutes, expected):
    svar = ovning("16_funktion_minuter").minutes_to_text(minutes)
    assert svar == expected, f"minutes_to_text({minutes}) ska returnera {expected!r}, returnerade {svar!r}"


@pytest.mark.parametrize("price, expected", [(100, 125.0), (19.99, 24.99), (0, 0)])
def test_17_funktion_moms(ovning, price, expected):
    svar = ovning("17_funktion_moms").price_with_vat(price)
    assert svar == expected, f"price_with_vat({price}) ska returnera {expected}, returnerade {svar!r}"


def test_18_funktion_mil(ovning):
    m = ovning("18_funktion_mil")
    assert m.km_to_mil(25) == 2.5, f"km_to_mil(25) ska ge 2.5, gav {m.km_to_mil(25)!r}"
    assert m.mil_to_km(3) == 30, f"mil_to_km(3) ska ge 30, gav {m.mil_to_km(3)!r}"
    assert m.mil_to_km(m.km_to_mil(42)) == 42, "Om man räknar fram och tillbaka ska man få samma tal"
