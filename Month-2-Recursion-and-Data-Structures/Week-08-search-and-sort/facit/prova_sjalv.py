"""Facit till "Try It Yourself" i vecka 8. Förklaringarna finns i FACIT.md."""

import random
import time

from search_and_sort.sort import bubble_sort, insertion_sort, merge_sort, quick_sort


# Uppgift 1: mät alla fyra sorteringsalgoritmerna.
def benchmark_sorts(n: int = 5_000, seed: int = 1) -> dict[str, float]:
    """Sortera samma slumpade lista med varje algoritm. Returnerar sekunder per algoritm."""
    rng = random.Random(seed)
    data = [rng.randint(0, 1_000_000) for _ in range(n)]
    expected = sorted(data)
    timings = {}
    for sort in (bubble_sort, insertion_sort, merge_sort, quick_sort):
        start = time.perf_counter()
        result = sort(data)
        timings[sort.__name__] = time.perf_counter() - start
        assert result == expected, f"{sort.__name__} sorted incorrectly"
    return timings


# Uppgift 2
def selection_sort(lst: list) -> list:
    """Hitta minsta värdet i den osorterade delen och byt plats med dess första element.

    O(n²) jämförelser i alla fall, även för en redan sorterad lista. Inte
    stabil: bytet kan flytta ett element förbi ett annat med samma värde.
    """
    result = list(lst)
    for i in range(len(result)):
        smallest = i
        for j in range(i + 1, len(result)):
            if result[j] < result[smallest]:
                smallest = j
        result[i], result[smallest] = result[smallest], result[i]
    return result


# Uppgift 3: quicksort med första elementet som pivot.
def quick_sort_first_pivot(lst: list) -> list:
    if len(lst) <= 1:
        return list(lst)
    pivot = lst[0]
    less = [x for x in lst[1:] if x < pivot]
    equal = [x for x in lst if x == pivot]
    greater = [x for x in lst[1:] if x > pivot]
    return quick_sort_first_pivot(less) + equal + quick_sort_first_pivot(greater)


def benchmark_sorted_input(n: int = 900) -> dict[str, float]:
    """Tid för båda pivotvalen på en redan sorterad lista.

    n hålls under 1000 eftersom första-element-varianten rekurserar en nivå
    per element på sorterad indata, och Pythons gräns är ungefär 1000 nivåer.
    """
    data = list(range(n))
    timings = {}
    for sort in (quick_sort, quick_sort_first_pivot):
        start = time.perf_counter()
        sort(data)
        timings[sort.__name__] = time.perf_counter() - start
    return timings


# Uppgift 4: alla förekomster i O(log n + k).
def _first_index_not_less_than(sorted_lst: list, target) -> int:
    """Binärsökning efter den första platsen där sorted_lst[i] >= target."""
    low, high = 0, len(sorted_lst)
    while low < high:
        mid = (low + high) // 2
        if sorted_lst[mid] < target:
            low = mid + 1
        else:
            high = mid
    return low


def _first_index_greater_than(sorted_lst: list, target) -> int:
    """Binärsökning efter den första platsen där sorted_lst[i] > target."""
    low, high = 0, len(sorted_lst)
    while low < high:
        mid = (low + high) // 2
        if sorted_lst[mid] <= target:
            low = mid + 1
        else:
            high = mid
    return low


def find_all(sorted_lst: list, target) -> list[int]:
    start = _first_index_not_less_than(sorted_lst, target)
    end = _first_index_greater_than(sorted_lst, target)
    return list(range(start, end))


# Uppgift 5: sätt in i en sorterad lista.
def insert_sorted(sorted_lst: list, value) -> None:
    """Sätt in value på rätt plats i sorted_lst (ändrar listan).

    Att hitta platsen tar O(log n) med binärsökning, men själva insättningen
    måste flytta alla element efter platsen ett steg: O(n). Totalt O(n).
    """
    position = _first_index_greater_than(sorted_lst, value)
    sorted_lst.insert(position, value)


if __name__ == "__main__":
    for name, seconds in benchmark_sorts().items():
        print(f"{name:<15} {seconds * 1000:8.1f} ms")
    print()
    for name, seconds in benchmark_sorted_input().items():
        print(f"{name:<25} {seconds * 1000:8.1f} ms  (redan sorterad lista)")
