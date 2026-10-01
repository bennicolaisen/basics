# Facit: Övning 4.16 – Läs en fil

def count_lines_and_words(path) -> tuple[int, int]:
    lines = 0
    words = 0
    with open(path, encoding="utf-8") as file:
        for line in file:
            lines = lines + 1
            words = words + len(line.split())
    return (lines, words)
