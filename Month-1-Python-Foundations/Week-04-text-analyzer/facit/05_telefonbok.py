# Facit: Övning 4.5 – Slå upp i en dictionary

def lookup(phone_book: dict[str, str], name: str) -> str:
    return phone_book.get(name, "okänt")
