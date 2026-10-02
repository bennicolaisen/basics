# Facit: Övning 3.10 – Långa ord

def count_long_words(text: str, min_length: int = 5) -> int:
    count = 0
    for word in text.split():
        if len(word) > min_length:
            count = count + 1
    return count
