"""Tests for the Try It Yourself solutions in facit/prova_sjalv.py."""

import pytest

from facit import prova_sjalv as facit
from recursion_basics.recursion import factorial, fibonacci


def test_1_trace_returns_the_right_answer_and_shows_every_call(capsys):
    assert facit.fibonacci_trace(6) == 8
    lines = capsys.readouterr().out.splitlines()
    calls = [line for line in lines if "fibonacci(" in line]
    assert len(calls) == 25
    assert lines[0] == "fibonacci(6)"
    assert lines[-1] == "-> 8"


def test_2_call_count_for_fibonacci_20():
    facit.call_count = 0
    assert facit.fibonacci_counted(20) == 6765
    assert facit.call_count == 21891
    assert facit.call_count < 2 ** 20


def test_3_memoized_version_agrees_and_makes_far_fewer_calls():
    facit.memo_call_count = 0
    assert facit.fibonacci_memo(20) == fibonacci(20)
    assert facit.memo_call_count == 39


def test_3_memoized_version_handles_large_n():
    # The plain version would need about 10**20 calls for this.
    assert facit.fibonacci_memo(90) == 2880067194370816120


def test_3_cache_is_fresh_for_every_top_level_call():
    first = facit.fibonacci_memo(10)
    facit.memo_call_count = 0
    assert facit.fibonacci_memo(10) == first
    assert facit.memo_call_count == 19


@pytest.mark.parametrize("n", [0, 1, 4, 10])
def test_4_accumulator_factorial_matches(n):
    assert facit.factorial_acc(n) == factorial(n)


def test_4_negative_raises():
    with pytest.raises(ValueError):
        facit.factorial_acc(-1)


def test_5_count_up_prints_in_order(capsys):
    facit.count_up(5)
    assert capsys.readouterr().out.split() == ["1", "2", "3", "4", "5"]


def test_5_count_up_zero_prints_nothing(capsys):
    facit.count_up(0)
    assert capsys.readouterr().out == ""
