# Facit: Övning 3.7 – Störst av tre
#
# Det största av tre är det största av (det största av a och b) och c. Att
# bygga en funktion av en enklare som redan fungerar är kärnan i att dela
# upp problem.

def larger(a: float, b: float) -> float:
    if a >= b:
        return a
    return b


def largest_of_three(a: float, b: float, c: float) -> float:
    return larger(larger(a, b), c)
