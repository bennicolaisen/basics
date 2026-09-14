"""Hands-on experiment: time linear_search against binary_search_iterative
on a large sorted list, for a worst-case target (one that isn't in the
list at all, so both functions have to look as hard as they possibly
can before giving up).

This is meant to be *run and read*, not asserted on. Wall-clock timings
vary by machine, load, and Python version — turning "binary search should
be faster" into a pytest assertion with a hard threshold would be flaky
by nature (see `tests/` for why this repo avoids that: only correctness
is tested there). Run this file directly to see the difference for
yourself.
"""

import time

from search_and_sort.search import binary_search_iterative, linear_search


def run_benchmark(n: int = 100_000) -> None:
    sorted_list = list(range(n))
    # A target guaranteed absent from the list: both searches are forced
    # into their worst case (linear_search scans every element; binary
    # search halves the range all the way down to nothing).
    worst_case_target = -1

    start = time.perf_counter()
    linear_result = linear_search(sorted_list, worst_case_target)
    linear_elapsed = time.perf_counter() - start

    start = time.perf_counter()
    binary_result = binary_search_iterative(sorted_list, worst_case_target)
    binary_elapsed = time.perf_counter() - start

    assert linear_result == -1 and binary_result == -1  # sanity check

    print(f"List size: {n:,}")
    print(f"linear_search:          {linear_elapsed * 1000:.4f} ms")
    print(f"binary_search_iterative: {binary_elapsed * 1000:.4f} ms")
    if binary_elapsed > 0:
        print(f"linear_search took ~{linear_elapsed / binary_elapsed:.0f}x longer")


if __name__ == "__main__":
    run_benchmark()
