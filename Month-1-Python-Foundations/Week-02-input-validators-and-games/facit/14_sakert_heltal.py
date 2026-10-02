# Facit: Övning 2.14 – Fånga ett fel

def to_int_or_none(text):
    try:
        return int(text)
    except ValueError:
        return None
