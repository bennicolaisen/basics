"""Kontroller för veckans övningar.

Kör alla:            python -m pytest kontroll
Kör en enda övning:  python -m pytest kontroll -k 05

Ett test som misslyckas skriver ut vad som var fel. Läs meddelandet
efter "AssertionError", rätta din kod och kör igen.

(PYTEST_DONT_REWRITE: raden gör att pytest bara visar meddelandena
nedan, i stället för en lång teknisk analys.)
"""

import inspect
import math

import pytest


def check(function, args, expected, **kwargs):
    """Anropa function(*args, **kwargs) och jämför med expected, med ett begripligt meddelande."""
    shown = [repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()]
    call = f"{function.__name__}({', '.join(shown)})"
    got = function(*args, **kwargs)
    assert got == expected, f"{call} ska returnera {expected!r}, men returnerade {got!r}"


def check_raises(function, *args):
    call = f"{function.__name__}({', '.join(repr(a) for a in args)})"
    try:
        function(*args)
    except ValueError:
        return
    raise AssertionError(f"{call} ska kasta ValueError")


def test_01_standardvarde(ovning):
    m = ovning("01_standardvarde")
    check(m.greet, ["Bo"], "Hej, Bo!")
    check(m.greet, ["Bo", "Tjena"], "Tjena, Bo!")


def test_02_cirkel(ovning):
    m = ovning("02_cirkel")
    got = m.circle_area(2)
    assert got == pytest.approx(4 * math.pi), f"circle_area(2) ska ge ungefär 12.566, gav {got!r}"
    assert m.circle_area(1) == pytest.approx(math.pi, abs=1e-9), "Använd math.pi, inte 3.14"


@pytest.mark.parametrize("value, expected", [(5, 5), (-3, 1), (42, 10), (1, 1), (10, 10)])
def test_03_begransa(ovning, value, expected):
    check(ovning("03_begransa").clamp, [value, 1, 10], expected)


def test_04_namngivna_argument(ovning):
    f = ovning("04_namngivna_argument").format_temperature
    check(f, [21.46], "21.5 °C")
    check(f, [70.7], "70.7 °F", unit="F")
    check(f, [21.46], "21.46 °C", decimals=2)
    check(f, [-3.04], "-3.0 °C")


def test_05_rackvidd(kor):
    resultat = kor("05_rackvidd")
    assert resultat.utskrift == "1\n", f"Programmet ska skriva ut 1, men skrev {resultat.utskrift!r}"


def test_06_ateranvand(ovning):
    m = ovning("06_ateranvand")
    for number, even in [(4, True), (7, False), (0, True), (-3, False)]:
        check(m.is_even, [number], even)
        check(m.is_odd, [number], not even)
    assert "is_even" in inspect.getsource(m.is_odd), "is_odd ska anropa is_even"


def test_07_storst_av_tre(ovning):
    m = ovning("07_storst_av_tre")
    check(m.larger, [3, 9], 9)
    check(m.larger, [9, 3], 9)
    for args in [(3, 9, 4), (9, 3, 4), (3, 4, 9), (-1, -5, -2), (2, 2, 2)]:
        check(m.largest_of_three, list(args), max(args))
    assert "max(" not in inspect.getsource(m), "Lös uppgiften utan den inbyggda max"


def test_08_procent(ovning):
    m = ovning("08_procent")
    check(m.percent, [1, 4], 25.0)
    check(m.percent, [1, 3], 33.3)
    check(m.percent, [0, 5], 0.0)
    check_raises(m.percent, 1, 0)


def test_09_porto(ovning):
    m = ovning("09_porto")
    for weight, price in [(1, 22), (50, 22), (51, 44), (100, 44), (101, 66), (250, 66), (251, 99), (2000, 99)]:
        check(m.postage, [weight], price)
    check_raises(m.postage, 0)
    check_raises(m.postage, -10)
    check_raises(m.postage, 2001)


def test_10_langa_ord(ovning):
    f = ovning("10_langa_ord").count_long_words
    check(f, ["Det regnar mycket i Göteborg idag"], 3)
    check(f, ["Det regnar mycket"], 3, min_length=2)
    check(f, [""], 0)
    check(f, ["exakt"], 0)  # fem bokstäver är inte fler än fem


@pytest.mark.parametrize("name, expected", [("Alva Larsson", "AL"), ("karl johan nilsson", "KJN"), ("Bo", "B")])
def test_11_initialer(ovning, name, expected):
    check(ovning("11_initialer").initials, [name], expected)


def test_12_dela_upp(ovning):
    m = ovning("12_dela_upp")
    check(m.subtotal, [[100, 50.5]], 150.5)
    check(m.apply_discount, [200, 10], 180.0)
    check(m.total_price, [[100, 50.5], 10], 135.45)
    check(m.total_price, [[100, 50.5]], 150.5)
    source = inspect.getsource(m.total_price)
    assert "subtotal(" in source and "apply_discount(" in source, "total_price ska använda subtotal och apply_discount"


@pytest.mark.parametrize(
    "name, expected",
    [("  alva   larsson ", "Alva Larsson"), ("BO", "Bo"), ("karl johan nilsson", "Karl Johan Nilsson")],
)
def test_13_snygga_namn(ovning, name, expected):
    check(ovning("13_snygga_namn").normalize_name, [name], expected)


def _buggy_ignores_nothing(text, ignore_case=True, ignore_spaces=True):
    return text == text[::-1]


def _buggy_case_sensitive(text, ignore_case=True, ignore_spaces=True):
    if ignore_spaces:
        text = text.replace(" ", "")
    return text == text[::-1]


def _buggy_ignores_parameters(text, ignore_case=True, ignore_spaces=True):
    text = text.replace(" ", "").lower()
    return text == text[::-1]


def test_14_skriv_tester(ovning):
    m = ovning("14_skriv_tester")
    tests = [getattr(m, name) for name in dir(m) if name.startswith("test_")]
    assert len(tests) >= 3, f"Skriv minst tre testfunktioner (namn som börjar med test_). Hittade {len(tests)}."

    from function_library.text_utils import is_palindrome

    def failures_with(implementation):
        m.is_palindrome = implementation
        failed = []
        for test in tests:
            try:
                test()
            except AssertionError:
                failed.append(test.__name__)
        return failed

    failed = failures_with(is_palindrome)
    assert not failed, f"Dina tester ska gå igenom med den riktiga funktionen, men de här misslyckades: {failed}"
    for buggy, description in [
        (_buggy_ignores_nothing, "bryr sig varken om stora bokstäver eller mellanslag"),
        (_buggy_case_sensitive, "glömmer att bortse från stora och små bokstäver"),
        (_buggy_ignores_parameters, "struntar i parametrarna ignore_case och ignore_spaces"),
    ]:
        assert failures_with(buggy), f"Dina tester avslöjar inte en felaktig version som {description}."
    m.is_palindrome = is_palindrome


def test_15_vanligast(ovning):
    m = ovning("15_vanligast")
    check(m.most_common, [[1, 3, 3, 2]], 3)
    check(m.most_common, [[5, 1, 5, 1]], 1)
    check(m.most_common, [[7]], 7)
    check_raises(m.most_common, [])


def test_16_variationsbredd(ovning):
    m = ovning("16_variationsbredd")
    check(m.spread, [[3, 9, 4]], 6)
    check(m.spread, [[5]], 0)
    check(m.spread, [[-2, 2]], 4)
    check_raises(m.spread, [])
