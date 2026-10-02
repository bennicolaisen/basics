# Facit: Övning 4.12 – Comprehension med villkor

def words_longer_than(words: list[str], min_length: int) -> list[str]:
    return [word for word in words if len(word) > min_length]
