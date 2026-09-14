"""LEGACY / TEACHING ARTIFACT — do not imitate this file.

This module is a deliberately bad "before" example: one giant, badly
named function that mixes numeric statistics and text processing
together with no decomposition into smaller pieces. It runs correctly
(there's no bug hunt here) and it is NOT covered by the automated test
suite on purpose — it exists to be refactored, not to be an API you
import and rely on. See this week's README, "Try It Yourself", for the
exercise: pull this apart into calls against `stats.py`/`text_utils.py`.
"""


def handle_data(d, t):
    total = 0
    cnt = 0
    for x in d:
        total = total + x
        cnt = cnt + 1
    avg = total / cnt

    sd_list = sorted(d)
    n = len(sd_list)
    if n % 2 == 0:
        med = (sd_list[n // 2 - 1] + sd_list[n // 2]) / 2
    else:
        med = sd_list[n // 2]

    counts = {}
    for x in d:
        if x in counts:
            counts[x] = counts[x] + 1
        else:
            counts[x] = 1
    best = None
    bestc = -1
    for k in counts:
        if counts[k] > bestc:
            bestc = counts[k]
            best = k

    vs = 0
    for x in d:
        vs = vs + (x - avg) ** 2
    var = vs / cnt
    sd = var ** 0.5

    words = t.split()
    wc = len(words)

    clean = ""
    for ch in t:
        if ch != " ":
            clean = clean + ch
    clean_lower = clean.lower()
    is_pal = clean_lower == clean_lower[::-1]

    print("=== Report ===")
    print("Average:", avg)
    print("Median:", med)
    print("Mode:", best)
    print("StdDev:", sd)
    print("Word count:", wc)
    print("Is palindrome:", is_pal)

    return {
        "average": avg,
        "median": med,
        "mode": best,
        "stddev": sd,
        "word_count": wc,
        "is_palindrome": is_pal,
    }
