"""Pure numeric statistics functions.

Every function takes a list of numbers and returns a single number (or,
for `mode`, the value that occurs most often). All of them raise
`ValueError` on an empty list — there is no meaningful mean, median,
mode, or spread of zero numbers, so refusing to guess is more correct
than returning `0` or `None` and letting a wrong answer travel silently
downstream.

Standard deviation here is the **population** standard deviation
(divide the sum of squared deviations by `len(nums)`, not `len(nums) - 1`).
That's a deliberate choice, not the only valid one: the *sample* standard
deviation (dividing by `n - 1`, "Bessel's correction") is more appropriate
when `nums` is a sample used to estimate the spread of some larger
population it was drawn from. Population standard deviation is used here
instead because it has one fewer edge case to explain to a beginner (it's
well-defined for `n == 1`, where it correctly gives `0.0`, whereas sample
stddev is undefined for `n == 1`) and because in this course's examples
`nums` is always treated as the *entire* dataset of interest, not a
sample standing in for something larger.
"""


def mean(nums: list[float]) -> float:
    """Arithmetic mean (average) of `nums`."""
    if not nums:
        raise ValueError("mean() requires at least one number")
    return sum(nums) / len(nums)


def median(nums: list[float]) -> float:
    """Middle value of `nums` once sorted; the average of the two middle
    values when `len(nums)` is even."""
    if not nums:
        raise ValueError("median() requires at least one number")

    ordered = sorted(nums)
    n = len(ordered)
    mid = n // 2

    if n % 2 == 1:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2


def mode(nums: list[float]) -> float:
    """Most frequently occurring value in `nums`.

    Ties are broken by returning the smallest of the tied values, so the
    result is deterministic (and reproducible in tests) rather than
    depending on iteration/insertion order.
    """
    if not nums:
        raise ValueError("mode() requires at least one number")

    counts: dict[float, int] = {}
    for value in nums:
        counts[value] = counts.get(value, 0) + 1

    highest_count = max(counts.values())
    tied_for_first = [value for value, count in counts.items() if count == highest_count]
    return min(tied_for_first)


def stddev(nums: list[float]) -> float:
    """Population standard deviation of `nums`. See module docstring for
    why population (not sample) standard deviation is used here."""
    if not nums:
        raise ValueError("stddev() requires at least one number")

    avg = mean(nums)
    variance = sum((x - avg) ** 2 for x in nums) / len(nums)
    return variance ** 0.5
