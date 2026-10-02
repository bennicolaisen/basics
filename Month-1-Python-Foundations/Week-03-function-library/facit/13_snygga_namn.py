# Facit: Övning 3.13 – Snygga till ett namn
#
# split() utan argument tar hand om alla extra mellanslag, även i början
# och slutet. join är motsatsen till split: den sätter ihop en lista med
# texter, med texten före punkten (här ett mellanslag) mellan varje del.

def normalize_name(name: str) -> str:
    parts = []
    for part in name.split():
        parts.append(part.capitalize())
    return " ".join(parts)
