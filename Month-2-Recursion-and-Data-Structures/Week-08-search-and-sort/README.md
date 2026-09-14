# Week 8 — Search and Sort

## Purpose

This is Month 2's capstone-adjacent week. Searching and sorting are
where "how much work does my code actually do" stops being an abstract
question and becomes something you can feel directly — a linear search
that takes a fraction of a second on 100 elements and visibly longer on
100,000 is Big-O made concrete instead of theoretical. This week
implements the standard searches and sorts from scratch and gives you a
way to actually watch the difference.

## Objectives

The code in this project demonstrates:

- **Search**: `linear_search` (works on anything), `binary_search_iterative`
  and `binary_search_recursive` (both require a sorted list, and both are
  implemented here — the loop version and the recursive version, so you
  can compare the same algorithm in both styles).
- **Sort**: `bubble_sort`, `insertion_sort`, `merge_sort`, `quick_sort` —
  four different strategies for the same problem, each returning a new
  list and leaving its input untouched.
- **Measuring**, not just asserting: `benchmark.py` times linear vs.
  binary search on a large list so the Big-O difference is something you
  see happen, not just something you're told.

## Concepts Refresher

### Big-O, informally

Big-O describes **how the amount of work an algorithm does grows as its
input grows** — not how fast it runs on your specific machine today, but
the shape of the curve as the input gets bigger. Two algorithms can both
"work correctly"; Big-O is about which one's workload explodes and which
one's stays manageable as `n` grows.

The clearest gut-check: **what happens if you double the input size?**

- **O(1)** — constant: doubling the input changes nothing. Looking up
  `dict[key]`.
- **O(log n)** — logarithmic: doubling the input adds roughly *one more
  step*. This is binary search's whole trick — each comparison throws
  away half of what's left, so the number of comparisons needed grows
  incredibly slowly. Searching 1,000,000 sorted elements takes at most
  ~20 comparisons; searching 2,000,000 takes at most ~21.
- **O(n)** — linear: doubling the input roughly doubles the work.
  `linear_search` — worst case, you check every element once.
- **O(n log n)** — doubling the input slightly more than doubles the
  work. `merge_sort`'s and (average-case) `quick_sort`'s territory: `n`
  elements, each one touched roughly `log n` times as the problem keeps
  getting split in half.
- **O(n²)** — quadratic: doubling the input roughly *quadruples* the
  work. `bubble_sort` and `insertion_sort`'s worst case — for every one
  of `n` elements, potentially scan/shift past up to `n` others.

### Time complexity of everything implemented here

| Algorithm | Best case | Average case | Worst case | Requires sorted input? |
|---|---|---|---|---|
| `linear_search` | O(1) | O(n) | O(n) | No |
| `binary_search_iterative` | O(1) | O(log n) | O(log n) | Yes |
| `binary_search_recursive` | O(1) | O(log n) | O(log n) | Yes |
| `bubble_sort` | O(n) | O(n²) | O(n²) | — |
| `insertion_sort` | O(n) | O(n²) | O(n²) | — |
| `merge_sort` | O(n log n) | O(n log n) | O(n log n) | — |
| `quick_sort` | O(n log n) | O(n log n) | O(n²) | — |

Notes on the entries that aren't obvious from the table alone:

- `bubble_sort`'s and `insertion_sort`'s **best case is O(n)**, not
  O(n²) — both are implemented to recognize an already-sorted list
  quickly (`bubble_sort` stops early once a full pass makes no swaps;
  `insertion_sort`'s inner `while` loop simply never runs when nothing is
  out of place) rather than grinding through unnecessary comparisons.
- `merge_sort` has **no bad worst case** — it always splits the list
  exactly in half regardless of the data, so its performance doesn't
  depend on the input's existing order at all.
- `quick_sort`'s **worst case is O(n²)**, and it happens specifically
  when the chosen pivot is consistently the smallest or largest remaining
  element — one partition ends up empty every time, so the recursion
  barely shrinks the problem per call. This implementation picks the
  *middle* element as pivot specifically to make already-sorted or
  reverse-sorted input (a common worst-case trigger for a first/last-
  element pivot choice) behave reasonably.

### Why binary search needs sorted input

Binary search's speed comes entirely from being able to eliminate half
the remaining elements with one comparison — but that's only a valid
move if "everything before the midpoint is smaller, everything after is
larger" is guaranteed. On an unsorted list, comparing against the middle
element tells you nothing about where the target could be, so there's
nothing valid to eliminate. This isn't a performance nuance, it's a
correctness requirement — `binary_search_iterative`/`_recursive` will
return wrong or missing results on unsorted input, silently, not raise an
error (checking sortedness would itself cost O(n), erasing the entire
point of using binary search in the first place).

## Design & Architecture

```
Week-08-search-and-sort/
├── README.md
├── conftest.py                       # adds src/ to sys.path for pytest
├── src/
│   └── search_and_sort/
│       ├── __init__.py
│       ├── search.py                 # linear/binary (iterative + recursive)
│       ├── sort.py                   # bubble/insertion/merge/quick
│       └── benchmark.py              # hands-on timing script, not a test
└── tests/
    ├── test_search.py
    └── test_sort.py
```

`search.py` and `sort.py` are independent of each other; `benchmark.py`
depends only on `search.py`. Tests are parametrized across all four sort
functions and both binary search variants so the same correctness checks
run against every implementation without duplicating test code per
algorithm.

## How to Build & Run

No build step — pure standard library.

```bash
cd Month-2-Recursion-and-Data-Structures/Week-08-search-and-sort
PYTHONPATH=src python3 -c "
from search_and_sort.sort import merge_sort
print(merge_sort([5, 3, 4, 1, 2]))
"
```

Run the benchmark experiment directly:

```bash
cd Month-2-Recursion-and-Data-Structures/Week-08-search-and-sort
PYTHONPATH=src python3 -m search_and_sort.benchmark
```

## Testing

```bash
cd Month-2-Recursion-and-Data-Structures/Week-08-search-and-sort
python -m pytest -q
```

`conftest.py` puts `src/` on `sys.path`, so `pytest` runs with zero extra
flags from this directory. Coverage, for every search and every sort:
empty list, single element, duplicates, already-sorted input,
reverse-sorted input, and a randomized correctness check (comparing
against Python's built-in `sorted()`). Sort functions are additionally
checked for *not mutating* their input and for returning an actual
permutation of it. `benchmark.py` is intentionally **not** covered by
`pytest` — timing assertions in CI are flaky by nature, so it's a script
to run and read, not something to assert against.

## Try It Yourself

1. **Time all four sorts, not just the two searches.** Extend
   `benchmark.py` (or write a new script) to time `bubble_sort`,
   `insertion_sort`, `merge_sort`, and `quick_sort` on a list of 5,000
   random integers each. Does the O(n²) vs. O(n log n) gap from the table
   show up the way you'd expect?
2. **Selection sort.** Implement `selection_sort(lst)`: repeatedly find
   the minimum of the unsorted remainder and move it to the front. Work
   out its time complexity yourself and add a row to your own copy of
   the table above — is it stable?
3. **A first-element-pivot quicksort worst case.** Modify (a copy of)
   `quick_sort` to always use `lst[0]` as the pivot instead of the
   middle element, then benchmark it against the original on an
   already-sorted list of a few thousand elements. Confirm the O(n²)
   worst case actually shows up.
4. **`find_all(lst, target)`.** Using `binary_search_iterative` as a
   starting point, write a function that returns *every* index where
   target appears in a sorted list with duplicates (in O(log n + k) time,
   where k is the number of matches) — not just one arbitrary match.
5. **A sorted `insert(lst, value)`.** Write a function that inserts
   `value` into an already-sorted list, keeping it sorted, in better than
   O(n log n) time (i.e. don't just append and re-sort). What's the best
   complexity you can get, and what part of the operation is the
   unavoidable bottleneck?

## Reflection

`quick_sort` here is written functionally (build `less`/`equal`/`greater`
lists with comprehensions) instead of the classic in-place, swap-based
partition scheme most textbooks show. That trade-off is worth naming: it
makes the algorithm dramatically easier to read and reason about — and,
as a side effect, this implementation is stable, while textbook quicksort
usually isn't — but it costs O(n) extra memory per recursive call for the
new lists, instead of sorting in place within the original array. For a
learning week, prioritizing "you can read this and see exactly what it's
doing" over squeezing out that memory cost is the right call; it's worth
knowing the classic in-place version is what you'd reach for if memory
pressure genuinely mattered.
