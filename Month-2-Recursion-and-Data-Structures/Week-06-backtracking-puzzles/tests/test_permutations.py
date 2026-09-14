from itertools import permutations as itertools_permutations
from math import factorial

from backtracking_puzzles.permutations import all_permutations


def test_empty_list():
    assert all_permutations([]) == [[]]


def test_single_element():
    assert all_permutations([1]) == [[1]]


def test_count_matches_factorial_length_3():
    result = all_permutations([1, 2, 3])
    assert len(result) == factorial(3)


def test_count_matches_factorial_length_4():
    result = all_permutations(["a", "b", "c", "d"])
    assert len(result) == factorial(4)


def test_no_duplicates_and_all_unique_orderings():
    lst = [1, 2, 3]
    result = all_permutations(lst)
    result_as_tuples = {tuple(p) for p in result}
    expected = {p for p in itertools_permutations(lst)}
    assert result_as_tuples == expected


def test_every_permutation_is_same_multiset_as_input():
    lst = [1, 2, 2]
    for perm in all_permutations(lst):
        assert sorted(perm) == sorted(lst)
