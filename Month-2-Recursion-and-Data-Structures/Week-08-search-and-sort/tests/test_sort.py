import random

import pytest

from search_and_sort.sort import bubble_sort, insertion_sort, merge_sort, quick_sort

SORTS = [bubble_sort, insertion_sort, merge_sort, quick_sort]


@pytest.mark.parametrize("sort_fn", SORTS)
class TestSortCorrectness:
    def test_empty_list(self, sort_fn):
        assert sort_fn([]) == []

    def test_single_element(self, sort_fn):
        assert sort_fn([42]) == [42]

    def test_already_sorted(self, sort_fn):
        assert sort_fn([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def test_reverse_sorted(self, sort_fn):
        assert sort_fn([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    def test_duplicates(self, sort_fn):
        assert sort_fn([3, 1, 2, 3, 1]) == [1, 1, 2, 3, 3]

    def test_all_equal(self, sort_fn):
        assert sort_fn([7, 7, 7, 7]) == [7, 7, 7, 7]

    def test_does_not_mutate_input(self, sort_fn):
        original = [5, 3, 4, 1, 2]
        snapshot = list(original)
        sort_fn(original)
        assert original == snapshot

    def test_returns_new_list_object(self, sort_fn):
        original = [3, 1, 2]
        result = sort_fn(original)
        assert result is not original

    def test_is_permutation_of_input(self, sort_fn):
        original = [4, 2, 7, 1, 9, 2, 4]
        result = sort_fn(original)
        assert sorted(result) == sorted(original)
        assert len(result) == len(original)

    def test_randomized_against_builtin_sorted(self, sort_fn):
        random.seed(42)
        for _ in range(20):
            data = [random.randint(-100, 100) for _ in range(random.randint(0, 50))]
            assert sort_fn(data) == sorted(data)

    def test_negative_numbers(self, sort_fn):
        assert sort_fn([-3, 5, -1, 0, 2]) == [-3, -1, 0, 2, 5]
