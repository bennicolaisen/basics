"""Decide whether some subset of a list of numbers sums to a target value,
using backtracking: for each number, try *including* it, and if that whole
branch fails to reach the target, undo that choice and try *excluding* it
instead.
"""


def has_subset_sum(nums: list[float], target: float) -> bool:
    """Return True if some subset of nums (possibly empty) sums to target.

    Base cases:
    - remaining == 0 -> True (the numbers chosen so far already sum to
      target; the empty subset itself sums to 0, which covers target == 0
      directly, including for an empty nums).
    - no numbers left to consider and remaining != 0 -> False.

    Recursive case: for the next number, first try including it
    (recurse with target reduced by that number). If that branch doesn't
    find a solution, *undo the inclusion* — the recursive call simply
    returns False and nothing about `nums` was ever mutated, so trying
    "exclude this number instead" is just a second, independent recursive
    call starting from the same state.
    """

    def backtrack(index: int, remaining: float) -> bool:
        if remaining == 0:
            return True
        if index >= len(nums):
            return False

        include = backtrack(index + 1, remaining - nums[index])
        if include:
            return True

        exclude = backtrack(index + 1, remaining)
        return exclude

    return backtrack(0, target)
