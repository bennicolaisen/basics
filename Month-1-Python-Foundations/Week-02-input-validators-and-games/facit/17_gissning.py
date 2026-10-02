# Facit: Övning 2.17 – Svar på en gissning

def guess_feedback(guess, secret):
    if guess < secret:
        return "För lågt"
    elif guess > secret:
        return "För högt"
    else:
        return "Rätt!"
