# Facit: Övning 3.5 – Lokala variabler
#
# Parametern count är en lokal variabel: när funktionen tar slut
# försvinner den, och ändringen med den. Det riktiga sättet att få ut ett
# värde ur en funktion är return, och den som anropar sparar svaret: count
# = add_one(count).

count = 0


def add_one(count):
    return count + 1


count = add_one(count)
print(count)
