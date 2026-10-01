# Facit: Övning 4.8 – Slå ihop två räkningar
#
# dict(first) gör en kopia. Om man skrev result = first skulle result bara
# vara ett nytt namn på samma dictionary, och ändringarna skulle synas i
# first också.

def merge_counts(first: dict[str, int], second: dict[str, int]) -> dict[str, int]:
    result = dict(first)
    for item, count in second.items():
        result[item] = result.get(item, 0) + count
    return result
