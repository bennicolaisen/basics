"""Tests for the Try It Yourself solutions in facit/prova_sjalv.py.

Timings are never asserted (they depend on the machine); only that the
benchmarks run and that every function gives correct results.
"""

import random
import sys

import pytest

from facit import prova_sjalv as facit
from search_and_sort.sort import quick_sort


class Item:
    """Compares by key only, so two items can be equal but distinguishable."""

    def __init__(self, key, label):
        self.key = key
        self.label = label

    def __lt__(self, other):
        return self.key < other.key

    def __gt__(self, other):
        return self.key > other.key

    def __eq__(self, other):
        return self.key == other.key


def test_1_benchmark_times_all_four_sorts():
    timings = facit.benchmark_sorts(n=300)
    assert set(timings) == {"bubble_sort", "insertion_sort", "merge_sort", "quick_sort"}
    assert all(seconds >= 0 for seconds in timings.values())


@pytest.mark.parametrize("data", [[], [1], [3, 1, 2], [5, 5, 1, 5], list(range(10, 0, -1))])
def test_2_selection_sort_sorts(data):
    assert facit.selection_sort(data) == sorted(data)


def test_2_selection_sort_leaves_input_alone():
    data = [3, 1, 2]
    facit.selection_sort(data)
    assert data == [3, 1, 2]


def test_2_selection_sort_is_not_stable():
    items = [Item(2, "a"), Item(2, "b"), Item(1, "c")]
    labels = [item.label for item in facit.selection_sort(items)]
    assert labels == ["c", "b", "a"]  # "a" and "b" swapped order


def test_3_first_pivot_quicksort_is_correct():
    rng = random.Random(7)
    data = [rng.randint(0, 50) for _ in range(200)]
    assert facit.quick_sort_first_pivot(data) == sorted(data)


@pytest.mark.skipif(sys.getrecursionlimit() > 5000, reason="needs Python's default recursion limit")
def test_3_sorted_input_is_the_worst_case():
    # One recursion level per element on sorted input: 5000 elements is far
    # past Python's limit for the first-element pivot, but the middle-element
    # pivot only needs about log2(5000) = 13 levels.
    data = list(range(5000))
    assert quick_sort(data) == data
    with pytest.raises(RecursionError):
        facit.quick_sort_first_pivot(data)


def test_3_sorted_input_benchmark_runs():
    timings = facit.benchmark_sorted_input(n=300)
    assert set(timings) == {"quick_sort", "quick_sort_first_pivot"}


@pytest.mark.parametrize(
    "data, target, expected",
    [
        ([1, 2, 2, 2, 3], 2, [1, 2, 3]),
        ([1, 2, 3], 4, []),
        ([1, 2, 3], 0, []),
        ([5, 5, 5], 5, [0, 1, 2]),
        ([], 1, []),
    ],
)
def test_4_find_all(data, target, expected):
    assert facit.find_all(data, target) == expected


@pytest.mark.parametrize(
    "data, value, expected",
    [
        ([1, 3, 5], 4, [1, 3, 4, 5]),
        ([1, 3, 5], 0, [0, 1, 3, 5]),
        ([1, 3, 5], 9, [1, 3, 5, 9]),
        ([], 2, [2]),
        ([2, 2], 2, [2, 2, 2]),
    ],
)
def test_5_insert_sorted(data, value, expected):
    facit.insert_sorted(data, value)
    assert data == expected
