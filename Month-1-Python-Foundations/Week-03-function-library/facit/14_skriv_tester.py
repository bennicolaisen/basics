# Facit: Övning 3.14 – Skriv egna tester
#
# Bra tester prövar varje sak funktionen lovar, en sak per test: ett
# vanligt fall åt båda hållen, och varje parameter både med standardvärdet
# och ändrat. Ett test som bara prövar "kajak" skulle inte märka om
# funktionen glömde bort stora bokstäver.

from function_library.text_utils import is_palindrome


def test_simple_palindrome():
    assert is_palindrome("kajak")


def test_not_a_palindrome():
    assert not is_palindrome("kanot")


def test_ignores_case_by_default():
    assert is_palindrome("Kajak")


def test_ignores_spaces_by_default():
    assert is_palindrome("ni talar bra latin")


def test_can_require_exact_case():
    assert not is_palindrome("Kajak", ignore_case=False)


def test_can_require_exact_spaces():
    assert not is_palindrome("ni talar bra latin", ignore_spaces=False)
