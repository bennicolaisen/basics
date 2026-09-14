"""Three ways to search a list: one that works on any list, and two that
require — and rely on — the list already being sorted.
"""


def linear_search(lst: list, target) -> int:
    """Return the index of the first occurrence of target in lst, or -1
    if it isn't present. Works on any list, sorted or not — it simply
    checks every element in order until it finds a match or runs out.
    """
    for i, item in enumerate(lst):
        if item == target:
            return i
    return -1


def binary_search_iterative(sorted_lst: list, target) -> int:
    """Return the index of target in sorted_lst, or -1 if absent.

    Requires sorted_lst to already be sorted in ascending order — this
    is not checked (checking would itself cost O(n), defeating the
    point). Passing an unsorted list gives an unspecified, meaningless
    result rather than an error.

    Repeatedly halves the search range: compare target against the
    middle element, and discard whichever half of the range can't
    possibly contain it, until the range is empty or the middle element
    matches.
    """
    low, high = 0, len(sorted_lst) - 1
    while low <= high:
        mid = (low + high) // 2
        if sorted_lst[mid] == target:
            return mid
        if sorted_lst[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def binary_search_recursive(sorted_lst: list, target) -> int:
    """Same contract as binary_search_iterative (requires sorted_lst to
    already be sorted ascending), implemented recursively instead of
    with a loop.

    Base cases: the search range is empty (low > high) -> return -1;
    the middle element is the target -> return its index.
    Recursive case: otherwise, recurse into whichever half of the range
    could still contain target.
    """

    def helper(low: int, high: int) -> int:
        if low > high:
            return -1
        mid = (low + high) // 2
        if sorted_lst[mid] == target:
            return mid
        if sorted_lst[mid] < target:
            return helper(mid + 1, high)
        return helper(low, mid - 1)

    return helper(0, len(sorted_lst) - 1)
