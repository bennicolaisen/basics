# Facit: Övning 3.11 – Initialer

def initials(full_name: str) -> str:
    result = ""
    for part in full_name.split():
        result = result + part[0].upper()
    return result
