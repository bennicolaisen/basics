# Facit: Övning 1.10 – Avrunda till närmaste steg. Förklaring i FACIT.md.


def round_to_nearest(value, step):
    return (2 * value + step) // (2 * step) * step
