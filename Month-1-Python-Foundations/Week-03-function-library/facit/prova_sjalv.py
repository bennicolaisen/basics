"""Facit till "Prova själv" i vecka 3. Förklaringarna finns i FACIT.md."""

from function_library.stats import mean, median, mode
from function_library.text_utils import is_palindrome, word_count


# Uppgift 1: legacy_report.handle_data uppdelad i anrop till biblioteket.
def build_report(numbers: list[float], text: str) -> str:
    """Samma rapport som handle_data, men som text i stället för utskrift."""
    lines = [
        "=== Rapport ===",
        f"Medelvärde: {mean(numbers)}",
        f"Median: {median(numbers)}",
        f"Typvärde: {mode(numbers)}",
        f"Standardavvikelse: {stddev(numbers)}",
        f"Antal ord: {word_count(text)}",
        f"Palindrom: {is_palindrome(text)}",
    ]
    return "\n".join(lines)


# Uppgift 2: variansen som en egen funktion, och stddev byggd på den.
def variance(numbers: list[float]) -> float:
    """Medelvärdet av de kvadrerade avvikelserna från medelvärdet."""
    average = mean(numbers)
    total = 0
    for value in numbers:
        total = total + (value - average) ** 2
    return total / len(numbers)


def stddev(numbers: list[float]) -> float:
    return variance(numbers) ** 0.5


# Uppgift 3
def most_common_word(text: str) -> str:
    """Det vanligaste ordet (små bokstäver). Vid lika antal vinner det som kommer först i bokstavsordning."""
    words = text.lower().split()
    if len(words) == 0:
        raise ValueError("texten innehåller inga ord")
    best = words[0]
    best_count = 0
    for word in sorted(words):
        count = words.count(word)
        if count > best_count:
            best = word
            best_count = count
    return best


# Uppgift 4
def modes(numbers: list[float]) -> list[float]:
    """Alla värden som förekommer flest gånger, sorterade."""
    if len(numbers) == 0:
        raise ValueError("modes() behöver minst ett tal")
    highest = 0
    for value in numbers:
        if numbers.count(value) > highest:
            highest = numbers.count(value)
    result = []
    for value in sorted(numbers):
        if numbers.count(value) == highest and value not in result:
            result.append(value)
    return result


# Uppgift 5
def summary(numbers: list[float], decimals: int = 2) -> str:
    return (
        f"medel {round(mean(numbers), decimals)}, "
        f"median {round(median(numbers), decimals)}, "
        f"typvärde {mode(numbers)}, "
        f"standardavvikelse {round(stddev(numbers), decimals)}"
    )
