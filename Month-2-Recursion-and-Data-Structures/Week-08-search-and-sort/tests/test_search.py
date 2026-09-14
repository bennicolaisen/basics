import pytest

from search_and_sort.search import (
    binary_search_iterative,
    binary_search_recursive,
    linear_search,
)

BINARY_SEARCHES = [binary_search_iterative, binary_search_recursive]


class TestLinearSearch:
    def test_empty_list(self):
        assert linear_search([], 5) == -1

    def test_single_element_found(self):
        assert linear_search([7], 7) == 0

    def test_single_element_not_found(self):
        assert linear_search([7], 3) == -1

    def test_found_in_unsorted_list(self):
        assert linear_search([5, 1, 9, 3], 9) == 2

    def test_not_found(self):
        assert linear_search([5, 1, 9, 3], 100) == -1

    def test_duplicates_returns_first_index(self):
        assert linear_search([1, 2, 2, 2, 3], 2) == 1


@pytest.mark.parametrize("search", BINARY_SEARCHES)
class TestBinarySearches:
    def test_empty_list(self, search):
        assert search([], 5) == -1

    def test_single_element_found(self, search):
        assert search([7], 7) == 0

    def test_single_element_not_found(self, search):
        assert search([7], 3) == -1

    def test_found_at_various_positions(self, search):
        sorted_lst = [1, 3, 5, 7, 9, 11, 13]
        for target in sorted_lst:
            assert sorted_lst[search(sorted_lst, target)] == target

    def test_not_found_below_range(self, search):
        assert search([1, 3, 5, 7], 0) == -1

    def test_not_found_above_range(self, search):
        assert search([1, 3, 5, 7], 100) == -1

    def test_not_found_between_elements(self, search):
        assert search([1, 3, 5, 7], 4) == -1

    def test_duplicates_finds_a_valid_index(self, search):
        sorted_lst = [1, 2, 2, 2, 3]
        idx = search(sorted_lst, 2)
        assert sorted_lst[idx] == 2

    def test_already_sorted_large_range(self, search):
        sorted_lst = list(range(0, 1000, 2))
        assert search(sorted_lst, 500) == 250
        assert search(sorted_lst, 501) == -1
