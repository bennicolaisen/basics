# Facit: Övning 3.9 – Porto
#
# Ogiltiga värden kontrolleras först och avvisas med ett tydligt fel.
# Varje if som träffar avslutar funktionen med return, så det behövs inga
# elif; den sista raden nås bara om inget annat stämde.

def postage(weight_grams: float) -> int:
    if weight_grams <= 0:
        raise ValueError("vikten måste vara mer än 0 g")
    if weight_grams <= 50:
        return 22
    if weight_grams <= 100:
        return 44
    if weight_grams <= 250:
        return 66
    if weight_grams <= 2000:
        return 99
    raise ValueError("för tungt för ett brev (max 2000 g)")
