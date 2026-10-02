# Facit: Övning 4.15 – Gruppera ord

def group_by_first_letter(words: list[str]) -> dict[str, list[str]]:
    groups = {}
    for word in words:
        first = word[0]
        if first not in groups:
            groups[first] = []
        groups[first].append(word)
    return groups
