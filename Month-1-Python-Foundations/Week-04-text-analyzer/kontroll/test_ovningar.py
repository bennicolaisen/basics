"""Kontroller för veckans övningar.

Kör alla:            python -m pytest kontroll
Kör en enda övning:  python -m pytest kontroll -k 05

Ett test som misslyckas skriver ut vad som var fel. Läs meddelandet
efter "AssertionError", rätta din kod och kör igen.

(PYTEST_DONT_REWRITE: raden gör att pytest bara visar meddelandena
nedan, i stället för en lång teknisk analys.)
"""

import inspect

import pytest


def check(function, args, expected):
    """Anropa function(*args) och jämför med expected, med ett begripligt meddelande."""
    call = f"{function.__name__}({', '.join(repr(a) for a in args)})"
    got = function(*args)
    assert got == expected, f"{call} ska returnera {expected!r}, men returnerade {got!r}"
    return got


def test_01_nast_storst(ovning):
    m = ovning("01_nast_storst")
    numbers = [4, 9, 1, 7]
    check(m.second_largest, [numbers], 7)
    assert numbers == [4, 9, 1, 7], "Listan som skickades in får inte ändras (använd sorted, inte sort)"
    check(m.second_largest, [[5, 5]], 5)
    for too_short in ([], [3]):
        with pytest.raises(ValueError):
            m.second_largest(too_short)


def test_02_forsta_och_sista(ovning):
    m = ovning("02_forsta_och_sista")
    check(m.first_and_last, [["Umeå", "Luleå", "Kiruna"]], ("Umeå", "Kiruna"))
    check(m.first_and_last, [["ensam"]], ("ensam", "ensam"))


def test_03_min_och_max(ovning):
    m = ovning("03_min_och_max")
    check(m.min_and_max, [[3, -1, 8]], (-1, 8))
    check(m.min_and_max, [[2]], (2, 2))


def test_04_byt_plats(kor):
    resultat = kor("04_byt_plats")
    assert resultat.utskrift == "a = 2, b = 1\n", f"Fick {resultat.utskrift!r}"


def test_05_telefonbok(ovning):
    m = ovning("05_telefonbok")
    book = {"Alva": "070-123", "Bo": "073-456"}
    check(m.lookup, [book, "Alva"], "070-123")
    check(m.lookup, [book, "Cyril"], "okänt")


def test_06_rakna_bokstaver(ovning):
    m = ovning("06_rakna_bokstaver")
    check(m.count_letters, ["Anna!"], {"a": 2, "n": 2})
    check(m.count_letters, ["Åsa ås"], {"å": 2, "s": 2, "a": 1})
    check(m.count_letters, ["123 !?"], {})


def test_07_vand_pa(ovning):
    m = ovning("07_vand_pa")
    check(m.invert, [{"SE": "Sverige", "NO": "Norge"}], {"Sverige": "SE", "Norge": "NO"})
    check(m.invert, [{}], {})


def test_08_sla_ihop(ovning):
    m = ovning("08_sla_ihop")
    first = {"paraply": 3, "mössa": 1}
    second = {"paraply": 2, "vantar": 4}
    check(m.merge_counts, [first, second], {"paraply": 5, "mössa": 1, "vantar": 4})
    assert first == {"paraply": 3, "mössa": 1}, "Den första dictionaryn får inte ändras (gör en kopia)"
    assert second == {"paraply": 2, "vantar": 4}, "Den andra dictionaryn får inte ändras"


def test_09_unika(ovning):
    check(ovning("09_unika").unique_sorted, [["sol", "regn", "sol", "snö", "regn"]], ["regn", "snö", "sol"])
    check(ovning("09_unika").unique_sorted, [[3, 1, 3]], [1, 3])


def test_10_gemensamma(ovning):
    m = ovning("10_gemensamma")
    check(m.common, [["Oslo", "Umeå", "Visby"], ["Visby", "Oslo", "Malmö"]], ["Oslo", "Visby"])
    check(m.common, [["a"], ["b"]], [])


def test_11_kvadrater(ovning):
    m = ovning("11_kvadrater")
    check(m.squares, [4], [1, 4, 9, 16])
    check(m.squares, [0], [])
    assert " for " in inspect.getsource(m.squares).split("return", 1)[-1], "Skriv svaret som en list comprehension efter return"


def test_12_filtrera(ovning):
    m = ovning("12_filtrera")
    check(m.words_longer_than, [["sol", "regn", "åska", "snöstorm"], 3], ["regn", "åska", "snöstorm"])
    check(m.words_longer_than, [["sol"], 5], [])


def test_13_sortera_langd(ovning):
    m = ovning("13_sortera_langd")
    words = ["snö", "regn", "is", "sol"]
    check(m.sort_by_length, [words], ["is", "snö", "sol", "regn"])
    assert words == ["snö", "regn", "is", "sol"], "Listan som skickades in får inte ändras"


def test_14_vinnaren(ovning):
    m = ovning("14_vinnaren")
    check(m.winner, [{"Bo": 7, "Alva": 9, "Cyril": 9}], "Alva")
    check(m.winner, [{"Bo": 10, "Alva": 9}], "Bo")
    check(m.winner, [{"Dina": 0}], "Dina")


def test_15_gruppera(ovning):
    m = ovning("15_gruppera")
    check(m.group_by_first_letter, [["sol", "snö", "regn"]], {"s": ["sol", "snö"], "r": ["regn"]})
    check(m.group_by_first_letter, [[]], {})


def test_16_las_fil(ovning, tmp_path):
    path = tmp_path / "text.txt"
    path.write_text("Hej på dig\nHej då\n", encoding="utf-8")
    check(ovning("16_las_fil").count_lines_and_words, [path], (2, 5))
    empty = tmp_path / "tom.txt"
    empty.write_text("", encoding="utf-8")
    check(ovning("16_las_fil").count_lines_and_words, [empty], (0, 0))


def test_17_skriv_fil(ovning, tmp_path):
    m = ovning("17_skriv_fil")
    path = tmp_path / "ut.txt"
    path.write_text("gammalt innehåll\n", encoding="utf-8")
    m.save_lines(path, ["sol", "regn"])
    content = path.read_text(encoding="utf-8")
    assert content == "sol\nregn\n", f"Filen ska innehålla 'sol\\nregn\\n', men innehöll {content!r}"


def test_18_klass(ovning):
    Rectangle = ovning("18_klass").Rectangle
    r = Rectangle(3, 4)
    assert getattr(r, "width", None) == 3 and getattr(r, "height", None) == 4, "Rectangle(3, 4) ska spara width=3 och height=4"
    assert r.area() == 12, f"area() ska ge 12, gav {r.area()!r}"
    assert r.perimeter() == 14, f"perimeter() ska ge 14, gav {r.perimeter()!r}"
    assert r.is_square() is False, "Rectangle(3, 4) är ingen kvadrat"
    assert Rectangle(5, 5).is_square() is True, "Rectangle(5, 5) är en kvadrat"
