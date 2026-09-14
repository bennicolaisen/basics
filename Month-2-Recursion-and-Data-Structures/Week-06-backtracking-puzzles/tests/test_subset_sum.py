from backtracking_puzzles.subset_sum import has_subset_sum


def test_empty_list_target_zero_is_true():
    assert has_subset_sum([], 0) is True


def test_empty_list_nonzero_target_is_false():
    assert has_subset_sum([], 5) is False


def test_target_zero_nonempty_list_is_true():
    assert has_subset_sum([1, 2, 3], 0) is True


def test_simple_true_case():
    assert has_subset_sum([3, 34, 4, 12, 5, 2], 9) is True


def test_simple_false_case():
    assert has_subset_sum([3, 34, 4, 12, 5, 2], 30) is False


def test_exact_single_element_match():
    assert has_subset_sum([7, 1, 2], 7) is True


def test_needs_all_elements():
    assert has_subset_sum([1, 2, 3], 6) is True


def test_unreachable_target():
    assert has_subset_sum([1, 2, 3], 100) is False
