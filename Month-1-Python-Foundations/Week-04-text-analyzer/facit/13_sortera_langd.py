# Facit: Övning 4.13 – Sortera med en nyckel
#
# Tupler jämförs ett värde i taget: först längden, och bara om den är lika
# jämförs ordet. Det ger "längd först, sedan bokstavsordning" utan någon
# extra kod. Kortare med lambda: sorted(words, key=lambda word:
# (len(word), word)).

def length_then_word(word: str) -> tuple[int, str]:
    return (len(word), word)


def sort_by_length(words: list[str]) -> list[str]:
    return sorted(words, key=length_then_word)
