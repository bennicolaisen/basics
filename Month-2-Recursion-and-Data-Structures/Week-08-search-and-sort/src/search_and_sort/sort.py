"""Four sorting algorithms. Every one of them returns a *new* sorted
list and leaves its input untouched — none of them mutate lst in place.
That's a deliberate design choice here (not a requirement of the
algorithms themselves, several of which are traditionally taught
in-place): it keeps every function's behavior obvious from its
signature alone, and makes it trivial to compare a function's output
against its original input in tests without needing to copy anything
first.

Stability means: two elements that compare equal keep their original
relative order in the output. It's noted per function below.
"""


def bubble_sort(lst: list) -> list:
    """Repeatedly sweep the list, swapping any adjacent out-of-order
    pair, until a full sweep makes no swaps. Stable: only strictly
    out-of-order adjacent pairs are swapped, so equal elements are never
    reordered relative to each other.
    """
    result = list(lst)
    n = len(result)
    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        if not swapped:
            break
    return result


def insertion_sort(lst: list) -> list:
    """Build up a sorted prefix one element at a time: take the next
    element and shift it leftward past everything strictly greater than
    it. Stable: shifting only happens past strictly-greater elements, so
    an element never moves past one it's equal to.
    """
    result = list(lst)
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    return result


def merge_sort(lst: list) -> list:
    """Split the list in half, recursively sort each half, then merge
    the two sorted halves back together. Stable: when merging, an
    element from the left half is taken before an equal element from the
    right half (see `<=` in `_merge`), preserving original relative order.
    """
    if len(lst) <= 1:
        return list(lst)

    mid = len(lst) // 2
    left = merge_sort(lst[:mid])
    right = merge_sort(lst[mid:])
    return _merge(left, right)


def _merge(left: list, right: list) -> list:
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def quick_sort(lst: list) -> list:
    """Pick a pivot, partition the rest into "less than", "equal to",
    and "greater than" groups, and recursively sort the less/greater
    groups around the (already-in-place) equal group.

    Stable *in this specific implementation*: because partitioning here
    builds three new lists by scanning lst left to right (rather than
    swapping elements in place, as classic textbook quicksort does),
    elements within each group keep their original relative order. That
    is a property of this particular approach, not of "quicksort" as an
    algorithm in general — the common in-place, swap-based version is
    not stable.
    """
    if len(lst) <= 1:
        return list(lst)

    pivot = lst[len(lst) // 2]
    less = [x for x in lst if x < pivot]
    equal = [x for x in lst if x == pivot]
    greater = [x for x in lst if x > pivot]
    return quick_sort(less) + equal + quick_sort(greater)
