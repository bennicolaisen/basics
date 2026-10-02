"""Tester för facit till "Prova själv" (facit/prova_sjalv.py)."""

import pytest

from facit.prova_sjalv import build_report, modes, most_common_word, stddev, summary, variance
from function_library import stats
from function_library.legacy_report import handle_data


def test_1_report_matches_the_legacy_output(capsys):
    numbers = [1, 2, 2, 3, 10]
    text = "Ni talar bra latin"
    handle_data(numbers, text)
    legacy = capsys.readouterr().out.rstrip("\n")
    assert build_report(numbers, text) == legacy


def test_2_variance_and_stddev():
    assert variance([2, 4, 4, 4, 5, 5, 7, 9]) == pytest.approx(4.0)
    assert stddev([2, 4, 4, 4, 5, 5, 7, 9]) == pytest.approx(2.0)
    assert stddev([1, 2, 3, 4]) == pytest.approx(stats.stddev([1, 2, 3, 4]))


def test_3_most_common_word():
    assert most_common_word("regn regn sol") == "regn"
    assert most_common_word("Sol sol Regn regn") == "regn"  # lika många: först i bokstavsordning
    with pytest.raises(ValueError):
        most_common_word("   ")


def test_4_modes_returns_every_tied_value():
    assert modes([1, 1, 2, 2, 3]) == [1, 2]
    assert modes([4, 4, 1]) == [4]
    assert modes([3, 1, 2]) == [1, 2, 3]
    with pytest.raises(ValueError):
        modes([])


def test_5_summary_rounds_to_the_requested_decimals():
    assert summary([1, 2, 3, 4]) == "medel 2.5, median 2.5, typvärde 1, standardavvikelse 1.12"
    assert summary([1, 2, 3, 4], decimals=0) == "medel 2.0, median 2.0, typvärde 1, standardavvikelse 1.0"
