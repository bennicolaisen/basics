# Facit: Övning 1.8 – Namn. Förklaring i FACIT.md.

namn = input("Namn: ").strip()
mellanslag = namn.find(" ")
fornamn = namn[:mellanslag]
efternamn = namn[mellanslag + 1:]
fornamn = fornamn[0].upper() + fornamn[1:].lower()
efternamn = efternamn[0].upper() + efternamn[1:].lower()
print(f"Initialer: {fornamn[0]}.{efternamn[0]}.")
print(f"Katalognamn: {efternamn}, {fornamn}")
