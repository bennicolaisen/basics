# Facit: Övning 4.6 – Räkna bokstäver
#
# counts.get(character, 0) ger det nuvarande antalet, eller 0 om bokstaven
# inte setts förut. Det är räknemönstret för dictionaries, och det används
# i word_frequencies i veckans projekt.

def count_letters(text: str) -> dict[str, int]:
    counts = {}
    for character in text.lower():
        if character.isalpha():
            counts[character] = counts.get(character, 0) + 1
    return counts
