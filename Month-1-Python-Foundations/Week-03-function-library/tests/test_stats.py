"""Tester för stats.py. Varje funktion prövas också med en tom lista, som ska ge ValueError."""

import pytest

from function_library.stats import mean, median, mode, stddev


class TestMean:
    def test_typical(self):
        assert mean([1, 2, 3, 4]) == pytest.approx(2.5)

    def test_single_value(self):
        assert mean([5]) == pytest.approx(5.0)

    def test_negative_values(self):
        assert mean([-2, 0, 2]) == pytest.approx(0.0)

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            mean([])


class TestMedian:
    def test_odd_count(self):
        assert median([3, 1, 2]) == 2

    def test_even_count_averages_middle_two(self):
        assert median([1, 2, 3, 4]) == pytest.approx(2.5)

    def test_single_value(self):
        assert median([7]) == 7

    def test_unsorted_input(self):
        assert median([5, 1, 4, 2, 3]) == 3

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            median([])


class TestMode:
    def test_clear_winner(self):
        assert mode([1, 2, 2, 3]) == 2

    def test_tie_returns_smallest(self):
        # 1 and 2 both occur twice; smallest wins for determinism.
        assert mode([1, 1, 2, 2]) == 1

    def test_single_value(self):
        assert mode([9]) == 9

    def test_all_same(self):
        assert mode([4, 4, 4]) == 4

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            mode([])


class TestStddev:
    def test_single_value_is_zero(self):
        assert stddev([5]) == pytest.approx(0.0)

    def test_all_identical_is_zero(self):
        assert stddev([3, 3, 3]) == pytest.approx(0.0)

    def test_known_population_value(self):
        # Population stddev of [2, 4, 4, 4, 5, 5, 7, 9] is exactly 2.0
        # (textbook example).
        assert stddev([2, 4, 4, 4, 5, 5, 7, 9]) == pytest.approx(2.0)

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            stddev([])
