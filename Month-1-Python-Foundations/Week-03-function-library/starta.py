"""Räkna statistik på egna tal. Skriv i terminalen (i den här mappen):

    python starta.py

(På Mac och Linux heter kommandot ofta python3.)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from function_library.stats import mean, median, mode, stddev  # noqa: E402
from function_library.text_utils import is_palindrome, word_count  # noqa: E402

numbers = []
for part in input("Skriv några tal med mellanslag mellan: ").split():
    numbers.append(float(part))

print(f"Medelvärde: {mean(numbers):.2f}")
print(f"Median: {median(numbers)}")
print(f"Typvärde: {mode(numbers)}")
print(f"Standardavvikelse: {stddev(numbers):.2f}")

text = input("Skriv en mening: ")
print(f"Antal ord: {word_count(text)}")
if is_palindrome(text):
    print("Meningen är en palindrom.")
else:
    print("Meningen är ingen palindrom.")
