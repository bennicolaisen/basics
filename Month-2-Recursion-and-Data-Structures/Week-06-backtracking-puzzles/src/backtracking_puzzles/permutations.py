"""Generate every permutation of a list, recursively, with no `itertools`.

The point isn't that `itertools.permutations` doesn't exist — it's building
the recursive "choose one element, recurse on what's left, put it back
together" pattern yourself, because that exact pattern (choose -> recurse ->
undo the choice) is the backbone of `maze_solver.py` and `subset_sum.py` in
this same week.
"""


def all_permutations(lst: list) -> list[list]:
    """Return a list of all permutations of lst, each as its own list.

    Base case: an empty list has exactly one permutation — itself (the
    empty arrangement).
    Recursive case: for each element in lst, temporarily set that element
    aside, recursively find all permutations of the *rest* of the list,
    then place the set-aside element at the front of each of those.

    Order of the output is not guaranteed to match any particular
    convention (e.g. `itertools.permutations`'s lexicographic-by-index
    order) — only that every permutation appears exactly once.
    """
    if len(lst) == 0:
        return [[]]

    permutations = []
    for i in range(len(lst)):
        chosen = lst[i]
        remaining = lst[:i] + lst[i + 1:]
        for rest_permutation in all_permutations(remaining):
            permutations.append([chosen] + rest_permutation)
    return permutations
